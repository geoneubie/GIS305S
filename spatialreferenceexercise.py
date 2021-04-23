import arcpy

srs = arcpy.ListSpatialReferences("*utm/north america*")

for sr_string in srs:
    sr_object = arcpy.SpatialReference(sr_string)
    print("{0.centralMeridian}   {0.name}  {0.PCSCode}".format(sr_object))

aprx = arcpy.mp.ArcGISProject(r"C:\Users\Owner\Desktop\GIS305\GIS305Ass#1\GIS305Ass#1.aprx")
map_doc = aprx.listMaps()[0]

state_plane_noco = arcpy.SpatialReference(3743)
map_doc.spatialReference = state_plane_noco
