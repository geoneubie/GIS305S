import yaml
import arcpy  # import the arcpy library
from GSheetsEtl import GSheetsEtl



def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict


def etl():
    print("etl test")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

# Defining a function that will set our workspace, allow us to overwrite files, and allows us to add outputs to the map
# def setup():
#     arcpy.env.workspace = rf"{config_dict.get('proj_dir')}arcgis\WestNileOutBreak\WestNileOutbreak.gdb"
#     arcpy.env.overwriteOutput = True
#     arcpy.env.addOutputsToMap = True


def buffer(layer_name, buff_dist):
    # Buffer the chosen layer by a set distance
    units = "miles"
    output_buffer = f"buff_{layer_name}"
    print(f"Buffering {layer_name} to generate {output_buffer}")
    arcpy.analysis.Buffer(layer_name, output_buffer, f"{buff_dist} {units}", "FULL", "ROUND", "ALL")
    # Adds the output to an empty list
    inter_layer_list.append(output_buffer)


# def intersect(output_inter):
#     # Find where the buffers intersect
#     print(f"Creating a layer named {output_inter} that shows where the layers:\n{inter_layer_list} intersect.")
#     arcpy.analysis.Intersect(inter_layer_list, output_inter)
#
#
# def spatial_join(output_sjoin):
#     # finding the addresses that fall within the buffer intersection
#     print(f"Finding address that fall in the area of concern.")
#     arcpy.analysis.SpatialJoin("Addresses", output_inter, output_sjoin)


def main():
    buff_layer_list = ["Mosquito_Larval_Sites", "Wetlands", "Lakes_and_Reservoirs", "OSMP_Properties"]
    inter_layer_list = []


    # Try and except statement so if the user inputs "ft" instead of "feet" they will get a helpful message
    for layer in buff_layer_list:
        # Goes through the list of layers that need to be buffered and runs the buffer function on each one
        buff_dist = input(f"\nHow far would you like to buffer {layer}\n")
        buffer(layer, buff_dist)


    output_inter = input("\nWhat would you like to name your intersect layer?\n")

    # intersect(output_inter)
    #
    # output_sjoin = input("\nWhat would you like to name your spatial join layer?\n")
    # spatial_join(output_sjoin)
    #
    # addAOCCount = 0
    #
    # with arcpy.da.SearchCursor(output_sjoin, ["Join_Count"]) as joinCursor:
    #     for x in joinCursor:
    #         # Creating a search cursor and iteration through the attributes in the Join_Count field
    #         if x[0] == 1:
    #             # If statement add 1 to a variable set to 0, so it can count each instance that 1 shows up
    #             addAOCCount = addAOCCount + 1
    #
    # print(f"There are {addAOCCount} addresses in the area of conern.")
    #
    # #proj_path = r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak"
    # aprx = arcpy.mp.ArcGISProject(f"{config_dict.get('proj_dir')}arcgis\westnileoutbreak\WestNileOutbreak.aprx")
    # map_doc = aprx.listMaps()[0]
    #
    # # Adds the spatial join output to the map
    # map_doc.addDataFromPath(rf"{config_dict.get('proj_dir')}arcgis\westnileoutbreakWestNileOutbreak.gdb\{output_sjoin}")
    #
    # # Saves the project
    # aprx.save()


if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    # intersect()
    # spatial_join()
