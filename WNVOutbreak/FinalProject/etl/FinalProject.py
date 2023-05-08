"""
Project Name: West Nile Outbreak Final Project.
Project Purpose: To create a final map that shows what areas in Boulder, CO need to be sprayed with pesticides to avoid
West Nile virus outbreaks.
Author: Heather Vinson
Date: 05/07/2023
"""
import yaml
import arcpy  # import the arcpy library
from GSheetsEtl import GSheetsEtl  # import the ETL functions created
import logging
import csv


import sys


def setup():
    """
    Open and load in the yaml file, so it can be referenced as config_dict
    :param:
    :return config_dict: The variable that references the yaml file
    """
    try:
        # open and load in the yaml file
        with open('config/wnvoutbreak.yaml') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
        # Use logging to create a file that prints statements based on the level
        logging.basicConfig(level=logging.DEBUG,
                            format="%(name)s - "
                                   "%(levelname)s - "
                                   "%(message)s",
                            handlers=[logging.FileHandler(f"{config_dict.get('proj_dir')}wnv.log")])
                            # , logging.StreamHandler(sys.stdout)])
                            # Remove pound sign above and ]) at the end of ...wnv.log") to have logging messages to print
                            # to console as well
        logging.debug("Exiting the setup function")
        return config_dict
    except Exception as s:
        print(f"Error in setup {s}")



def etl():
    """
    Runs the ETL file, Gsheets ETL to download, geocode, and load addresses that have opted out of pesticide spraying
    :param:
    :return:
    """
    try:
        # running the GsheetsElt script with the yaml file as an input
        logging.debug("Running ELT process.")
        etl_instance = GSheetsEtl(config_dict)
        etl_instance.process()
        logging.debug("Exiting Etl function")
    except Exception as e:
        print(f"Error in etl {e}")


def buffer(layer_name, buff_dist):
    """
    Creates a buffer polygon around a given layer at a specified distance in feet
    :param layer_name: Layer to be buffered
    :param buff_dist: Distance in feet to buffer the layer
    :return:
    """
    try:
        logging.debug("Running Buffer function")
        # Buffer the chosen layer by a set distance
        units = "feet"
        output_buffer = f"buff_{layer_name}"
        logging.info(f"Buffering {layer_name} to generate {output_buffer}")
        arcpy.Buffer_analysis(layer_name, output_buffer, f"{buff_dist} {units}", "FULL", "ROUND", "ALL")
        logging.debug("Exiting Buffer function")
    except Exception as b:
        print(f"Error in buffer {b}")


def intersect(inter_layer_list):
    """
    Creates a polygon everywhere that given layers overlap
    :param inter_layer_list: Layers to find where they overlap
    :return output_inter: the polygon layer that just has where the layers overlap
    """
    try:
        logging.debug("Starting intersect function")
        # Find where the buffers intersect
        output_inter = input("\nWhat would you like to name your intersect layer?\n")
        arcpy.analysis.Intersect(inter_layer_list, output_inter)
        logging.debug("Exiting intersect function")
        return output_inter
    except Exception as i:
        print(f"Error in intersect {i}")


def sym_diff(lyr_inter):
    """
    Removes the geometry of the buffered avoid points from another polygon
    :param lyr_inter: The polygon layer that will have areas removed from it
    :return out_sym_diff: The name of the polygon layer
    """
    try:
        logging.debug("Starting Symmetric Difference function")
        # removing the areas that have opted out of being sprayed
        out_sym_diff = input("What would you like to name the new intersect layer that is missing the opt-out areas?\n")
        arcpy.analysis.SymDiff(lyr_inter, "buff_avoid_points", out_sym_diff)
        logging.debug("Exiting Symmetric Difference function")
        return out_sym_diff
    except Exception as d:
        print(f"Error in sym_diff {d}")


