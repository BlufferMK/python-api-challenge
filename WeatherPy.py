# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Import the OpenWeatherMap API key
from api_keys import weather_api_key

# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy

import datetime


# ### Generate the Cities List by Using the `citipy` Library


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []
# Range of latitudes and longitudes
lat_range = (-80, 80)
lng_range = (-180, 180)
# I used -80 to 80 as there are very few cities that are not in this range, 
# and none are likely to be vacation destinations.

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in full_cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# # reduced number of cities for code development
# # test code
# count = 0
# for city in full_cities:
#     if count <35:
#         cities.append(city)
#         count +=1
# 
# print(f"Number of cities in the smaller list: {len(cities)}")
# 

# Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# # test code
# 
# url = "https://api.openweathermap.org/data/2.5/weather?"
# city = cities[27]
# 
# city_url = url + "q=" + city + "&appid=" + weather_api_key
# 
# print(city_url)
# 
# city_weather = requests.get(city_url).json()
# 
# city_weather


# Set the API base URL
url = "https://api.openweathermap.org/data/2.5/weather?"

# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):
        
    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
    city_url = url + "q=" + city + "&appid=" + weather_api_key
    
    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Parse the JSON and retrieve data
        city_weather = requests.get(city_url).json()

        # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date

        city_lat = city_weather['coord']['lat']
        city_lng = city_weather['coord']['lon']
        city_max_temp = city_weather['main']['temp_max'] - 273
        city_humidity = city_weather['main']['humidity']
        city_clouds = city_weather['clouds']['all']
        city_wind = city_weather['wind']['speed']
        city_country = city_weather['sys']['country']
        dt = city_weather['dt']
        dt2 = datetime.datetime.fromtimestamp(dt)
        city_date = dt2.strftime("%Y-%m-%d")

        # Append the City information into city_data list
        city_data.append({"City": city, 
                          "Lat": city_lat, 
                          "Lng": city_lng, 
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})

    # If an error is experienced, skip the city
    except:
        print("City not found. Skipping...")
        pass
              
# Indicate that Data Loading is complete 
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


print(city_data)


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# Display sample data
city_data_df.head()


# Export the City_Data into a csv
city_data_df.to_csv("output_data/cities.csv", index_label="City_ID")


# Read saved data
city_data_df = pd.read_csv("output_data/cities.csv", index_col="City_ID")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots

# #### Latitude Vs. Temperature

city_data_df.dtypes

# Build scatter plot for latitude vs. temperature
city_data_df.plot(kind="scatter", x="Lat", y="Max Temp", grid=True, figsize=(8,8),
              title="City Max Temperature vs. Latitude (2024-2-1)",xlabel = "Latitude", 
              ylabel = "Maximum Temperature (C)")
#plt.show()

# Save the figure
plt.savefig("output_data/TempvsLat.png")


# #### Latitude Vs. Humidity

# Build the scatter plots for latitude vs. humidity
city_data_df.plot(kind="scatter", x="Lat", y="Humidity", grid=True, figsize=(8,8),
              title="City Humidity(%) vs. Latitude (2024-2-1)",xlabel = "Latitude", ylabel = "Humidity (%)")
#plt.show()

# Save the figure
plt.savefig("output_data/HumvsLat.png")

# #### Latitude Vs. Cloudiness

# Build the scatter plots for latitude vs. cloudiness
city_data_df.plot(kind="scatter", x="Lat", y="Cloudiness", grid=True, figsize=(8,8),
              title="City Cloudiness vs. Latitude (2024-2-1)",xlabel = "Latitude", ylabel = "Cloudiness")
#plt.show()

# Save the figure
plt.savefig("output_data/cloudsvsLat.png")

# #### Latitude vs. Wind Speed Plot

# Build the scatter plots for latitude vs. wind speed
city_data_df.plot(kind="scatter", x="Lat", y="Wind Speed", grid=True, figsize=(8,8),
              title="City Wind Speed vs. Latitude (2024-2-1)",xlabel = "Latitude", ylabel = "Wind Speed")
#plt.show()

# Save the figure
plt.savefig("output_data/windvsLat.png")



# ## Compute Linear Regression for Each Relationship
# 

# Define a function to create Linear Regression plots
y_axis_columns = ['Max Temp',"Humidity","Cloudiness","Wind Speed"]

