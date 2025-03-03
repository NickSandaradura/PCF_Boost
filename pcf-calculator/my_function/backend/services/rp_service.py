import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from my_function.models.geo_dto import GeoDto
from dataclasses import asdict
from my_function.models.part_dto import PartDto
from my_function.backend.interfaces.request_service_interface import RpRequestServiceInterface
from my_function.backend.exceptions.rp_exception import ResourcePredictionRequestException
from my_function.models.sheet_dto import SheetDto


load_dotenv()


class RpRequestService(RpRequestServiceInterface):
    def __init__(self):
        self.url = 'https://api-s.trumpf.com/resource-prediction/1.0'

    def _request_access_token(self):
        client_id = os.environ["RP_CLIENT_ID"]
        client_secret = os.environ["RP_CLIENT_SECRET"]

        if not client_id or not client_secret:
            raise ValueError(
                "Client ID or Client Secret not set in environment variables")

        idm_url = "https://identity-s.trumpf.com/oauth2/token"
        if os.environ.get("PROXY") != None:
            response = requests.post(
                idm_url,
                data={"grant_type": "client_credentials"},
                auth=(client_id, client_secret),
                proxies={"https": os.environ["PROXY"]}   
            )
        else:
            response = requests.post(
                idm_url,
                data={"grant_type": "client_credentials"},
                auth=(client_id, client_secret),
            )
        response_data = response.json()
        self.access_token = response_data["access_token"]
        expires_in = response_data["expires_in"]

        self.token_expiration = datetime.now() + timedelta(seconds=expires_in)

    def _get_access_token(self):
        if (not self.access_token or
            not self.token_expiration or
                (self.token_expiration - datetime.now() <= timedelta(minutes=5))):
            self._request_access_token()
        return self.access_token
    
    def _build_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_access_token()}'
        }

    def post_geo_request(self, payload: GeoDto):
        
            headers = self._build_headers()
            payload_dict = asdict(payload)
            payload_str = json.dumps(payload_dict)
            try:
                if os.environ.get("PROXY") != None:
                    response = requests.post(
                        self.url + "/part-consumptions/tru-laser",
                        headers=headers,
                        data=payload_str,
                        proxies={"https": os.environ["PROXY"]})       
                    response.raise_for_status()             
                    response_data = response.json()
                    part = self._process_post_geo_response(response_data,payload)
                    return part
                else:
                    response = requests.post(
                        self.url + "/part-consumptions/tru-laser",
                        headers=headers,
                        data=payload_str)       
                    response.raise_for_status()             
                    response_data = response.json()
                    part = self._process_post_geo_response(response_data,payload)
                    return part

            except requests.RequestException as e:
                self._handle_error(e)
 

    def _process_post_geo_response(self,data:dict, geo_dto : GeoDto)->PartDto:
        laser = geo_dto.machine_definition
        material = geo_dto.material
        weight = data["consumptions"]["part_consumptions"]["weight"]["value"]
        area = data["consumptions"]["part_consumptions"]["area"]["value"]
        part_scrap_weight = data["consumptions"]["part_consumptions"]["scrap_weight"]["value"]
        part_scrap_area = data["consumptions"]["part_consumptions"]["scrap_area"]["value"]
        sheet_scrap_weight = data["consumptions"]["non_part_relevant_consumptions"]["sheet_scrap_weight"]["value"]
        sheet_scrap_area = data["consumptions"]["non_part_relevant_consumptions"]["sheet_scrap_area"]["value"]      
        time = data["consumptions"]["part_consumptions"]["time"]["value"]
        gas_consumption = data["consumptions"]["part_consumptions"]["gas"]["consumption"]["value"]
        energy_consumption = data["consumptions"]["part_consumptions"]["energy"]["value"]
        cut_gas = geo_dto.cut_gas
        sheet = SheetDto(sheet_scrap_weight,sheet_scrap_area) 
        return PartDto(material, laser, geo_dto.name, 
        weight, area, part_scrap_weight, part_scrap_area,sheet,time,cut_gas,gas_consumption,energy_consumption)
        

    def _handle_error(self, exception:requests.RequestException):
        if exception.response.status_code == 422:
            raise ResourcePredictionRequestException(
            message=f"Resource Prediction cant process the Combination of these Inputparameters",
            details=exception.__str__
        )

        if exception.response.status_code == 500:
            raise ResourcePredictionRequestException(
            message=f"Cant Connect to Resource Prediction",
            details=exception.__str__
        )