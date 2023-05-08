import csv
import requests
import arcpy
import json
from SpatialEtl import SpatialEtl
import logging


class GSheetsEtl(SpatialEtl):
    """
    ETL class. Extracts, transforms and loads a Google sheet file.
    :param SpatialEtl: SpatialEtl class from the SpatialETL script
    :return:
    """

    # creates a class called GsheetsETL that uses the SpatialEtl class
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def extract(self):
        """
        Writes a csv from a Google sheet containing addresses from a pesticide spraying opt-out form specified in the
        yaml file
        :param:
        :return:
        """
        try:
            # downloads and pulls out the data
            logging.info("Extracting addresses from google form spreadsheet")
            r = requests.get(self.config_dict.get('remote_url'))
            r.encoding = "utf-8"
            data = r.text
            with open(rf"{self.config_dict.get('proj_dir')}addresses.csv", "w") as output_file:
                output_file.write(data)
            logging.debug("Exiting extract function in GsheetsEtl.py")
        except Exception as e:
            print(f"Error in GSheetsEtl extract {e}")

    def transform(self):
        """
        Geocodes the addresses from the opt-out form and writes to a new csv file
        """
        try:
            logging.debug("Starting transform function in GsheetsEtl.py")

            transformed_file = open(f"{self.config_dict.get('proj_dir')}new_addresses.csv", "w")
            transformed_file.write("X,Y,Type\n")
            # opens the file from the extract function, geocodes the data and adds it to a new CSV file
            with open(f"{self.config_dict.get('proj_dir')}addresses.csv", "r") as partial_file:
                csv_dict = csv.DictReader(partial_file, delimiter=',')
                for row in csv_dict:
                    address = row["Street Address"] + " Boulder CO"
                    logging.info(address)
                    geocode_url = self.config_dict.get('geocoder_prefix_url') + address + self.config_dict.get \
                        ('geocoder_suffix_url')
                    logging.info(geocode_url)
                    r = requests.get(geocode_url)

                    resp_dict = r.json()
                    x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                    y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                    transformed_file.write(f"{x},{y},Residential\n")

            transformed_file.close()
            logging.debug("Exiting transform function in GsheetsEtl.py")
        except Exception as t:
            print(f"Error in GsheetsEtl transform {t}")

    def load(self):
        """
        Creates a point feature called "avoid_points" of the addresses that opted-out of spraying
        """
        try:
            logging.debug("Starting load function in GsheetsEtl.py")
            # Set environment settings
            arcpy.env.workspace = (f"{self.config_dict.get('proj_dir')}WestNileOutbreak.gdb")
            arcpy.env.overwriteOutput = True

            # Set the local variables
            in_table = (f"{self.config_dict.get('proj_dir')}new_addresses.csv")
            out_feature_class = "avoid_points"
            x_coords = "X"
            y_coords = "Y"

            # Make the XY event layer...
            arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

            # Logs the total rows
            logging.info(arcpy.GetCount_management(out_feature_class))
            logging.debug("Exiting load function in GsheetsEtl.py")
        except Exception as e:
            print(f"Error in GsheetsEtl load {e}")

    def process(self):
        self.extract()
        self.transform()
        self.load()
