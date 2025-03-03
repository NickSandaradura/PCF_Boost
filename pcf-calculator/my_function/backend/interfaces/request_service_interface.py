from abc import ABC, abstractmethod
from my_function.models.geo_dto import GeoDto
from my_function.models.part_dto import PartDto
from my_function.backend.business_logic.pcf_calculator import GeoPcfCalculator 
class RequestServiceInterface(ABC):
    msg = ""


class RequestServiceBearerAuthInterface(RequestServiceInterface):
    access_token = None
    token_expiration = None
    @abstractmethod
    def _request_access_token(self):
        pass


class NashRequestServiceInterface(RequestServiceInterface):
    @abstractmethod
    def post_energy_request(self, payload:PartDto):
        pass

    @abstractmethod
    def _process_response(self, json_data, payload, pcf_calculator):
        pass

    @abstractmethod
    def _handle_error(self, pcf_calculator:GeoPcfCalculator,payload:PartDto):
        pass
       
class RpRequestServiceInterface(RequestServiceBearerAuthInterface):
    @abstractmethod
    def post_geo_request(self, payload:GeoDto):
        pass

    @abstractmethod
    def _process_post_geo_response(self,data, geo_dto):
        pass

    @abstractmethod
    def _handle_error(self,exception):
        pass

class LstRequestServiceInterface(RequestServiceInterface):
    
    @abstractmethod
    def _handle_error(self,file_path,exception):
        pass