from dataclasses import dataclass
@dataclass(order=True)
class LstDto:
    name:str
    content_base64:str
    