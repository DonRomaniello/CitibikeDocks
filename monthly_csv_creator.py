# -*- coding: utf-8 -*-
"""Monthly_CSV_Creator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w6g3Ji4hVgK3rJDz5b4UBOGX1mqK65Gt
"""

import pandas as pd
import time

import os
import tarfile

import json

#Set initial directory as the directory where the script is running.

initial_directory = '.'
os.chdir(initial_directory)
print("Current working directory is", os.getcwd())

# Select directories

directory_prompt_selection = 'none'

while directory_prompt_selection != 'w':
  current_directories = [d for d in os.listdir('.') if os.path.isdir(d)]

  print("Current working directory is", os.getcwd())

  for directory in current_directories:

    print(current_directories.index(directory), directory)

  print("w", "We can use current directory")
  print("c", "Change top level directory")
  print("u", "Navigate up one level.")
  directory_prompt_selection = input("Choose an option:")
  print("\n")
  
  if directory_prompt_selection == 'c':
    directory_prompt_selection = input('Provide either the relative or full path name of the directory')
    os.chdir(directory_prompt_selection)
  elif directory_prompt_selection == 'u':
    os.chdir('../')
  elif directory_prompt_selection == 'w':
    None
  else:
    os.chdir(os.path.join('.', current_directories[int(directory_prompt_selection)]))

print("Current working directory is", os.getcwd())

# Get rid of anything the operating system may add...
files = ([x for x in sorted(filter(os.path.isfile,
                                   os.listdir('.')),
                                   key=os.path.getmtime) if x[-2:] == "xz"])

files

# Start some timers to track how long everything is taking.

stopwatch_start = time.time()
stopwatch_hour = time.time()

stations_big = pd.DataFrame()


files_by_month = [x for x in sorted(filter(os.path.isfile,
                                          os.listdir('.')),
                                    key=os.path.getmtime) if x[-2:] == "xz"]


hour = tarfile.open('./' + files_by_month[0])
hour_list = hour.getnames()

# To avoid losing an entire hour when the JSON file is empty or misformed, using
# minute to index into a list.

minute = 0
minute_json = json.load(hour.extractfile(hour_list[minute]))
timestamp = minute_json["last_updated"]
stations_tick = (pd.DataFrame(minute_json['data']['stations'])
                [['station_id', 'num_docks_available']]
                .rename(columns={'num_docks_available':timestamp})
                .astype('int16')
                .set_index('station_id')
                .sort_index()[timestamp])

minute+=1

minute_json = json.load(hour.extractfile(hour_list[minute]))
timestamp = minute_json["last_updated"]
stations_tock = (pd.DataFrame(minute_json['data']['stations'])
                [['station_id', 'num_docks_available']]
                .rename(columns={'num_docks_available':timestamp})
                .astype('int16')
                .set_index('station_id')
                .sort_index()[timestamp])

stations_tick = pd.concat([stations_tick, stations_tock], join="outer", axis=1)

# Initial dataframe has been built. Now it is time to loop the first hour.

minute+=1
while minute < len(hour_list):
  try:
    minute_json = json.load(hour.extractfile(hour_list[minute]))
    timestamp = minute_json["last_updated"]

    stations_tock = (pd.DataFrame(minute_json['data']['stations'])
              [['station_id', 'num_docks_available']]
              .rename(columns={'num_docks_available':timestamp})
              .astype('int16')
              .set_index('station_id')
              .sort_index()[timestamp])

    if stations_tick.index.equals(stations_tock.index):
      stations_tick.insert((stations_tick.shape[1]), timestamp, stations_tock)
    else:
      stations_tick = pd.concat([stations_tick,stations_tock],
                            join='outer',
                            axis=1)

    minute+=1
  except json.JSONDecodeError:
    minute+=1
    print(stations_tick.shape)    

print(time.time() - stopwatch_hour)
stopwatch_hour = time.time()

# Build out month, hour by hour, day by day

for hour_xz in files_by_month[1:]:
  hour = tarfile.open('./' + hour_xz)
  hour_list = hour.getnames()
  minute=0

  print(stations_tick.shape)    
  print(time.time() - stopwatch_hour)
  stopwatch_hour = time.time()

  while minute < len(hour_list):
    try:
      minute_json = json.load(hour.extractfile(hour_list[minute]))
      timestamp = minute_json["last_updated"]

      stations_tock = (pd.DataFrame(minute_json['data']['stations'])
                [['station_id', 'num_docks_available']]
                .rename(columns={'num_docks_available':timestamp})
                .astype('int16')
                .set_index('station_id')
                .sort_index()[timestamp])

      if stations_tick.index.equals(stations_tock.index):
        stations_tick.insert((stations_tick.shape[1]), timestamp, stations_tock)
      else:
        stations_tick = pd.concat([stations_tick,stations_tock],
                              join='outer',
                              axis=1)

# There is a HUGE slowdown once 1440 columns (24 hours of minutes) is reached.
# By building dataframes day by day and then merging once a day, well over 25
# times faster excution is achieved.


      if stations_tick.shape[1] > 1440:
        stations_big = pd.concat([stations_big, stations_tick], join='outer', axis=1)
        stations_tick = pd.DataFrame(index=stations_tick.index)
      else:
        pass

      minute+=1
    except json.JSONDecodeError:
      minute+=1


# Finally, print how long this whole thing took.

stopwatch_end = time.time()
print((stopwatch_end - stopwatch_start), 
      " seconds, or ",
      ((stopwatch_end - stopwatch_start)/60),
      " minutes elapsed.")

# Save, and brag about it.
stations_big.to_csv(('./' + os.getcwd().split('/')[-1] + '.csv.gzip'))

print((os.getcwd() + os.getcwd().split('/')[-1] + 'csv.gzip'), " saved.")
