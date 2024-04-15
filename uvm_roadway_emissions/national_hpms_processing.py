# This program is an on-road vehicle emissions data post-processing and analysis routine
# prepared by Environmental Defense Fund. 

# For details on how to use this program refer to the doc/ folder

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.   This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details at root level in LICENSE.txt
# or see http://www.gnu.org/licenses/.

# PURPOSE - This script finds roadways emissions overlaid on each census tract in the United States
# and returns the data as shapefiles and csv's

# Import packages
import geopandas as gpd
import pandas as pd
from census import Census
from pathlib import Path
gpd.options.io_engine = "pyogrio"

#### NEW USERS - EDIT THESE VARIABLES
# INPUT DIRECTORIES
census_shapes_dir = Path(r'data\2020_census_tracts') # directory containing all census tract shapefiles
vehicle_emissions_path = Path(r"data\national_hpms_emissions_all_vehicles_2018.csv") # Emission rates csv
hpms_roadways_path = Path(r"data\2018_HPMS_Emissions.gdb") # HPMS roadways geodatabase

# OUTPUT DIRECTORIES
shapefile_dir = Path(r'outputs\2018_hpms_tract_emissions_shapefiles') # directory to store output shapefiles
csv_dir = Path(r'outputs\2018_hpms_tract_emissions_csvs') # directory to store output csvs

# Insert your census API key - sign up for a key at https://api.census.gov/data/key_signup.html
key = Census("")

#### NEW USERS - DON'T EDIT BEYOND THIS POINT
# Read in csv with all roadway segment emission rates
all_vehicle_emission_rates = pd.read_csv(vehicle_emissions_path)

# Read in national 2018 hpms roadway segments used in UVM paper
hpms_roads = gpd.read_file(hpms_roadways_path).to_crs(5070) #for 2018 data
hpms_roads = hpms_roads.drop(columns = {'VEHCLASS', 'ER_100_PM10_PRI', 'ER_106_PM10_PRI', 'ER_107_PM10_PRI',
       'ER_110_PM25_PRI', 'ER_116_PM25_PRI', 'ER_117_PM25_PRI', 'ER_3_NOX',
       'ER_33_NO2', 'ER_98_CO2', 'ER_PM10', 'ER_PM25'})
# glob all the shapefiles in the directory containing census tract geometries
census_shapes = census_shapes_dir.rglob("*.shp")

