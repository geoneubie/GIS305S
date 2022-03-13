import arcpy

def setup():
    arcpy.env.workspace = r"C:\Users\Owner\Documents\305 Python\Lab 1A\WestNileOutbreak\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
def buffer(layer_name, buf_dist):
    # Buffer the incoming layer by the buffer distance
    output_buffer_layer_name = f"{layer_name}_buf"

    print(f'My Buffering {layer_name} to generate a new {output_buffer_layer_name}')

    arcpy.analysis.Buffer(layer_name, output_buffer_layer_name, buf_dist, "FULL", "ROUND", "ALL")

def intersect(layer_name, int_lyrs):
    # Use a breakpoint in the code line below to debug your script.
    print(f'My intersect Method')

    output_intersect_name = "Intersect"
    arcpy.analysis.Intersect(int_lyrs, output_intersect_name)


def spatial_join():
    # Use a breakpoint in the code line below to debug your script.
    print(f'My spatial join Method')
    arcpy.analysis.SpatialJoin("BoulderAddresses", "Intersect", "Areas_of_concern")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()
    # mosquito larval sites
    # wetlands
    # lakes and reservoirs
    # open space (OSMP)
    buffer_layer_list = ["Mosquito_Larval_Sitess", "LakesandRes_Boulder", "OSMP_properties", "Wetlands_Boulder"]
    for layer in buffer_layer_list:
        print("Looping")
        buffer(layer, "0.1 mile")
    int_lyrs = ["LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf", "Wetlands_Boulder_buf"]
    intersect("Intersect", int_lyrs)

    spatial_join()


