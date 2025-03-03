from dotenv import load_dotenv
import os
import json
import requests
from my_function.models.part_dto import PartDto
from my_function.backend.exceptions.nash_exceptions import NashApiRequestException
from my_function.backend.business_logic.pcf_calculator import GeoPcfCalculator
from my_function.backend.interfaces.request_service_interface import NashRequestServiceInterface
load_dotenv()

class NashRequestService(NashRequestServiceInterface):
    def __init__(self) -> None:
        self.current_directory = os.path.dirname(__file__)
        self.url = "https://api-staging.trace-electricity.com/api"
        self.cert_directory = os.path.abspath(os.path.join(self.current_directory, '..', 'certificates'))
        self.full_cert_path = os.path.join(self.cert_directory, "CA-TRUMPF-ROOT-01.crt")
        self.api_key = os.environ["NASH_API_KEY"]
        

    def _build_data_payload(self, payload: PartDto):
        return {
            "zone": "DE-LU",
            "emissionFactor": 1,
            "calculationMethod": 1,
            "organizationInput": {
                "load": payload.energy_consumption,
                "pvSelfProduction": 0,
                "windSelfProduction": 0
            }
        }
    
    def _build_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }
    

    def post_energy_request(self, payload: PartDto):
        pcf_calculator = GeoPcfCalculator(payload)
        headers = self._build_headers()
        data = self._build_data_payload(payload)

        try:
            if os.environ.get("PROXY") != None:
                response = requests.post(
                    f"{self.url}/carbon-intensity/now",
                    headers=headers,
                    data=json.dumps(data),
                    proxies={"https": os.environ["PROXY"]},
                    verify=self.full_cert_path
                )
            else:
                response = requests.post(
                    f"{self.url}/carbon-intensity/now",
                    headers=headers,
                    data=json.dumps(data),
                    verify = True
                )
            response.raise_for_status() 

            json_data = response.json()
            payload.energy_co2_equivalent = self._process_response(json_data, payload, pcf_calculator)
        
        except requests.RequestException:
            self._handle_error(pcf_calculator,payload)


    def _process_response(self, json_data, payload:PartDto, pcf_calculator:GeoPcfCalculator):
        pcf_calculator = GeoPcfCalculator(payload)
        if "organizationCarbonFootprint" in json_data and json_data["organizationCarbonFootprint"] is not None:
            return json_data["organizationCarbonFootprint"]
        else:
            self._handle_error(pcf_calculator,payload)


    def _handle_error(self, pcf_calculator:GeoPcfCalculator,payload:PartDto):
        pcf_calculator.calc_energy_co2_equivalent(payload.energy_consumption)
        pcf_calculator.calc_pcf()
        raise NashApiRequestException(f"Request error: switching to manual calculation")