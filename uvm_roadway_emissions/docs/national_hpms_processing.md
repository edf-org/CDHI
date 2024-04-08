Author: Alex Adame  
Project: Community Data Health Initiative
## Requirements
Python 3.12.2

Packages:

    geopandas 0.14.3
    pandas 2.2.1
    pygris 0.1.6
    pyogrio 0.7.2

## How to use
Under "NEW USERS - EDIT THESE VARIABLES", insert the file path to the:
- emissions rate file (.csv)
- HPMS roadways file (.gdb)
- spatial data file containing the points of interest in any vector based spatial format (.shp, .gdb, .geojson, etc.)
- directory for output files

Insert your Census API key between the quotes - go to https://api.census.gov/data/key_signup.html to request a key

## Outputs
A directory for each state containing the emissions data with census tracts as geometries: "tl_2020_{State FIPS ID}_tract\tl_2020_{State FIPS ID}_tract_vehicle_emissions.shp"
>e.g. *"uvm_roadway_emissions\outputs\2020_tract_emissions_shapefiles\tl_2020_11_tract\tl_2020_11_tract_vehicle_emissions.shp"* 

A directory for each state containing the same emissions data without the spatial component: "tl_2020_{State FIPS ID}_tract\tl_2020_{State FIPS ID}_tract_vehicle_emissions.csv"
>e.g. *"uvm_roadway_emissions\outputs\2020_tract_emissions_csvs\tl_2020_11_tract_vehicle_emissions.csv"*

The output files will contain all population data for children 5 and under, 18 and under, and emissions for the four pollutant classes in the data(PM2.5, PM10, NOx, and NO2) aggregated by vehicle class (LDV, MDV, HDV, and Total) and census tract. Emissions are in tons per year.

## Data sources
The vehicle emissions data is sourced from the University of Vermont in relation to the publication "2020 Near-roadway population census, traffic exposure and equity in the United States" (https://doi.org/10.1016/j.trd.2023.103965) and is tied to the 2020 Highway Performance Monitoring System (HPMS) from the U.S. Department of Transportation. 

State and county geometries are sourced from the U.S. Census TIGER/Line® API for the year 2020.