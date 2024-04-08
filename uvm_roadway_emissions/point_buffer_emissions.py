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

## PURPOSE - This is one method of estimating emissions around points of interest, like a school or hospital

# Import packages
import geopandas as gpd
import pandas as pd
from pygris import counties
from pathlib import Path
gpd.options.io_engine = "pyogrio"

#### NEW USERS - EDIT THESE VARIABLES
# Full paths to data
vehicle_emissions_path = Path(r"data\national_hpms_emissions_all_vehicles.csv") # Emission rates csv
hpms_roadways_path = Path(r"data\hpms_all_states_emissions_input.gdb") # HPMS roadways geodatabase
geodata_path = Path(r"data\School.shp") # Point data in any vector-based spatial data format
output_dir = Path(r"outputs") # Directory to store outputs

# Set options
create_state_roadway_file = False # Set to True to output the roads clipped to the state of interest for faster processing in the future
buffer_radius = 804.7  # Buffer radius in meters - 804.7m is half a mile
state_abbv = "LA"  # Insert your state's abbreviaton, e.g. TX 

#### NEW USERS - DON'T EDIT BEYOND THIS POINT
# Create output directory if it doesn't exist
if not Path.exists(output_dir):
       Path.mkdir(output_dir)

# Read in data
state_geom = counties(state=state_abbv, cache=True, year=2020).to_crs(5070) # Fetch state geometry to clip the national roadways data
vehicle_emission_rates = pd.read_csv(vehicle_emissions_path).rename(columns={'FID_Link_Cnty_Intxn': 'FID_Link'}) # Read in csv with road emission rates per road link
hpms_roads = gpd.read_file(hpms_roadways_path).to_crs(5070).clip(state_geom) # Read in national hpms roadways and clip to the state of interest
hpms_roads = hpms_roads.rename(columns={'FID_Link_Cnty_Intxn': 'FID_Link', 'THROUGH_LANES':'THRU_LANES', 'Est_AADT_LDV':'AADT_LDV',
                                        'Est_AADT_MDV':'AADT_MDV', 'Est_AADT_HDV':'AADT_HDV'}) # Shorten colnames for ESRI format standards

# -- output the roads clipped to the state of interest for faster processing in the future
if create_state_roadway_file == True:
       hpms_roads.to_file(output_dir / ("hpms_" + state_abbv + "_roadways.gdb"), driver = "OpenFileGDB")

# Process data and calculate emissions
hpms_onroad_emissions = pd.merge(hpms_roads, vehicle_emission_rates, on = 'FID_Link') # Join the emission rates to the roadways by link

geodata_buffer = gpd.read_file(geodata_path).to_crs(5070)
geodata_buffer['ID'] = geodata_buffer.index # Create unqiue ID col from index to identify emissions in overlay
geodata_buffer['geometry'] = geodata_buffer.buffer(buffer_radius)

# Get length of each roadway segment clipped to the overlaid point buffers
buffer_roads_gdf = gpd.overlay(hpms_onroad_emissions, geodata_buffer)
buffer_roads_gdf['clip_len'] = buffer_roads_gdf.length

# Multiply each pollutant's emission rates per vehicle class, then convert to tons per year 
buffer_roads_gdf['PM10_LDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'LDV']['clip_len'] * buffer_roads_gdf['ER_PM10'] * 365 / 907185).round(4)
buffer_roads_gdf['PM10_MDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'MDV']['clip_len'] * buffer_roads_gdf['ER_PM10'] * 365 / 907185).round(4)
buffer_roads_gdf['PM10_HDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'HDV']['clip_len'] * buffer_roads_gdf['ER_PM10'] * 365 / 907185).round(4)
buffer_roads_gdf['PM10_Total'] = buffer_roads_gdf.loc[:, ['PM10_LDV', 'PM10_MDV', 'PM10_HDV']].sum(axis = 1)

buffer_roads_gdf['PM25_LDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'LDV']['clip_len'] * buffer_roads_gdf['ER_PM25'] * 365 / 907185).round(4)
buffer_roads_gdf['PM25_MDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'MDV']['clip_len'] * buffer_roads_gdf['ER_PM25'] * 365 / 907185).round(4)
buffer_roads_gdf['PM25_HDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'HDV']['clip_len'] * buffer_roads_gdf['ER_PM25'] * 365 / 907185).round(4)
buffer_roads_gdf['PM25_Total'] = buffer_roads_gdf.loc[:, ['PM25_LDV', 'PM25_MDV', 'PM25_HDV']].sum(axis = 1)

buffer_roads_gdf['NOx_LDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'LDV']['clip_len'] * buffer_roads_gdf['ER_3_NOX'] * 365 / 907185).round(4)
buffer_roads_gdf['NOx_MDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'MDV']['clip_len'] * buffer_roads_gdf['ER_3_NOX'] * 365 / 907185).round(4)
buffer_roads_gdf['NOx_HDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'HDV']['clip_len'] * buffer_roads_gdf['ER_3_NOX'] * 365 / 907185).round(4)
buffer_roads_gdf['NOx_Total'] = buffer_roads_gdf.loc[:, ['NOx_LDV', 'NOx_MDV', 'NOx_HDV']].sum(axis = 1)

buffer_roads_gdf['NO2_LDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'LDV']['clip_len'] * buffer_roads_gdf['ER_33_NO2'] * 365 / 907185).round(4)
buffer_roads_gdf['NO2_MDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'MDV']['clip_len'] * buffer_roads_gdf['ER_33_NO2'] * 365 / 907185).round(4)
buffer_roads_gdf['NO2_HDV'] = (buffer_roads_gdf[buffer_roads_gdf['VEHCLASS'] == 'HDV']['clip_len'] * buffer_roads_gdf['ER_33_NO2'] * 365 / 907185).round(4)
buffer_roads_gdf['NO2_Total'] = buffer_roads_gdf.loc[:, ['NO2_LDV', 'NO2_MDV', 'NO2_HDV']].sum(axis = 1)

# Emissions are grouped by roadway link and unique point ID, then summed
buffer_roads_gdf = buffer_roads_gdf.loc[:, ['ID', 'FID_Link',
       'PM10_LDV', 'PM10_MDV', 'PM10_HDV', 'PM10_Total',
       'PM25_LDV', 'PM25_MDV', 'PM25_HDV', 'PM25_Total',
       'NOx_LDV', 'NOx_MDV', 'NOx_HDV', 'NOx_Total',
       'NO2_LDV', 'NO2_MDV', 'NO2_HDV', 'NO2_Total']].groupby(['FID_Link', 'ID']).agg("sum").reset_index()

# Sum of emissions by unique point ID to return final output of point buffers with total emissions
buffer_roads_gdf = buffer_roads_gdf.groupby('ID').agg("sum")

# Merge emissions data back onto point spatial data
gdf = pd.merge(geodata_buffer, buffer_roads_gdf, on = 'ID')

# Write data
gdf.to_file(output_dir / (state_abbv + '_emissions_around_points.shp')) # Outputs as shapefile, but can be changed to other spatial data format
gdf.to_csv(output_dir / (state_abbv + '_emissions_around_points.csv'), index = False)