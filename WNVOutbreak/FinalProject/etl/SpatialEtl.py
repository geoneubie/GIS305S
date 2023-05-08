import yaml
import requests
import logging
class SpatialEtl:
    """
    Logs what data is being processed in GsheetsEtl and where it is going.
    """

    def __init__(self, config_dict):
        try:
            self.config_dict = config_dict
        except Exception as e:
            print(f"Error in SpatialEtl init {e}")

    def extract(self):
        try:
            logging.info(f"Extracting data from {self.config_dict.get('remote_url')} to {self.config_dict.get('proj_dir')}")
        except Exception as e:
            print(f"Error in SpatialEtl extract {e}")

    def transform(self):
        try:
            logging.info(f"Transforming {self.config_dict.get('data_format')}")
        except Exception as e:
            print(f"Error in SpatialEtl transform {e}")

    def load(self):
        try:
            logging.info(f"Loading data into {self.config_dict.get('proj_dir')}")
        except Exception as e:
            print(f"Error in SpatialEtl load {e}")







