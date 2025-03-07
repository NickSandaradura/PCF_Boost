from dataclasses import dataclass, field
from my_function.models.material_dto import MaterialDto
from my_function.models.laser_dto import LaserDto
from my_function.models.gas_dto import GasDto

@dataclass(order=True)
class GeoDto:
    name : str
    machine_definition :  LaserDto
    material : MaterialDto
    cut_gas : GasDto
    # Check wheater the values for Gasdto are the right one or if there is a need of 
    #adjusting the params for an propper calculation
    geometry : dict 
    laser_cutting_options : dict 


    def __init__(self, name, machine_definition, material, cut_gas, content_base64 = ""):
        self.name = name
        self.machine_definition = machine_definition
        self.material = material
        self.cut_gas = cut_gas
        self.geometry = {"content_type": "GEO", "content_base64": content_base64}
        self.laser_cutting_options = {"cool_line": False, 
        "fly_line": False,"bright_line":False,"performance_package":False,"high_speed": False,
        "high_speed_eco":False,"high_focus_cutting": False,"bevel_cut": False}



    