x_values = city_data_df['Lat']

def lin_regress():
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
    regress_values = x_values * slope + intercept
    line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
    plt.scatter(x_values,y_values)
    plt.plot(x_values,regress_values,"r-")
    plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
    plt.xlabel = ("Latitude")
    plt.ylabel(y_axis_columns[y])
    plt.show()
for y in range(4):
     y_values = city_data_df[y_axis_columns[y]]
     lin_regress()



# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
northern_hemi_df = city_data_df.loc[city_data_df['Lat']>=0,:]

# Display sample data
northern_hemi_df

# Create a DataFrame with the Southern Hemisphere data (Latitude < 0)
southern_hemi_df = city_data_df.loc[city_data_df['Lat']<0,:]

# Display sample data
southern_hemi_df.head()

# ###  Temperature vs. Latitude Linear Regression Plot

# Linear regression on Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Max Temp']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Max Temp (C)')
plt.show()
print("The r-value is :", rvalue)


# Linear regression on Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Max Temp (C)')
plt.show()
print("The r-value is :", rvalue)


# **Discussion about the linear relationship:** 
# 
# In the Northern Hemisphere, there is clearly some correlation between Latitude and Maximum Temperature 
# for this date in February.  There is increased variability north of Latitude 30, however.  North of this 
# latitude, the range of maximum temperatures for a given latitude increases dramatically.  It might be 
# interesting to simply look at a regression for the tropical locations in the Northern Hemisphere.  
# I believe the r-value would be even closer to 1.
# 
# For the Southern Hemisphere, the correlation is much less.  There are many cities in latitudes 
# between -20 and -30 that show quite high temperatures.  This is perhaps unsurprising as the temperatures 
# reflect summertime weather in these areas, somewhat distant from the equator where seasonal temperature 
# differences would be expected.  Similarly, the temperatures in the southern hemisphere, even far from the 
# equator show higher maximum temperatures than some places in the northern hemisphere.  

# It should also be noted that there are no cities randomly chosen that are further south than -60 latitude.  
# There are also quite a few fewer cities represented in the southern hemisphere.


# ### Humidity vs. Latitude Linear Regression Plot

# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Humidity']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.show()
print("The r-value is :", rvalue)

# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Humidity']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.show()
print("The r-value is :", rvalue)


# **Discussion about the linear relationship:** 
# There is very little correlation between humidity and latitude for either the northern hemisphere 
# or the southern hemisphere.  It appears that there is a very broad trend toward higher humidity nearer 
# the equator, and lower humidity farther from the equator, but it is not useful for making predictions 
# for any individual city.  The variability in humidity, especially at the higher latitudes, is quite high. 
 
# One could say that there is a very good chance that the humidity will be above 60% for any city within 
# 20 degrees of the equator, but there are many examples of cities for which this is still not true.   


# ### Cloudiness vs. Latitude Linear Regression Plot


# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Cloudiness']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Cloudiness')
plt.show()
print("The r-value is :", rvalue)


# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Cloudiness']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Cloudiness')
plt.show()
print("The r-value is :", rvalue)


# **Discussion about the linear relationship:** 
# 
# There is essentially no relationship between latitude and cloudiness.  The r-values for both hemispheres 
# are both well below 0.3.  There is a large amount of variability of cloudiness at the same latitude.  
# Cloudiness apparently depends much more heavily on factors other than latitude.


# ### Wind Speed vs. Latitude Linear Regression Plot


# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Wind Speed']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Wind Speed')
plt.show()
print("The r-value is :", rvalue)

# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Wind Speed']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
# plt.xlabel('Latitude')
plt.ylabel('Wind Speed')
plt.show()
print("The r-value is :", rvalue)


# **Discussion about the linear relationship:** 
# 
# There appears to be no real relationship between latitude and wind speed.  The wind speed varies greatly 
# between 0 and 10 for all latitudes.  Wind speeds between 10 and 15 are present for nearly all latitudes, 
# but are less prevalent close to the equator.  The largest wind speeds were for cities far from the equator.  
# Only one city in the northern hemisphere and one in the southern hemisphere had wind speed above 20.  Both 
# of these cities are beyond 50 degrees North or South of the equator.





