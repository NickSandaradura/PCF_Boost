from dataclasses import dataclass

@dataclass(order=True)
class LaserDto:
    machine_type_identifier : str
    laser_power : dict[str,int]
    laser_type : str 
    laser_head_type : int 
    software_version : str

    
    def __init__(self,machine_type_identifier,watt=8000,laser_type = "DK",laser_head_type = 12,software_version= "2.1.32.3"):
        self.machine_type_identifier = machine_type_identifier
        self.laser_power = {"unit":"W","value":watt}
        self.laser_type = laser_type
        self.laser_head_type = laser_head_type
        self.software_version = software_version
    
