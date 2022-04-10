import arcpy

arcpy.env.workspace = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb"
arcpy.env.overwriteOutput = True

WNV_Spatial = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb\WNV_Spatial"

arcpy.Select_analysis(WNV_Spatial, 'selection', "Join_Count > 0")

count_lyr = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb\selection"
result = arcpy.GetCount_management(count_lyr)
print("There are " + result[0] + " homes in the danger area.")