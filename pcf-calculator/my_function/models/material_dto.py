from dataclasses import dataclass, field

@dataclass(order=True)
class MaterialDto:
    id: str
    thickness: dict
    foil_type: str
    coating_type: str
    name:str


    def __init__(self, material_id=" ", thickness_value=0, foil_type="NO_FOIL", coating_type="NO_COATING"):
        self.id = material_id
        self.thickness = {"unit": "mm", "value": thickness_value}
        self.foil_type = foil_type
        self.coating_type = coating_type
        self.name = self.map_id_to_name(material_id)
        
    def map_id_to_name(self,id):
        material_id_name = {"AlMg3":"Aluminium", 
        "1.0038":"Stahl","Cu":"Copper", "CuZn":"Messing"}
        return material_id_name[id]