# Process emissions data for every tract in the US
# Outputs a shapefile and csv for each state
for file in census_shapes:
       tracts = gpd.read_file(file).to_crs(5070)
       # Get census population data via the API
       census_data = key.acs5.state_county_tract(fields = ('NAME', 'B09001_001E', 'B09001_003E', 'B09001_004E', 'B09001_005E'),
                                          state_fips = tracts.loc[0, 'STATEFP'],
                                          county_fips = '*',
                                          tract = "*",
                                          year = 2020)

       census_data = pd.DataFrame(census_data)
       # Create 5 and under column by adding together age 5, 3-4, and under 3
       census_data['Pop5Under'] = census_data[['B09001_003E', 'B09001_004E', 'B09001_005E']].sum(axis = 1)
       # Create GEOID.Tract column to join to census spatial data
       census_data['GEOID'] = census_data.loc[:, ['state', 'county', 'tract']].sum(axis = 1)
       # Subset data to make output less cluttered
       census_data = census_data.loc[:, ['B09001_001E', 'Pop5Under', 'GEOID']].rename(columns = {'B09001_001E': 'Pop18Under'})

       # Join census population data and spatial data
       tracts_pop_2020 = pd.merge(tracts, census_data, on = 'GEOID')
       # Convert area to square miles from meters
       tracts_pop_2020['area_sqmi'] = tracts_pop_2020.area/2589988
       # Calculate population per square mile
       tracts_pop_2020['Pop5SqMi'] = (tracts_pop_2020['Pop5Under']/tracts_pop_2020['area_sqmi']).round(2)
       tracts_pop_2020['Pop18SqMi'] = (tracts_pop_2020['Pop18Under']/tracts_pop_2020['area_sqmi']).round(2)

       # Merge roadways and emission rates
       roads_emissions = pd.merge(hpms_roads, all_vehicle_emission_rates, on = 'FID_Link_Cnty_Intxn')

       # Overlay returns roadways clipped to each census tract with identifying information
       tract_emissions = gpd.overlay(roads_emissions, tracts)
       tract_emissions['clip_len'] = tract_emissions.length

       # Get length of each roadway segment and multiply by emission rates
       # Emissions are then converted to tons per year
       tract_emissions['PM10_LDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'LDV']['clip_len'] * tract_emissions['ER_PM10'] * 365 / 907185).round(4)
       tract_emissions['PM10_MDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'MDV']['clip_len'] * tract_emissions['ER_PM10'] * 365 / 907185).round(4)
       tract_emissions['PM10_HDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'HDV']['clip_len'] * tract_emissions['ER_PM10'] * 365 / 907185).round(4)
       tract_emissions['PM10_Total'] = tract_emissions.loc[:, ['PM10_LDV', 'PM10_MDV', 'PM10_HDV']].sum(axis = 1)

       tract_emissions['PM25_LDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'LDV']['clip_len'] * tract_emissions['ER_PM25'] * 365 / 907185).round(4)
       tract_emissions['PM25_MDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'MDV']['clip_len'] * tract_emissions['ER_PM25'] * 365 / 907185).round(4)
       tract_emissions['PM25_HDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'HDV']['clip_len'] * tract_emissions['ER_PM25'] * 365 / 907185).round(4)
       tract_emissions['PM25_Total'] = tract_emissions.loc[:, ['PM25_LDV', 'PM25_MDV', 'PM25_HDV']].sum(axis = 1)

       tract_emissions['NOx_LDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'LDV']['clip_len'] * tract_emissions['ER_3_NOX'] * 365 / 907185).round(4)
       tract_emissions['NOx_MDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'MDV']['clip_len'] * tract_emissions['ER_3_NOX'] * 365 / 907185).round(4)
       tract_emissions['NOx_HDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'HDV']['clip_len'] * tract_emissions['ER_3_NOX'] * 365 / 907185).round(4)
       tract_emissions['NOx_Total'] = tract_emissions.loc[:, ['NOx_LDV', 'NOx_MDV', 'NOx_HDV']].sum(axis = 1)

       tract_emissions['NO2_LDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'LDV']['clip_len'] * tract_emissions['ER_33_NO2'] * 365 / 907185).round(4)
       tract_emissions['NO2_MDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'MDV']['clip_len'] * tract_emissions['ER_33_NO2'] * 365 / 907185).round(4)
       tract_emissions['NO2_HDV'] = (tract_emissions[tract_emissions['VEHCLASS'] == 'HDV']['clip_len'] * tract_emissions['ER_33_NO2'] * 365 / 907185).round(4)
       tract_emissions['NO2_Total'] = tract_emissions.loc[:, ['NO2_LDV', 'NO2_MDV', 'NO2_HDV']].sum(axis = 1)

       # Aggregate road segment emissions by tract
       # Emissions are grouped by roadway link and unique GEOID, then summed
       tract_emissions = tract_emissions.loc[:, ['GEOID', 'FID_Link_Cnty_Intxn',
       'PM10_LDV', 'PM10_MDV', 'PM10_HDV', 'PM10_Total',
       'PM25_LDV', 'PM25_MDV', 'PM25_HDV', 'PM25_Total',
       'NOx_LDV', 'NOx_MDV', 'NOx_HDV', 'NOx_Total',
       'NO2_LDV', 'NO2_MDV', 'NO2_HDV', 'NO2_Total']].groupby(['GEOID']).agg("sum").reset_index()

       # Join population data to emissions data
       roads_emissions = pd.merge(tracts_pop_2020, tract_emissions, on = 'GEOID')
       # Create columns for emissions per square mile and round to 3 decimal places
       roads_emissions[['PM10_sqmi', 'PM25_sqmi', 'NOx_sqmi', 'NO2_sqmi']] = roads_emissions.loc[:,
                     ['PM10_Total', 'PM25_Total', 'NOx_Total', 'NO2_Total']].div(
                     roads_emissions['area_sqmi'], axis = 0).round(3)

       # Create directories to store outputs if they don't exist
       if not Path.exists(shapefile_dir / file.stem):
              Path.mkdir(shapefile_dir / file.stem, parents=True, exist_ok=True)
       if not Path.exists(csv_dir):
              Path.mkdir(csv_dir, parents=True, exist_ok=True)

       # Write shapefile
       roads_emissions.to_file(Path.joinpath(shapefile_dir, file.stem, file.stem + '_vehicle_emissions.shp'))
       # Subset columns and write csv
       roads_emissions.loc[:, ['GEOID', 'NAMELSAD', 'area_sqmi',
                     'Pop18Under', 'Pop5Under', 'Pop5SqMi', 'Pop18SqMi',
                     'PM10_LDV', 'PM10_MDV', 'PM10_HDV', 'PM10_Total',
                     'PM25_LDV', 'PM25_MDV', 'PM25_HDV', 'PM25_Total',
                     'NOx_LDV', 'NOx_MDV', 'NOx_HDV', 'NOx_Total',
                     'NO2_LDV', 'NO2_MDV', 'NO2_HDV', 'NO2_Total',
                     'PM10_sqmi', 'PM25_sqmi', 'NOx_sqmi', 'NO2_sqmi']
                     ].to_csv(
                            Path.joinpath(csv_dir, file.stem + '_vehicle_emissions.csv'), index = False)

       print(file.stem + ' processing finished!')