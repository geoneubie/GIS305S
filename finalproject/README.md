## West Nile Virus Simulation
# GIS305 Spring 2022

West nile virus simulation uses data retreived from Boulder County open data (https://opendata-bouldercounty.hub.arcgis.com/)
-Lakes and Reserviors, Mosquito Larval Sites, OSMP Properties, Wetlands Regulatory, Addresses


The simulation also uses google forms to input "no spray areas" (https://docs.google.com/forms/d/e/1FAIpQLSdH9uikBhEZw99hfJU5FJLyOBYMmSkCTuXRDozO2RPIrDPbKQ/viewform)


The simulation allows the user to input buffer distances for the Lakes, Mosiquito, OSMP, and Wetlands layers, which are then intersected together creating a "danger area".


Using Extract, transform, load (ETL) protocal data from the google form is transformed to point locations and then buffered at 1500 ft creating "avoid areas".


The avoid areas are erased from the danger area creating an "analysis area"


Addresses are spatially joined to the analysis area and added to the map with a definition query to only display addresses within the danger area.

The user can input a map subtitle (such as distances used), and an export file name.

The map is then exported displaying the results of the user inputs. (Data added to the map is not saved, as to allow for multiple runs of the program without adding duplicate layers.)


# Running
User should update included yaml file with new input parameters( file locations, database locations, etc)
User should then run finalproject.py

Exports included within directory location
/WestNileOutbreakwnv.log (logfile of functions and errors)
/*userdefinedmapname*.pdf (pdf map displaying output)
