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
To obtain the emissions data and HPMS roadways file, contact EDF.

Under "NEW USERS - EDIT THESE VARIABLES", insert the file path to the:
- emissions rate file (.csv)
- HPMS roadways file (.gdb)
- spatial data file containing the points of interest in any vector based spatial format (.shp, .gdb, .geojson, etc.)
- directory for output files

Insert your Census API key between the quotes - go to https://api.census.gov/data/key_signup.html to request a key

## Outputs
A directory for each state containing the emissions data with census tracts as geometries: "tl_2018_{State FIPS ID}_tract\tl_2018_{State FIPS ID}_tract_vehicle_emissions.shp"
>e.g. *"uvm_roadway_emissions\outputs\2018_tract_emissions_shapefiles\tl_2018_11_tract\tl_2018_11_tract_vehicle_emissions.shp"* 

A directory for each state containing the same emissions data without the spatial component: "tl_2018_{State FIPS ID}_tract\tl_2018_{State FIPS ID}_tract_vehicle_emissions.csv"
>e.g. *"uvm_roadway_emissions\outputs\2018_tract_emissions_csvs\tl_2018_11_tract_vehicle_emissions.csv"*

## Data Dictionary

| Parameter Name | Units | Description |
|---|---|---|
| GEOID20 | NA | Unique geographic identifier assigned by the U.S. Census |
| NAMELSAD | NA | Tract Name |
| area_sqmi | Square miles | Area in square miles |
| Pop18Under | Number of people | Population aged 18 and younger |
| Pop5Under | Number of people | Population aged 5 and younger |
| Pop5SqMi | Number of people per square mile | Population aged 5 and younger per square mile, normalized by census tract |
| Pop18SqMi | Number of people per square mile | Population aged 18 and younger per square mile, normalized by census tract |
| PM10_LDV | Tons per year | Particulate Matter smaller than or equal to 10Ám (PM10) from light-duty vehicles |
| PM10_MDV | Tons per year | Particulate Matter smaller than or equal to 10Ám (PM10) from medium-duty vehicles |
| PM10_HDV | Tons per year | Particulate Matter smaller than or equal to 10Ám (PM10) from heavy-duty vehicles |
| PM10_Total | Tons per year | Particulate Matter smaller than or equal to 10Ám (PM10) from all vehicles combined |
| PM25_LDV | Tons per year | Particulate Matter smaller than or equal to 2.5Ám (PM2.5) from light-duty vehicles |
| PM25_MDV | Tons per year | Particulate Matter smaller than or equal to 2.5Ám (PM2.5) from medium-duty vehicles |
| PM25_HDV | Tons per year | Particulate Matter smaller than or equal to 2.5Ám (PM2.5) from heavy-duty vehicles |
| PM25_Total | Tons per year | Particulate Matter smaller than or equal to 2.5Ám (PM2.5) from all vehicles combined |
| NOx_LDV | Tons per year | Oxides of Nitrogen (NOx) from light-duty vehicles |
| NOx_MDV | Tons per year | Oxides of Nitrogen (NOx) from medium-duty vehicles |
| NOx_HDV | Tons per year | Oxides of Nitrogen (NOx) from heavy-duty vehicles |
| NOx_Total | Tons per year | Oxides of Nitrogen (NOx) from all vehicles combined |
| NO2_LDV | Tons per year | Nitrogen Dioxide (NO2) from light-duty vehicles |
| NO2_MDV | Tons per year | Nitrogen Dioxide (NO2) from medium-duty vehicles |
| NO2_HDV | Tons per year | Nitrogen Dioxide (NO2) from heavy-duty vehicles |
| NO2_Total | Tons per year | Nitrogen Dioxide (NO2) from all vehicles combined |
| PM10_sqmi | Tons per year per square mile | Particulate Matter smaller than or equal to 10Ám (PM10) from all vehicles combined ,per square mile, normalized by census tract |
| PM25_sqmi | Tons per year per square mile | Particulate Matter smaller than or equal to 2.5Ám (PM2.5) from all vehicles combined, per square mile, normalized by census tract |
| NOx_sqmi | Tons per year per square mile | Oxides of Nitrogen (NOx) from all vehicles combined, per square mile, normalized by census tract |
| NO2_sqmi | Tons per year per square mile | Nitrogen Dioxide (NO2) from all vehicles combined, per square mile, normalized by census tract |

## Data sources
The vehicle emissions data is sourced from the University of Vermont in relation to the publication "2020 Near-roadway population census, traffic exposure and equity in the United States" (https://doi.org/10.1016/j.trd.2023.103965) and is tied to the 2020 Highway Performance Monitoring System (HPMS) from the U.S. Department of Transportation. 

State and county geometries are sourced from the U.S. Census TIGER/Line® API for the year 2020.