def spatial_join(out_sym_diff):
    """
    This preforms a spatial join on the Addresses point layer and the parameter intersect layer
    This creates a copy of the Addresses point layer with an additional attribute called Join_Count.
    If Join_count is equal to 1 then it falls in the intersect layer, if it is 0 then it does not.
    :param lyr_inter: The intersect layer to be joined with addresses
    :return output_sjoin: Name of output point layer
    """
    try:
        logging.debug("Starting spatial join function")
        # finding the addresses that fall within the buffer intersection
        output_sjoin = input("\nWhat would you like to name your spatial join layer?\n")
        logging.info(f"Finding address that fall in the area of concern.")
        arcpy.analysis.SpatialJoin("Addresses", out_sym_diff, output_sjoin)
        logging.debug("Exiting spatial join function")
        return output_sjoin
    except Exception as j:
        print(f"Error in spatial_join {j}")


def exportMap():
    """
    Adds a subtitle to the Layout and prints the layout as a pdf
    :param:
    :return:
    """
    try:
        logging.debug("Starting export map function")
        # create a variable that is equal to the layout
        aprx = arcpy.mp.ArcGISProject(rf"{config_dict.get('proj_dir')}WestNileOutbreak.aprx")
        lyt = aprx.listLayouts()[0]

        # Add a subtitle after the element "Title"
        subtitle = input("Please enter a subtitle for the output map.\n")
        for el in lyt.listElements():
            logging.info(el.name)
            if "Title" in el.name:
                el.text = el.text + subtitle
        # export the layout to a pdf
        lyt.exportToPDF(rf"{config_dict.get('proj_dir')}WestNileOutbreak{subtitle}.pdf")
        logging.info(rf"Created a pdf of your map namedWestNileOutbreak{subtitle}.pdf located {config_dict.get('proj_dir')}")
        logging.debug("Exiting export map function")
    except Exception as e:
        print(f"Error in export_map {e}")


