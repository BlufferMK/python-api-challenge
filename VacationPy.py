# %% [markdown]
# # VacationPy
# ---
# 
# ## Starter Code to Import Libraries and Load the Weather and Coordinates Data

# %%
# Dependencies and Setup
import hvplot.pandas
import pandas as pd
import requests

import warnings
warnings.filterwarnings("ignore")

# Import API key
from api_keys import geoapify_key

import pycountry

# %%
# Load the CSV file created in Part 1 into a Pandas DataFrame
city_data_df = pd.read_csv("output_data/cities.csv")

# Display sample data
city_data_df.head()

# %% [markdown]
# ---
# 
# ### Step 1: Create a map that displays a point for every city in the `city_data_df` DataFrame. The size of the point should be the humidity in each city.

# %%
%%capture --no-display

# Configure the map plot
map_plot = city_data_df.hvplot.points(
    "Lng",
    "Lat",
    geo = True,
    tiles = "OSM",
    frame_width = 800,
    frame_height = 600,
    size = "Humidity",
    scale = 0.3,
    color = "City",
    xlabel = "Longitude",
    ylabel = "Latitude",
    legend = False
)

# Display the map
map_plot

# %% [markdown]
# ### Step 2: Narrow down the `city_data_df` DataFrame to find your ideal weather condition

# %%
# Narrow down cities that fit criteria and drop any results with null values
ideal_city_df = city_data_df.loc[(city_data_df['Max Temp']>22)&(city_data_df['Max Temp']<30)&(city_data_df['Humidity']<80),:]

# Drop any rows with null values
ideal_city_df=ideal_city_df.dropna(how='any')
# Display sample data
ideal_city_df

# %% [markdown]
# ### Step 3: Create a new DataFrame called `hotel_df`.

# %%
# Use the Pandas copy function to create DataFrame called hotel_df to store the city, country, coordinates, and humidity
hotel1_df = ideal_city_df[["City","Country","Lat","Lng","Humidity"]]

# Add an empty column, "Hotel Name," to the DataFrame so you can store the hotel found using the Geoapify API
hotel1_df['Hotel']={}

# Display sample data
hotel_df = hotel1_df.reset_index(drop=True)

hotel_df

# %% [markdown]
# ### Step 4: For each city, use the Geoapify API to find the first hotel located within 10,000 metres of your coordinates.

# %%
# Set parameters to search for a hotel
latitude = []
longitude = []

radius = 10000
limit = 1


params = params = {
    "limit":limit,
    "categories":"accommodation.hotel",
    "apiKey": geoapify_key    
}

# Print a message to follow up the hotel search
print("Starting hotel search")

# Iterate through the hotel_df DataFrame
for index, row in hotel_df.iterrows():
    latitude = hotel_df.loc[index,"Lat"]   
    longitude = hotel_df.loc[index,"Lng"] 
    
    # Add filter and bias parameters with the current city's latitude and longitude to the params dictionary
    params["filter"] = f'circle:{longitude},{latitude},{radius}'
    bias = f"proximity:{longitude},{latitude}"
    params["bias"] = bias
    
    # Set base URL
    base_url = "https://api.geoapify.com/v2/places"


    # Make and API request using the params dictionaty
    name_address = requests.get(base_url, params=params)
    
    # Convert the API response to JSON format
    name_address = name_address.json()
    
    # Grab the first hotel from the results and store the name in the hotel_df DataFrame
    try:
        hotel_df.loc[index, "Hotel"] = name_address["features"][0]["properties"]["name"]
    except (KeyError, IndexError):
        # If no hotel is found, set the hotel name as "No hotel found".
        hotel_df.loc[index, "Hotel"] = "No hotel found"
        
    # Log the search results
    print(f"{hotel_df.loc[index, 'City']} - nearest hotel: {hotel_df.loc[index, 'Hotel']}")

# Display sample data
hotel_df

# %% [markdown]
# ### Step 5: Add the hotel name and the country as additional information in the hover message for each city in the map.

# %%
hotel_df.to_csv("output_data/hotels.csv", index_label="City")

# %%
hotel_df = pd.read_csv("output_data/hotels.csv", index_col="City")

hotel_df.head(30)

# %%
%%capture --no-display

# Configure the map plot
map_plot_1 = hotel_df.hvplot.points(
    "Lng",
    "Lat",
    hover_cols = ['Hotel','Country'],
    geo = True,
    tiles = "OSM",
    size = "Humidity",
    scale = 0.3,
    color = "City.1",
    xlabel = "Longitude",
    ylabel = "Latitude",
    legend = False
)


# Display the map
map_plot_1

# %%



