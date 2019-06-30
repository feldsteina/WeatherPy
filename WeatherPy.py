# %% [markdown]
# # WeatherPy
# ----
#
# ### Analysis
# * As expected, the weather becomes significantly warmer
# as one approaches the equator (0 Deg. Latitude).
# More interestingly, however, is the fact that the southern hemisphere
# tends to be warmer this time of year than the northern hemisphere.
# This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness.
# However, it is interesting to see that a strong band of cities sits at
# 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed.
# However, in northern hemispheres there is a flurry of cities
# with over 20 mph of wind.
#
# ---
#
# #### Note
# * Instructions have been included for each segment.
# You do not have to follow them exactly,
# but they are included to help you think through the steps.

# %%
# Dependencies and Setup
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
from time import sleep

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# %% [markdown]
# ## Generate Cities List

# %%
# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

# %% [markdown]
# ### Perform API Calls
# * Perform a weather check on each city
# using a series of successive API calls.
# * Include a print log of each city
# as it's being processed (with the city number and city name).
#
url = f"https://api.openweathermap.org/data/2.5/weather\
?appid={api_key}&units=imperial&q="
temps = []
wind = []
humidity = []
cloudiness = []
latitude = []
city_list = []

i = 0

for city in cities:
    try:
        response = requests.get(url + f"{city}")
        print(response.url)
        print(f"Getting data for {city}")

        data = json.loads(response.text)
        pretty_data = json.dumps(data, sort_keys=True, indent=4)
        print(f"City {i} of {len(cities)}")

        temps.append(data["main"]["temp"])
        wind.append(data["wind"]["speed"])
        humidity.append(data["main"]["humidity"])
        cloudiness.append(data["clouds"]["all"])
        latitude.append(data["coord"]["lat"])
        city_list.append(city)
        i = i + 1
    except:
        print("Failed")
        pass

    sleep(1.1)

    # limit while testing:
    # if i > 99:
    #     break

# %%
# i = 0
# for item in temps:
#     i = i+1
#     print(f"Temp {i}: {item}")

# %%
# i = 0
# for item in wind:
#     i = i+1
#     print(f"Wind {i}: {item}")

# %%
# i = 0
# for item in humidity:
#     i = i+1
#     print(f"Humid {i}: {item}")

# %%
# i = 0
# for item in cloudiness:
#     i = i+1
#     print(f"Clouds {i}: {item}")

# %%
# i = 0
# for item in latitude:
#     i = i+1
#     print(f"Lat {i}: {item}")

# %%
# i = 0
# for item in city_list:
#     i = i+1
#     print(f"City {i}: {item}")

# %% [markdown]
# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# %%
weather_df = pd.DataFrame(
    {"city": city_list,
     "lat": latitude,
     "temp": temps,
     "humidity": humidity,
     "wind": wind,
     "clouds": cloudiness
     }
)

weather_df.to_csv("weather.csv")


# %%
weather_df.head()

# %% [markdown]
# ### Plotting the Data
# * Use proper labeling of the plots
# using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.
# %% [markdown]
# #### Latitude vs. Temperature Plot

# %%
now = datetime.datetime.now()
date = f"{now.year}-{now.month}-{now.day}"
# %%
x = weather_df["lat"]
y = weather_df["temp"]
plt.scatter(x, y)
plt.xlabel("Latitude (Degrees)")
plt.ylabel("Temperature (F)")
plt.title(f"Latitude vs Temperature on {date}")
plt.savefig("analysis/temp.png")
plt.show()


# %% [markdown]
# #### Latitude vs. Humidity Plot

# %%
x = weather_df["lat"]
y = weather_df["humidity"]
plt.scatter(x, y)
plt.xlabel("Latitude (Degrees)")
plt.ylabel("Humidity (%)")
plt.title(f"Latitude vs Humidity on {date}")
plt.savefig("analysis/humidity.png")
plt.show()


# %% [markdown]
# #### Latitude vs. Cloudiness Plot

# %%

x = weather_df["lat"]
y = weather_df["clouds"]
plt.scatter(x, y)
plt.xlabel("Latitude (Degrees)")
plt.ylabel("Cloud Cover (%)")
plt.title(f"Latitude vs Cloud Cover on {date}")
plt.savefig("analysis/clouds.png")
plt.show()


# %% [markdown]
# #### Latitude vs. Wind Speed Plot

# %%

x = weather_df["lat"]
y = weather_df["wind"]
plt.scatter(x, y)
plt.xlabel("Latitude (Degrees)")
plt.ylabel("Wind speed (MPH)")
plt.title(f"Latitude vs Wind on {date}")
plt.savefig("analysis/wind.png")
plt.show()

# %%
