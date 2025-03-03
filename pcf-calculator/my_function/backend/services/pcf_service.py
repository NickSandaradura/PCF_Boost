import base64
import uuid
import json
import os
from flask import request, render_template, redirect, url_for, current_app
from my_function.backend.business_logic.geo_plot import GeoPlot
from dataclasses import asdict
from my_function.backend.services.lst_service import LstRequestService
from my_function.backend.services.rp_service import RpRequestService
from my_function.backend.business_logic.base64_encoder import Base64Encoder
from my_function.backend.services.nash_service import NashRequestService
from my_function.backend.exceptions.lst_exception import LstParserApiRequestException
from my_function.backend.exceptions.nash_exceptions import NashApiRequestException
from my_function.backend.exceptions.rp_exception import ResourcePredictionRequestException
from my_function.backend.business_logic.pcf_calculator import GeoPcfCalculator
from my_function.models.geo_dto import GeoDto
from my_function.models.laser_dto import LaserDto
from my_function.models.material_dto import MaterialDto
from concurrent.futures import ThreadPoolExecutor

DATA_TTL = 600
DATA_FOLDER = "/tmp/data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


lst_service = LstRequestService()
b64_encoder = Base64Encoder()
rp_service = RpRequestService()
nash_service = NashRequestService()

def register_routes(app,cache_service):
    @app.route("/")
    def index():
        return render_template('index.html')


    @app.route('/geo/pcf', methods=['POST'])
    def geo_part_carbon_footprint():
        file_data = request.get_data()
        file_name = request.headers.get('Filename', 'uploaded_file')
        thickness = request.headers.get('Thickness')
        laser = request.headers.get('Laser')
        material_id = request.headers.get('Materialid')
        cut_gas = request.headers.get('Gasid')
        request_id = str(uuid.uuid4())
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_image = executor.submit(create_geo_image, file_data, file_name, lst_service, DATA_FOLDER, request_id)
            future_pcf = executor.submit(calculate_geo_pcf, file_data, file_name, thickness, laser, material_id, cut_gas,request_id)
            image_result = future_image.result()
            pcf_result = future_pcf.result()
        
        cache_service.setex(f"part_{request_id}", DATA_TTL, json.dumps(pcf_result))
        cache_service.setex(f"image_{request_id}", DATA_TTL, image_result)
        return redirect(url_for('pcf_report_page', request_id=request_id))

        

    @app.route('/geo-pcf-report/<request_id>')
    def pcf_report_page(request_id):
        part_data = cache_service.get(f"part_{request_id}")
        image_base64 = cache_service.get(f"image_{request_id}")
        error_message = cache_service.get(f"error_message_{request_id}")
        part = json.loads(part_data) if part_data else None
        return render_template('pcf.html', part=part, error_message=error_message,image=image_base64)
        
    def calculate_geo_pcf(file_data, file_name, thickness, laser, material_id, cut_gas, request_id):
        try:
            content_base64 = b64_encoder.encode_to_base64(file_data)
            geo_dto = GeoDto(file_name, LaserDto(laser), MaterialDto(material_id,thickness), cut_gas, content_base64)
            part = rp_service.post_geo_request(geo_dto)
            nash_service.post_energy_request(part)
            geo_pcf_calculator = GeoPcfCalculator(part)
            geo_pcf_calculator.calc_pcf()
            return asdict(part)
        except ResourcePredictionRequestException as e:
            cache_service.setex(f"error_message_{request_id}", DATA_TTL, str(e))
        except NashApiRequestException as e:
            cache_service.setex(f"error_message_{request_id}", DATA_TTL, str(e))
            return asdict(part)
            
        
    def create_geo_image(file_data, file_name, lst_service, data_folder,request_id):
        geo_plot = GeoPlot()
        try:
            image_bytes = geo_plot.create_geo_image(file_data, file_name, lst_service, data_folder)
            return base64.b64encode(image_bytes).decode('utf-8')    
        except LstParserApiRequestException as e:
            cache_service.setex(f"error_message_{request_id}", DATA_TTL, str(e))
        except Exception as e:
            cache_service.setex(f"error_message_{request_id}", DATA_TTL, str(e))