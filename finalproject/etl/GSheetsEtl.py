"""
GIS 305 Final Project (West Nile Virus Outbreak Simulation) GSheets Header file
Performs extract, transform, load process using a google spreadsheet URL.
The Spreadsheet must contain address and zipcode columns.

params: config_dict (dictionary containing paths to url, geocoding, files)
"""
import requests
import arcpy
import csv
import logging

from etl.SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    """
    Performs extract, transform, load process using a google spreadsheet URL.
    The Spreadsheet must contain address and zipcode columns.
    Params: config_dict (dictionary containing paths to url, geocoding, files)
    Returns: extracts data from url to program directory
    """
    config_dict = None

    def __init__(self,config_dict):
        self.config_dict = config_dict


    def extract(self):
        """
        extract data from gsheet
        Params: gsheet url
        Returns: gsheet as downloaded csv
        """
        logging.info("Extracting addresses from google form spreadsheet")
        r = requests.get(self.config_dict.get('remote_url'))
        r.encoding = "utf-8"
        data = r.text
        with open(rf"{self.config_dict.get('proj_dir')}\address.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        """
        transform data from gsheet
        Params: downloaded csv
        Returns: csv addresses as geocoded addresses with x,y locations
        """
        logging.info("Add City, State")

        transformed_file = open(f"{self.config_dict.get('proj_dir')}new_addresses.csv", "w")
        transformed_file.write("X,Y,Type\n")
        with open(rf"{self.config_dict.get('proj_dir')}\address.csv", "r") as partial_file:
            csv_dict = csv.DictReader(partial_file, delimiter=",")
            for row in csv_dict:
                address = row['Street Address'] + " Boulder CO"
                logging.info(address)
                geocode_url = f"{self.config_dict.get('geocoder_prefix_url')}{address}{self.config_dict.get('geocoder_suffix_url')}"
                r = requests.get(geocode_url)
                r.encoding = "utf-8"

                resp_dict = r.json()
                x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                transformed_file.write(f"{x},{y},Residential\n")
        transformed_file.close()

    def load(self):
        """
        load data from transformed data
        Params: transformed csv
        Returns: addresses as point locations in arc
        """
        arcpy.env.workspace = rf"{self.config_dict.get('proj_dir')}\WestNileOutbreak.gdb\\"
        arcpy.env.overwriteOutput = True

        # local variables
        in_table = f"{self.config_dict.get('proj_dir')}new_addresses.csv"
        out_feature_class = "Avoid_Points"
        x_coords = "X"
        y_coords = "Y"

        # XY event layer
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

        # print total rows
        logging.info(arcpy.GetCount_management(out_feature_class))

    def process(self):
        """
        process the order to perform steps
        Params:
        Returns:
        """
        self.extract()
        self.transform()
        self.load()