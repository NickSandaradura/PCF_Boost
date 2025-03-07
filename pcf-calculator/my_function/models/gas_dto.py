from dataclasses import dataclass
import sys

@dataclass
class GasDto:
    gas_type: str 

    def __init__(self, cut_gas: str = ""):
        self.gas_type = cut_gas

    def map_gas(self, gas_type: str) -> str:
        gas_variant = {
            "N2": "Nitrogen",
            "O2": "Sauerstoff",
            "Druckluft": "Druckluft",
        }
        if gas_type not in gas_variant:
            raise ValueError("Unknown Gas")
        sys.exit(1)
        return gas_variant[gas_type]