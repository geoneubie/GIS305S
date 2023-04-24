import arcpy
import requests
import csv

from GSheetsEtl import GSheetsEtl

if __name__ == "__main__":
    etl_instance = GSheetsEtl("https://foo_bar.com", "C:Users", "GSheets", "C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.gdb")

    etl_instance.process()