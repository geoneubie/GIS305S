import requests
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
    units = "feet"
    output_buffer = f"buff_{layer_name}"
    print(f"Buffering {layer_name} to generate {output_buffer}")
    arcpy.Buffer_analysis(layer_name, output_buffer, f"{buff_dist} {units}", "FULL", "ROUND", "ALL")


def intersect(inter_layer_list):
    # Find where the buffers intersect
    output_inter = input("\nWhat would you like to name your intersect layer?\n")

    arcpy.analysis.Intersect(inter_layer_list, output_inter)
    return output_inter


def spatial_join(lyr_inter):
    # finding the addresses that fall within the buffer intersection
    output_sjoin = input("\nWhat would you like to name your spatial join layer?\n")
    print(f"Finding address that fall in the area of concern.")
    arcpy.analysis.SpatialJoin("Addresses", lyr_inter, output_sjoin)
    return output_sjoin


def sym_diff(lyr_inter):
    out_sym_diff = input("What would you like to name the new intersect layer that is missing the opt-out areas?\n")
    arcpy.analysis.SymDiff(lyr_inter, "buff_avoid_points", out_sym_diff)
    return out_sym_diff


def main():
    buff_layer_list = ["Mosquito_Larval_Sites", "Wetlands", "Lakes_and_Reservoirs", "OSMP_Properties"]

    for layer in buff_layer_list:
        # Goes through the list of layers that need to be buffered and runs the buffer function on each one
        buff_dist = input(f"\nHow far would you like to buffer {layer}\n")
        buffer(layer, buff_dist)

    inter_layer_list = ["buff_Mosquito_Larval_Sites", "buff_Wetlands", "buff_Lakes_and_Reservoirs",
                        "buff_OSMP_Properties"]

    lyr_inter = intersect(inter_layer_list)
    print(f"Creating a layer named {lyr_inter} that shows where the layers:\n{inter_layer_list} intersect.")

    avoid_buff_dist = input("There are some addresses that have opted-out of pesticide spraying.\n"
                            "How many feet would you like to avoid spraying around these addresses?\n")

    avoid_points = "avoid_points"

    buffer(avoid_points, avoid_buff_dist)

    lyr_sym_diff = sym_diff(lyr_inter)

    print(f"Removing opt-out areas to create a new layer named {lyr_sym_diff}")

    proj_path = f"{config_dict.get('proj_dir')}arcgis\westnileoutbreak\WestNileOutbreak.gdb"
    # "C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.aprx"
    aprx = arcpy.mp.ArcGISProject(rf"{config_dict.get('proj_dir')}arcgis\westnileoutbreak\WestNileOutbreak.aprx")
    map_doc = aprx.listMaps()[0]

    # Adds the spatial join output to the map
    map_doc.addDataFromPath(rf"{proj_path}\{lyr_sym_diff}")

    # Saves the project
    aprx.save()

    lyr_sjoin = spatial_join(lyr_sym_diff)

    addAOCCount = 0

    with arcpy.da.SearchCursor(lyr_sjoin, ["Join_Count"]) as joinCursor:
        for x in joinCursor:
            # Creating a search cursor and iteration through the attributes in the Join_Count field
            if x[0] == 1:
                # If statement add 1 to a variable set to 0, so it can count each instance that 1 shows up
                addAOCCount = addAOCCount + 1

    print(f"There are {addAOCCount} addresses in the area of concern.")

    aprx.save()


if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    main()
