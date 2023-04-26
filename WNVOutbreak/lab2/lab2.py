import arcpy  # import the arcpy library
from etl.GSheetsEtl import GSheetsEtl

# Defining a function that will set our workspace, allow us to overwrite files, and allows us to add outputs to the map
def setup():
    arcpy.env.workspace = r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    arcpy.env.addOutputsToMap = True


def etl():
    print("testing etl")
    etl_instance = GSheetsEtl("https://foo_bar.com", "C:Users", "GSheets",
                              r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.gdb")
    etl_instance.process()

#
# def buffer(layer_name, buff_dist):
#     # Buffer the chosen layer by a set distance
#     output_buffer = f"buff_{layer_name}"
#     print(f"Buffering {layer_name} to generate {output_buffer}")
#     arcpy.analysis.Buffer(layer_name, output_buffer, buff_dist, "FULL", "ROUND", "ALL")
#     # Adds the output to an empty list
#     inter_layer_list.append(output_buffer)
#
#
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
#

if __name__ == '__main__':
    setup()
    etl()

    # buff_layer_list = ["Mosquito_Larval_Sites", "Wetlands", "Lakes_and_Reservoirs", "OSMP_Properties"]
    # inter_layer_list = []
    #
    # try:
    #     # Try and except statement so if the user inputs "ft" instead of "feet" they will get a helpful message
    #     for layer in buff_layer_list:
    #         # Goes through the list of layers that need to be buffered and runs the buffer function on each one
    #         buff_dist = input(f"\nHow far would you like to buffer {layer}\n")
    #         buffer(layer, buff_dist)
    # except:
    #     print("Input invalid\n"
    #           "Please enter your value and full unit name\n"
    #           "Example: 5280 feet or 1 mile")
    #     exit()
    #
    # output_inter = input("\nWhat would you like to name your intersect layer?\n")
    #
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
    # proj_path = r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak"
    # aprx = arcpy.mp.ArcGISProject(rf"{proj_path}\WestNileOutbreak.aprx")
    # map_doc = aprx.listMaps()[0]

    # # Adds the spatial join output to the map
    # map_doc.addDataFromPath(rf"{proj_path}\WestNileOutbreak.gdb\{output_sjoin}")
    #
    # # Saves the project
    # aprx.save()