# python-api-challenge
What if you wanted to travel to the global location with the perfect weather conditions?  You would need to determine what your perfect weather conditions are, and you would need to research weather conditions around the globe.  And you would likely want to find out if there is a hotel in that location!

In this challenge, random geographic coordinates were generated, and the city nearest each set of random coordinates was determined using the citypy library.  For each of these cities, the openweather API was called to provide current weather conditions.

Visualizations were then created to ccompare weather conditions vs. Latitude and lindar regressions were cretaed to explore any possible relationships.  Weather and location data were exported to a csv file.

In the follow-up VacationPy.py file, the weather and location data were imported and the cities were mapped using hvplot.  Geoapify API was called to find the nearest hotel to each of the coordinates, and a new dataframe was created and exported to a csv file. Hotel names were added to the map upon hovering.




