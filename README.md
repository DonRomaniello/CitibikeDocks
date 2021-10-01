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

