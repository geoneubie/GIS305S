"""
GIS 305 Final Project (West Nile Virus Outbreak Simulation)
Spring 2022
Author: Charles Myers
ArcGIS Pro Python reference: https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm
"""

# import libraries
import arcpy
import yaml
import requests
import logging
from etl.GSheetsEtl import GSheetsEtl

# setup logger
log = logging.getLogger(__name__)


def setup():
    """
    Setup config dict and logger.
    Params: yaml
    Returns: config_dict
    """
    try:
        with open('wnvoutbreak.yaml') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)

            logging.basicConfig(filename=f"{config_dict.get('proj_dir')}wnv.log",
                                filemode="w", level=logging.DEBUG)
        return config_dict

    except Exception as e:
        log.debug(f"error in setup {e}")


"""
Setup arc workspace, variables, logger, using config_dict.
Params: config_dict
Returns: usable variables for program
"""
# setup workspace and config dict
global config_dict
config_dict = setup()
log.info(config_dict)

arcpy.env.workspace = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\\"
arcpy.env.overwriteOutput = True

# define layers
address = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Addresses"
lakes = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Lakes_Reservoirs"
mosquito = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Mosquito_Larva"
osmp = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\OSMP_Properties"
wetlands = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Wetlands"
avoid = rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Avoid_Points"


def etl():
    """
    Setup etl.
    Params: config_dict
    Returns: Extracted data transformed and usable in program
    """
    try:
        log.info('ETLing')
        etl_instance = GSheetsEtl(config_dict)
        etl_instance.process()
        log.debug('ETL complete')

    except Exception as e:
        log.debug(f"error in etl {e}")

def buffer(buf_lyr):
    """
    Setup buffer for input layers
    Params: buf_lyr
    Returns: buf_out_name
    """
    try:
        log.info('Buffering')
        buf_out_name = input("What is the name of the buffer output for the " + buf_lyr + " layer?")
        buf_dist_input = input("What is the buffer distance in feet?")
        buf_dist = buf_dist_input + " feet"

        # buffer analysis
        result = arcpy.Buffer_analysis(buf_lyr, buf_out_name, buf_dist,"FULL","ROUND","ALL")
        log.debug('Buffer complete')
        return buf_out_name

    except Exception as e:
        log.debug(f"error in buffer {e}")


def intersect(int_lyrs):
    """
    Setup intersect of buffer outputs.
    Params: int_lyrs
    Returns: lyr_name
    """
    try:
        log.info('Intersecting')
        # ask user to name output layer
        lyr_name = input("What is the desired name of the output intersect layer?")

        # run intersect operation on input layer
        arcpy.Intersect_analysis(int_lyrs, lyr_name)

        log.debug('Intersect complete')
        # return resulting output layer
        return lyr_name

    except Exception as e:
        log.debug(f"error in intersect {e}")

def exportMap(aprx):
    """
    Setup export map to pdf
    Params: aprx
    Returns:
    """
    try:
        log.debug('Starting to export map')
        subtitle = input("Enter map subtitle:")

        lyt = aprx.listLayouts()[0]
        for el in lyt.listElements():
            if 'Title' in el.name:
                el.text = el.text + subtitle

        export_name = input("Enter exported layout name:")
        lyt.exportToPDF(rf"{config_dict.get('proj_dir')}\{export_name}.pdf")
        log.debug('Export complete')
        return

    except Exception as e:
        log.debug(f"error in exportMap {e}")


def erase(output_lyr_name):
    """
    Setup erase of intersected buf layers and avoid points buff
    Params: aprx
    Returns:
    """
    try:
        log.info('Erase')
        update_layer = arcpy.Buffer_analysis(avoid, "avoid_buf", "1500 feet", "FULL", "ROUND", "ALL")
        spray_areas = arcpy.Erase_analysis(output_lyr_name, update_layer, "Final_analysis")
        new_at_risk = arcpy.SelectLayerByLocation_management(address, 'INTERSECT', spray_areas)
        result2 = arcpy.GetCount_management(new_at_risk)
        log.info("There are " + result2[0] + " homes in the danger area after removing no spray zones.")
        log.debug('Erase complete')
        return spray_areas

    except Exception as e:
        log.debug(f"error in erase {e}")



def main():
    """
    uses multiple functions to complete a west nile simulation based off of user inputs and exports a pdf.
    Params: etl,buffer,intersect,export,erase,spatial
    Returns: exports a pdf
    """
    log.info('Starting West Nile Virus Simulation')

    # Define variables
    int_lyrs = []
    buf_lyrs = [lakes, mosquito, wetlands, osmp]

    # Call buffer
    try:
        for lyr in buf_lyrs:
            out_buf_name=buffer(lyr)
            int_lyrs.append(out_buf_name)
    except Exception as e:
        log.debug(f"error in main calling buffer {e}")

    # Call Intersect
    try:
        output_lyr_name = intersect(int_lyrs)
    except Exception as e:
        log.debug(f"error in main calling intersect{e}")

    # erase
    try:
        spray_areas = erase(output_lyr_name)
    except Exception as e:
        log.debug(f"error in main calling erase {e}")

    # spatial join for definition query
    try:
        log.info('Spatial Join for definition query')
        arcpy.analysis.SpatialJoin(address, spray_areas, "Target_Addresses")
        log.debug('Spatial join for definition query complete')
    except Exception as e:
        log.debug(f"error in main preforming spatial join {e}")

    # add results to map
    try:
        log.info('adding results to map')
        aprx = arcpy.mp.ArcGISProject(f"{config_dict.get('proj_dir')}\WestNileOutbreak.aprx")
        map_doc = aprx.listMaps()[0]

        log.info('adding final analysis symbology')
        map_doc.addDataFromPath(rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Final_analysis")
        sym_lyr = map_doc.listLayers("Final_Analysis")[0]
        sym = sym_lyr.symbology
        sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
        sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
        sym_lyr.symbology = sym
        sym_lyr.transparency = 50

        map_doc.addDataFromPath(rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\Target_Addresses")

        log.info('adding target addresses definition query')
        lyr = map_doc.listLayers("Target_Addresses")[0]
        lyr.definitionQuery = "Join_Count = 1"

        log.info('setting spatial reference')
        # https://www.spatialreference.org/ref/epsg/2231/
        nad_1983 = arcpy.SpatialReference(2231)
        map_doc.spatialReference = nad_1983

        log.debug('Adding results complete')

        exportMap(aprx)
    except Exception as e:
        log.debug(f"error in main mapping {e}")

    log.debug('WNV Simulation complete')


if __name__ == '__main__':
    """
   Order to run
    """
    etl()
    main()
