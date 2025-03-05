from dataclasses import dataclass

@dataclass
class GasDto:
    gas_type: str 

    def __init__(self, cut_gas: str = "N2"):

        self.gas_type = cut_gas

    def map_gas(self, gas_type: str) -> str:
        gas_variant = {
            "N2": "Nitrogen",
            "O2": "Sauerstoff",
            "Druckluft": "Druckluft",
        }
        return gas_variant.get(gas_type, "Unknown Gas")
