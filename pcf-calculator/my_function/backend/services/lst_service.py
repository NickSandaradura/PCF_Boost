import requests
from my_function.backend.exceptions.lst_exception import LstParserApiRequestException
import json
import os
from my_function.backend.interfaces.request_service_interface import LstRequestServiceInterface
class LstRequestService(LstRequestServiceInterface):
    def __init__(self) -> None:
        self.url = "https://autonomousmachine.api.trumpf.com/lab/service/api"
        self.data_path = "/tmp/data"
    
    def parse_geo_file(self,geo_filename,file_path):
        files = [('', (geo_filename, open(os.path.join(self.data_path, geo_filename), 'rb'), 'application/octet-stream'))]
        try:
            if os.environ.get("PROXY") != None:
                response = requests.post(f"{self.url}/lst/utils/export", headers={}, files=files, data={},proxies={"https": os.environ["PROXY"]}) 
                response.raise_for_status()
                geo_json = json.loads(response.text) 
                return geo_json
            else:
                response = requests.post(f"{self.url}/lst/utils/export", headers={}, files=files, data={})
                response.raise_for_status()
                geo_json = json.loads(response.text) 
                return geo_json
        except requests.RequestException as e:
            self._handle_error(e,file_path)

    def _handle_error(self,file_path,exception:requests.RequestException):
        os.remove(file_path)
        raise LstParserApiRequestException(f"Request error: {exception}, .GEO could not be parsed to json", exception.response.status_code if exception.response else None)