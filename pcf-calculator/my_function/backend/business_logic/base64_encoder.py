import os
import base64
from my_function.models.geo_dto import GeoDto 
from my_function.models.lst_dto import LstDto
from concurrent.futures import ThreadPoolExecutor
import copy
from pathlib import Path

class Base64Encoder:
    def __init__(self, directory_path='data'):
        self.directory = directory_path
       
    
    @staticmethod
    def encode_to_base64(file_content:bytes)-> str:
        return base64.b64encode(file_content).decode('utf-8')

    @staticmethod
    def encode_file_to_base64(file_path) -> str:
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error encoding file: {file_path}") from e
     
    def encode_geo_file_to_base64(self, file_name: str, geo_dto:GeoDto):
        file_path = os.path.join(self.directory, file_name)
        encoded_string = Base64Encoder.encode_file_to_base64(file_path)
        geo_dto.name = file_name
        geo_dto.geometry["content_base64"] = encoded_string
        return geo_dto
    
    def encode_lst_file_to_base64(self, file_name)->LstDto:
        file_path = os.path.join(self.directory, file_name)
        encoded_string = Base64Encoder.encode_file_to_base64(file_path)
        lst_file = LstDto(file_name,encoded_string)
        return lst_file
    
    
    def encode_geo_files_to_base64(self, geo_dto:GeoDto) -> list[GeoDto]:
        geo_files = [file.name for file in Path(self.directory).glob("*.GEO")]    
        geo_dto_list : list[GeoDto]  = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(lambda file_name: self.encode_geo_file_to_base64(file_name, copy.deepcopy(geo_dto)), geo_files)
            geo_dto_list.extend(results)
        return geo_dto_list
