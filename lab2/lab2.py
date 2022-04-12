import arcpy
import yaml
import requests
from etl.GSheetsEtl import GSheetsEtl

def setup():
    with open('wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict

global config_dict
config_dict = setup()
print(config_dict)

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
    print ("etling...")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

# Define Buffer
def buffer(buf_lyr):

    buf_out_name = input("What is the name of the buffer output for the " + buf_lyr + " layer?")
    buf_dist_input = input("What is the buffer distance in feet?")
    buf_dist = buf_dist_input + " feet"

    # buffer analysis
    result = arcpy.Buffer_analysis(buf_lyr, buf_out_name, buf_dist,"FULL","ROUND","ALL")

    return buf_out_name;


# Define Intersect
def intersect(int_lyrs):
    # ask user to name output layer
    lyr_name = input("What is the desired name of the output intersect layer?")

    # run intersect operation on input layer
    arcpy.Intersect_analysis(int_lyrs, lyr_name)

    # return resulting output layer
    return lyr_name


# Define Main
def main():


    # Define variables
    int_lyrs = []
    buf_lyrs = [lakes, mosquito, wetlands, osmp]

    # Call buffer
    for lyr in buf_lyrs:
        out_buf_name=buffer(lyr)
        int_lyrs.append(out_buf_name)


    # Call Intersect
    output_lyr_name = intersect(int_lyrs)

    # Spatial Join
    arcpy.analysis.SpatialJoin(address, output_lyr_name, "WNV_Spatial")

    # Extra Credit
    WNV_Spatial = f"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\WNV_Spatial"
    arcpy.Select_analysis(WNV_Spatial, 'exposed_addresses', "Join_Count > 0")
    count_lyr = (f"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\exposed_addresses")
    result = arcpy.GetCount_management(count_lyr)
    print("There are " + result[0] + " homes in the danger area.")
    aprx = arcpy.mp.ArcGISProject(f"{config_dict.get('proj_dir')}\WestNileOutbreak.aprx")
    map_doc = aprx.listMaps()[0]
    # Add new layer to map
    map_doc.addDataFromPath(f"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\exposed_addresses")
    aprx.save()

    # Symmetrical Difference displays the areas of no overlap between the intersect layer and the avoid point buffer.
    # Erase removes the avoid point buffer from the intersect layer creating a new risk area.

    update_layer =arcpy.Buffer_analysis(avoid, "avoid_buf", "1500 feet", "FULL", "ROUND", "ALL")
    symdif = arcpy.SymDiff_analysis(output_lyr_name,update_layer, "Areas_to_Spray", "ALL", None)
    spray_areas = arcpy.Erase_analysis(symdif,update_layer,"new_danger_area")
    new_at_risk = arcpy.SelectLayerByLocation_management(address,'INTERSECT',spray_areas)
    result2= arcpy.GetCount_management(new_at_risk)
    print("There are now " + result2[0] + " homes in the danger area after removing no spray zones.")
    map_doc.addDataFromPath(rf"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\new_danger_area")
    aprx.save()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    etl()
    main()
