Author: Alex Adame  
Project: Community Data Health Initiative
## Requirements
Python client with pandas, geopandas, pyogrio, pathlib, and pygris

## How to use
Under "USER INPUT", insert the full file path to the:
- emissions rate file (.csv)
- HPMS roadways file (.gdb)
- spatial data file containing the points of interest in any vector based spatial format (.shp, .gdb, .geojson, etc.)
- directory for output files

Set the options for:
- buffer radius in meters (default 804.7m which is ~1/2 mile)
- state abbreviation, e.g. "MI"

Run the script and the files will be generated in the output folder. The runtime may take upwards of 20 minutes. 

## Outputs
Shapefile containing the emissions data with the point buffers as geometries: "{Input State Abbreviation}_emissions_around_points.shp"
>e.g. *"C:\Users\aadame\Documents\uvm_roadway_emissions\outputs\MI_emissions_around_points.shp"* 

A csv containing the same emissions data without the spatial component: "{Input State Abbreviation}_emissions_around_points.csv"
>e.g. *"C:\Users\aadame\Documents\uvm_roadway_emissions\outputs\MI_emissions_around_points.csv"*

The output files will contain all fields in the provided point data along with fields for the four pollutant classes in the data(PM2.5, PM10, NOx, and NO2) aggregated by vehicle class (LDV, MDV, HDV, and Total). Emissions are in tons per year.

## Data sources
The vehicle emissions data is sourced from the University of Vermont in relation to the publication "2020 Near-roadway population census, traffic exposure and equity in the United States" (https://doi.org/10.1016/j.trd.2023.103965) and is tied to the 2018 Highway Performance Monitoring System (HPMS) from the U.S. Department of Transportation. 

State and county geometries are sourced from the U.S. Census TIGER/Line® API for the year 2020.
