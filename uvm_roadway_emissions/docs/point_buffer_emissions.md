Author: Alex Adame  
Project: Community Data Health Initiative
## Requirements
Python 3.12.2

Packages:

    census 0.8.21
    geopandas 0.14.3
    pandas 2.2.1
    pyogrio 0.7.2

## How to use
To obtain the emissions data and HPMS roadways file, contact EDF.

Under "NEW USERS - EDIT THESE VARIABLES", insert the file path to the:
- census tract shapefile directory
- emissions rate file (.csv) - can be obtained from 
- HPMS roadways file (.gdb)
- directories for both output files

Set the options for:
- buffer radius in meters (default 804.7m which is ~1/2 mile)
- state abbreviation, e.g. "MI"
- create_state_roadway_file - If True, this will output a shapefile of the roadways in the state of interest that can be used instead of the larger HPMS roadways file to cut down on processing time in the future

## Outputs
Shapefile containing the emissions data with the point buffers as geometries: "{Input State Abbreviation}_emissions_around_points.shp"
>e.g. *"uvm_roadway_emissions\outputs\MI_emissions_around_points.shp"* 

A csv containing the same emissions data without the spatial component: "{Input State Abbreviation}_emissions_around_points.csv"
>e.g. *"uvm_roadway_emissions\outputs\MI_emissions_around_points.csv"*

The output files will contain all fields in the provided point data along with fields for the four pollutant classes in the data(PM2.5, PM10, NOx, and NO2) aggregated by vehicle class (LDV, MDV, HDV, and Total). Emissions are in tons per year.

## Data sources
The vehicle emissions data is sourced from the University of Vermont in relation to the publication "2020 Near-roadway population census, traffic exposure and equity in the United States" (https://doi.org/10.1016/j.trd.2023.103965) and is tied to the 2018 Highway Performance Monitoring System (HPMS) from the U.S. Department of Transportation. 

State and county geometries are sourced from the U.S. Census TIGER/Line® API for the year 2020.
