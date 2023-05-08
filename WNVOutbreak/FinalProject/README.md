# GIS305S
This code is meant to find areas in Boulder, CO that need to be 
sprayed with pesticides to avoid a west nile virus outbreak. 
To run this program you will need an ArcGIS Pro project called "WestNileOutbreak"
with an empty map and a layout with your map frame, legend, a north arrow, scale bar, and a text element named "Title". 
In the geodatabase, you will need the following features:
"OSMP_Properties", "Lakes_and_Reservoirs", "Wetlands", "Mosquito_Larval_Sites", and "Addresses".
Then you will need to update the yaml file project directory with the file path for your WestNileOutbreak project. 
Once you have that set up run the "FinalProject.py" script found in the FinalProject folder.
It will ask you fill in some inputs on how far to buffer things and what you would like to name outputs.
After it is done running, you should find a pdf in the folder outside your WestNileOutbreak folder. 
