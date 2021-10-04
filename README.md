## CitiBike Dock Availability

New York City's bike share program is a powerful transportation upgrade for the city. When a Citibike station was deployed in front of my apartment building, it shaved fifteen minutes off my commute every day. Over the course of a year, this amounted to a time savings of around 50 hours.

However, there were multiple times where my efforts to save time backfired. If the station where you end your trip is completely filled with bikes, you are in a bit of jam. 

Simply abandoning the bike can result in a $1,200 charge. Trying your luck at another station carries risk as well. In high-traffic areas there may be bike saturation for the whole cluster of stations in the area. If you set out to try another station, you would also lose your place in line at the first station. If you decide to wait it out, you are at the mercy of the scruples of others who may decide that this will be one of the few areas in our society where queueing will not be used to determine priority.

There has to be a better way!

# The Tool this City Deserves

Any sort of insight into whether there is likely to be an available dock at your destination could be useful in planning your trips. With enough data some trends will hopefully emerge.

# Data Sources

Citibike provides two sources of public data which could be used to solve the problem. 

The first source are the monthly trip reports which provide detailed records of every trip, defined as a customer taking a bike out for longer than 60 seconds.

The second source is the live JSON feed of the entire system. This includes information like the name and location of each station, the amount of bikes at every station, and the amount of *open docks* at every station.

# Data Collection

Since the monthly reports only really need to be collated once, the Jupyter notebook TripData.ipnyb in the root directory of this repository is all you need to build your own dataset of trips spanning years. 

[Here is the link for a ready-to-run Colab Notebook version.](https://colab.research.google.com/github/DonRomaniello/CitibikeDocks/blob/master/TripData.ipynb)

A small AWS EC2 Instance running the scripts in the Scraping directory has been polling the JSON feed of the CitiBike system every 60 seconds for over a year.

# Preliminary Analysis
![One Week of Docks Data]
(https://raw.githubusercontent.com/DonRomaniello/CitibikeDocks/master/Graphs/17012020.png)

This graph represents one week of dock availability in early 2020. Even with hundreds of stations represented, some patterns of activity emerge. Notice the patches of white peaking through when the change in dock availability tapers off overnight. This is due to reduced ridership at night, meaning the stations are not experiencing as much change in availability. Thus, the lines representing the amount of available docks will be relatively straight instead of tangled and crossed.
