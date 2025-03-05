from my_function.models.material_dto import MaterialDto
from my_function.models.laser_dto import LaserDto
from my_function.models.emission_dto import EmissionDto
from my_function.models.sheet_dto import SheetDto
from my_function.models.gas_dto import GasDto
from dataclasses import dataclass,field

@dataclass(order=True)
class PartDto:
    material: MaterialDto
    laser: LaserDto
    name: str
    weight:float
    area:float
    scrap_weight: float
    scrap_area: float
    sheet: SheetDto    
    time: float
    cut_gas: GasDto    
    gas_consumption: float
    energy_consumption: float
    energy_co2_equivalent: float = 0
    pcf:float = 0
    emission: EmissionDto = field(default_factory=EmissionDto)

