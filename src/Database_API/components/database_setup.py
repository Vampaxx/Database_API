import os
from dotenv import load_dotenv
from Database_API import logger
from Database_API.constants import * 
from Database_API.utils.common import read_yaml
from Database_API.entity.config_entity import (DatabaseConfig)




class ConfigurationManager:
    def __init__(self,
                 config    = CONFIG_FILE_PATH):

        self.config = read_yaml(config)


    def get_database_config(self) -> DatabaseConfig:
        config      = self.config.Database_config
        logger.info("Model config initialized")
        load_dotenv()
        data_base_config = DatabaseConfig(db_user       = config.db_user,
                                          db_password   = config.db_password,
                                          db_host       = config.db_host,
                                          db_name       = config.db_name)

        return data_base_config
    


if __name__ == "__main__":
    manager = ConfigurationManager()
    database = manager.get_database_config()





