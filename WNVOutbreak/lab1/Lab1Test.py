import arcpy  # import the arcpy library


# Defining a function that will set our workspace, allow us to overwrite files, and allows us to add outputs to the map
def setup():
    arcpy.env.workspace = r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    arcpy.env.addOutputsToMap = True


def buffer(layer_name, buff_dist):
    # Buffer the chosen layer by a set distance
    units = "miles"
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


def main():
    buff_layer_list = ["Mosquito_Larval_Sites", "Wetlands", "Lakes_and_Reservoirs", "OSMP_Properties"]

    for layer in buff_layer_list:
        # Goes through the list of layers that need to be buffered and runs the buffer function on each one
        buff_dist = input(f"\nHow far would you like to buffer {layer}\n")
        buffer(layer, buff_dist)

    inter_layer_list = ["buff_Mosquito_Larval_Sites", "buff_Wetlands", "buff_Lakes_and_Reservoirs", "buff_OSMP_Properties"]

    lyr_inter = intersect(inter_layer_list)
    print(f"Creating a layer named {lyr_inter} that shows where the layers:\n{inter_layer_list} intersect.")

    proj_path = r"C:\Users\hcvin\OneDrive\Desktop\Spring_2023\GIS_3005\arcgis\westnileoutbreak"
    aprx = arcpy.mp.ArcGISProject(rf"{proj_path}\WestNileOutbreak.aprx")
    map_doc = aprx.listMaps()[0]

    # Adds the spatial join output to the map
    map_doc.addDataFromPath(rf"{proj_path}\WestNileOutbreak.gdb\{lyr_inter}")

    # Saves the project
    aprx.save()

    lyr_sjoin = spatial_join(lyr_inter)

    addAOCCount = 0

    with arcpy.da.SearchCursor(lyr_sjoin, ["Join_Count"]) as joinCursor:
        for x in joinCursor:
            # Creating a search cursor and iteration through the attributes in the Join_Count field
            if x[0] == 1:
                # If statement add 1 to a variable set to 0, so it can count each instance that 1 shows up
                addAOCCount = addAOCCount + 1

    print(f"There are {addAOCCount} addresses in the area of conern.")

    aprx.save()

if __name__ == '__main__':
    setup()
    main()

