import arcpy.mp as map_mod

aprx = map_mod.ArcGISProject(r'C:\Users\Owner\Documents\ArcGIS\Projects\ClassExerciseLesson#1\ClassExerciseLesson#1.'
                             'aprx')

lyt_list = aprx.listLayouts()
for lyt in lyt_list:
    print(lyt.name)
lyt = aprx.listLayouts()[0]
for el in lyt.listElements():
    print(el.name)

