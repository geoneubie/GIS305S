import arcpy

srs = arcpy.ListSpatialReferences("*utm/north america*")

for sr_string in srs:
    sr_object = arcpy.SpatialReference(sr_string)
    print("{0.centralMeridian}   {0.name}  {0.PCSCode}".format(sr_object))

aprx = arcpy.mp.ArcGISProject(r"C:\Users\Owner\Documents\ArcGIS\Projects\ClassExerciseLesson#1\ClassExerciseLesson#1"
                              r".aprx")
map_doc = aprx.listMaps()[0]

state_plane_noco = arcpy.SpatialReference(3743)
map_doc.spatialReference = state_plane_noco

lyr = map_doc.listLayers("U.S. States (Generalized)")[0]
# Get the symbology.
sym = lyr.symbology

sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
lyr.symbology = sym
lyr.transparency = 50
# aprx.save()

lyr.definitionQuery = "STATE_NAME = 'Colorado'"
aprx.save()
