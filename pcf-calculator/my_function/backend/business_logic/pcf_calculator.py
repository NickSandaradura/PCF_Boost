from my_function.models.part_dto import PartDto
from my_function.backend.interfaces.pcf_calculator_interface import GeoPcfCalculatorInterface, LstPcfCalculatorInterface

class GeoPcfCalculator(GeoPcfCalculatorInterface):

    def __init__(self, part:PartDto):
        self.part = part
    
    def calculate_material_emissions(self,part_weight, sheet_scrap_weight, 
    part_scrap_weight, material_id)->float:
        emission_factor = self.material_emission_factors[material_id]
        self.part.emission.part_raw_material_emission = part_weight * emission_factor
        self.part.emission.part_scrap_emission = part_scrap_weight * emission_factor
        self.part.emission.sheet_scrap_emission = sheet_scrap_weight * emission_factor
        self.part.emission.material_emission = self.part.emission.part_raw_material_emission + self.part.emission.part_scrap_emission + self.part.emission.sheet_scrap_emission
        return self.part.emission.material_emission


    def calc_production_emission(self, cut_gas, gas_consumption, energy_co2_equivalent)->float:
        emission_factor = self.energy_emission_factors[cut_gas]
        self.part.emission.gas_emission = (gas_consumption * emission_factor * 1.17 / 1000)
        self.part.emission.production_emission =  self.part.emission.gas_emission + energy_co2_equivalent
        return self.part.emission.production_emission
          
    def calc_energy_co2_equivalent(self, energy_consumption:float)->float:
        self.part.energy_co2_equivalent=energy_consumption * self.energy_emission_factors["Electricity"]
        return self.part.energy_co2_equivalent
    

    def calc_pcf(self):
        material_emission = self.calculate_material_emissions(self.part.weight, self.part.sheet.scrap_weight,self.part.scrap_weight,self.part.material.id)
        production_emission = self.calc_production_emission(self.part.cut_gas, self.part.gas_consumption, self.part.energy_co2_equivalent)
        self.part.pcf = material_emission + production_emission
        


class LstPcfCalculator(LstPcfCalculatorInterface):
    def __init__(self, lst): 
        self.lst = lst