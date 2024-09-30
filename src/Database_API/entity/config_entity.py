import os 
from pathlib import Path
from dataclasses import dataclass



@dataclass(frozen=True)
class DatabaseConfig:
    db_user         : str 
    db_password     : str 
    db_host         : str 
    db_name         : str 