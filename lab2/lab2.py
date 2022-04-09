import arcpy
import yaml
import requests
from etl.GSheetsEtl import GSheetsEtl



def setup():
    with open('wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict

def etl():
    print ("etling...")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

# Define Buffer
def buffer(buf_lyr):
    # ask user for buffer parameters
    buf_out_name = (buf_lyr + "buf")
    buf_dist_input = input("What is the buffer distance in feet? For the "+{buf_lyr}+" layer")
    buf_dist = buf_dist_input + " feet"

    # buffer analysis
    result = arcpy.Buffer_analysis(buf_lyr, buf_out_name, buf_dist)

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
    buf_lyrs = [lakes, mosquito, wetlands, osmp,avoid]

    # Call buffer
    for lyr in buf_lyrs:
        out_buf_name=buffer(lyr)
        int_lyrs.append(out_buf_name)


    # Call Intersect
    output_lyr_name = intersect(int_lyrs)

    # Spatial Join
    arcpy.analysis.SpatialJoin(address, output_lyr_name, "WNV_Spatial")

    # Extra Credit
    WNV_Spatial = f"{config_dict.get('project_dir')}WestNileOutbreak.gdb\WNV_Spatial"
    arcpy.Select_analysis(WNV_Spatial, 'exposed_addresses', "Join_Count > 0")
    count_lyr = (f"{config_dict.get('project_dir')}WestNileOutbreak.gdb\exposed_addresses")
    result = arcpy.GetCount_management(count_lyr)
    print("There are " + result[0] + " homes in the danger area.")
    aprx = arcpy.mp.ArcGISProject(f"{config_dict.get('project_dir')}WestNileOutbreak.aprx")
    map_doc = aprx.listMaps()[0]
    # Add new layer to map
    map_doc.addDataFromPath(f"{config_dict.get('project_dir')}WestNileOutbreak.gdb\exposed_addresses")
    aprx.save()

    #symmetrical Difference
    arcpy.SymDiff_analysis(output_lyr_name,"Avoid_Points_buf", "Areas_to_Spray", "ALL", None)
    map_doc.addDataFromPath(f"{config_dict.get('project_dir')}WestNileOutbreak.gdb\Areas_to_Spray")
    aprx.save()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)

    arcpy.env.workspace = f"{config_dict.get('project_dir')}WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    input_path = f"{config_dict.get('project_dir')}WestNileOutbreak.gdb"


    # define layers
    address = input_path.format(layer_name=r"\Addresses")
    lakes = input_path.format(layer_name=r"\Lakes_Reservoirs")
    mosquito = input_path.format(layer_name=r"\Mosquito_Larva")
    osmp = input_path.format(layer_name=r"\OSMP_Properties")
    wetlands = input_path.format(layer_name=r"\Wetlands")
    avoid = input_path.format(layer_name=r"\Avoid_Points")


    etl()
    main()