def main():
    """
    Adds four layers to the map and symbolize them.
    Calls the functions to buffer four specified layers, find where the buffers intersect, buffers the avoid points,
    removes the avoid points buffer from the intersect layer and adds the symbolized layer to the map,
    joins te addresses to new intersect layer and adds the address points that fall within the intersect layer to the
    map, and counts how many addresses fall in the new intersect layer.
    :param:
    :return:
    """
    try:
        logging.info('Starting West Nile Virus Simulation main')

        # Setting a variable equal to the geodatabase, aprx, and the map document
        geodb = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
        aprx = arcpy.mp.ArcGISProject(rf"{config_dict.get('proj_dir')}WestNileOutbreak.aprx")
        map_doc = aprx.listMaps()[0]

        sp_co_north = arcpy.SpatialReference(102653)
        map_doc.spatialReference = sp_co_north

        # Maplyers is an empty list that will be appended with layer names as they are added to the map document
        maplyrs = []
        # created a list of the layers to be buffered
        buff_layer_list = ["OSMP_Properties", "Lakes_and_Reservoirs", "Wetlands", "Mosquito_Larval_Sites"]

        # for loop adds the layers to be buffered to the map and then saves the project
        for layer in buff_layer_list:
            map_doc.addDataFromPath(rf"{geodb}\{layer}")
            maplyrs.append(layer)

        # Set the symbology for OSMP_Properties, Lakes_and_Reservoirs, Wetlands, and Mosquito_Larval_Sites layers
        # Symbology for Mosquito_Larval_Sites
        mos_lar_site_lyr = map_doc.listLayers("Mosquito_Larval_Sites")[0]
        mos_lar_site_sym = mos_lar_site_lyr.symbology
        mos_lar_site_sym.renderer.symbol.color = {'RGB': [255, 255, 115, 100]}
        mos_lar_site_sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
        mos_lar_site_lyr.symbology = mos_lar_site_sym

        # Symbology for Lakes_and_Reservoirs
        lake_lyr = map_doc.listLayers("Lakes_and_Reservoirs")[0]
        lake_sym = lake_lyr.symbology
        lake_sym.renderer.symbol.color = {'RGB': [0, 169, 230, 100]}
        lake_sym.renderer.symbol.outlineColor = {'RGB': [0, 113, 245, 100]}
        lake_lyr.symbology = lake_sym

        # Symbology for OSMP_Properties
        osm_lyr = map_doc.listLayers("OSMP_Properties")[0]
        osm_sym = osm_lyr.symbology
        osm_sym.renderer.symbol.color = {'RGB': [0, 115, 76, 100]}
        osm_sym.renderer.symbol.outlineColor = {'RGB': [204, 204, 204, 100]}
        osm_lyr.symbology = osm_sym

        # Symbology for Wetlands
        wetlands_lyr = map_doc.listLayers("Wetlands")[0]
        wetlands_sym = wetlands_lyr.symbology
        wetlands_sym.renderer.symbol.color = {'RGB': [211, 255, 190, 100]}
        wetlands_sym.renderer.symbol.outlineColor = {'RGB': [204, 204, 204, 100]}
        wetlands_lyr.symbology = wetlands_sym

        aprx.save()

        for layer in buff_layer_list:
            # Goes through the list of layers that need to be buffered and runs the buffer function on each one
            buff_dist = input(f"\nHow far would you like to buffer {layer}(in feet)?\n")
            buffer(layer, buff_dist)

        # a list of the output layers after being buffered
        inter_layer_list = ["buff_Mosquito_Larval_Sites", "buff_Wetlands", "buff_Lakes_and_Reservoirs",
                            "buff_OSMP_Properties"]

        # assigns the return form the intersect function to the variable lyr_inter and runs the function
        lyr_inter = intersect(inter_layer_list)
        logging.info(f"Creating a layer named {lyr_inter} that shows where the layers:\n{inter_layer_list} intersect.")

        # Asks for input on how far to buffer the avoid points
        avoid_buff_dist = input("There are some addresses that have opted-out of pesticide spraying.\n"
                                "How many feet would you like to avoid spraying around these addresses?\n")
        avoid_points = "avoid_points"
        # Runs the buffer function on the avoid points, so we have a polygon to use in the sym_diff function
        buffer(avoid_points, avoid_buff_dist)
        # Removes the buffered avoid points from the intersect layer created earlier and creates a variable out of the
        # returned output
        lyr_sym_diff = sym_diff(lyr_inter)
        logging.info(f"Removing opt-out areas to create a new layer named {lyr_sym_diff}")
        # Adds intersect layer that does not include the avoid points buffer to map and maplrys list then saves project
        map_doc.addDataFromPath(rf"{geodb}\{lyr_sym_diff}")
        maplyrs.append(lyr_sym_diff)

        # Symbolizes the new intersect layer
        final_inter_lyr = map_doc.listLayers(lyr_sym_diff)[0]
        final_inter_sym = final_inter_lyr.symbology
        final_inter_sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
        final_inter_sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
        final_inter_lyr.symbology = final_inter_sym
        final_inter_lyr.transparency = 50

        aprx.save()

        # Runs the spatial join function on the output from the sym_diff function
        lyr_sjoin = spatial_join(lyr_sym_diff)

        # Adds the addresses with Join_Count attribute to the map
        map_doc.addDataFromPath(rf"{geodb}\{lyr_sjoin}")
        maplyrs.append(lyr_sjoin)

        # Filters out all the addresses except the ones with 1 in our Join_Count attribute
        sjoin_lyr = map_doc.listLayers(lyr_sjoin)[0]
        sjoin_lyr.definitionQuery = "Join_Count = 1"

        addAOCCount = 0
        with arcpy.da.SearchCursor(lyr_sjoin, ["Join_Count"]) as joinCursor:
            for x in joinCursor:
                # Creating a search cursor and iteration through the attributes in the Join_Count field
                if x[0] == 1:
                    # If statement add 1 to a variable set to 0, so it can count each instance that 1 shows up
                    addAOCCount = addAOCCount + 1
        logging.info(f"There are {addAOCCount} addresses in the area of concern.")

        aprx.save()

        logging.debug("Exiting West Nile Virus Simulation main")
    except Exception as m:
        print(f"Error in setup {m}")

if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    main()
    exportMap()
