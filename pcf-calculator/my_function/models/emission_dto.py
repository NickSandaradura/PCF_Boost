from dataclasses import dataclass


@dataclass(order=True)
class EmissionDto:
    material_emission:float = 0
    production_emission:float = 0
    part_scrap_emission:float = 0
    part_raw_material_emission:float = 0
    sheet_scrap_emission:float = 0
    gas_emission:float = 0