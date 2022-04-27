"""
GIS 305 Final Project (West Nile Virus Outbreak Simulation) ETL definitions header file
Spring 2022
Author: Charles Myers
ArcGIS Pro Python reference: https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm
"""

import logging

class SpatialEtl:

    def __init__(self,config_dict):
        self.config_dict = config_dict

    def extract(self):
        """
        extract data from url
        Params:
        Returns: extracts data from url to program directory
        """
        logging.info (f"Extracting data from {self.config_dict.get('remote_url')}"
                f" to {self.config_dict.get('proj_dir')}")

    def transform(self):
        """
        transform data
        Params:
        Returns:
        """
        logging.info(f"Transforming data from {self.config_dict('format')}")

    def load(self):
        """
        load data
        Params:
        Returns:
        """
        logging.info(f"Loading data to {self.config_dict('project_dir')}")