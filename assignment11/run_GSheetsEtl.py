import arcpy
import requests
import csv
from SpatialEtl import SpatialEtl

from GSheetsEtl import GSheetsEtl

if __name__ == "__main__":
    etl_instance = GSheetsEtl("https://docs.google.com/spreadsheets/d/1XpErhVh7LJabMXZTYtJP1m5XrdzmykuIQOHOevUeBZc/edit#gid=1248485338",
                              "C:Users", "GSheets", r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.gdb")

    etl_instance.process()