from abc import ABC, abstractmethod
class PcfCalculatorInterface(ABC):
    material_emission_factors =  {
        "AlMg3": 7.48, 
        "1.0038": 0.55, 
        "Cu": 6.86, 
        "CuZn": 5.69
        }

    energy_emission_factors = {
    "N2": 0.2,
    "Druckluft": 0.01,
    "Electricity": 0.435,
    "O2": 0.55
}

class GeoPcfCalculatorInterface(PcfCalculatorInterface):
    @abstractmethod
    def calculate_material_emissions(self,part_weight:float, sheet_scrap_weight:float, 
    part_scrap_weight:float, material_id:str)->float:
        pass

    @abstractmethod
    def calc_production_emission(self,cut_gas:str, gas_consumption:float, energy_co2_equivalent:float)->float:
        pass
    
    @abstractmethod
    def calc_pcf(self)->None:
        pass

class LstPcfCalculatorInterface(PcfCalculatorInterface):
    pass
    
