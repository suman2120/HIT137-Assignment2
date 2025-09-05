import pandas as pd
import glob  #used to get all csv files automatically

#Read all CSV files from "temperatures" folder
all_csv_files = glob.glob("ques2/temperatures/*.csv") 

all_dataframes = []  # temporary list to store each csv as a dataframe

for file in all_csv_files:
    df = pd.read_csv(file)   #read csv file
    all_dataframes.append(df)

data = pd.concat(all_dataframes, ignore_index=True)  #merge all csv into one dataframe

#Convert months to numeric
months = ['January', 'February', 'March','April','May','June','July','August','September',
          'October','November','December']
for month in months:
    data[month] = pd.to_numeric(data[month], errors='coerce')  #convert columns to numbers, ignore NaN values

#Define Australian seasons
seasons = {
    'Summer': ['December','January','February'],
    'Autumn': ['March','April','May'],
    'Winter': ['June','July','August'],
    'Spring': ['September','October','November']
}

seasonal_avg = {}
for season, month_list in seasons.items():
    seasonal_avg[season] = data[month_list].stack().mean()  #average per season across all stations

with open('ques2/average_temp.txt','w') as f:  
    for season, avg in seasonal_avg.items():
        f.write(f'{season}: {avg:.2f} degree celsius\n') # save seasonal average in required format

data['MaximumTemperature'] = data[months].max(axis=1) # maximum temperature per station across all months

data['MinimumTemperature'] = data[months].min(axis=1) # minimum temperature per station across all months
data['TemperatureRange'] = data['MaximumTemperature'] - data['MinimumTemperature'] # temperature range per station


max_range = data['TemperatureRange'].max()
largest_range_stations = data[data['TemperatureRange'] == max_range] # get stations with the largest range


with open('ques2/largest_temp_range_station.txt', 'w') as f:  
    for _, row in largest_range_stations.iterrows():
        f.write(
            f"Station {row['STATION_NAME']}: Range {row['TemperatureRange']:.2f} degree celsius "
            f"(Max: {row['MaximumTemperature']:.2f} degree celsius, "
            f"Min: {row['MinimumTemperature']:.2f} degree celsius)\n") # save in required format

data['StandardDeviation'] = data[months].std(axis=1) # standard deviation per station to measure stability

max_std = data['StandardDeviation'].max() # largest stddev means most variable
min_std = data['StandardDeviation'].min() # smallest stddev mean most stable


most_stable = data[data['StandardDeviation'] == min_std] # get most stable stations

most_variable = data[data['StandardDeviation'] == max_std] #get most variable stations

with open('ques2/temperature_stability_station.txt','w') as f:   
    for i, row in most_stable.iterrows():
        f.write(f"Most Stable: Station {row['STATION_NAME']}: StdDev {row['StandardDeviation']:.2f} degree celsius\n")
    for i, row in most_variable.iterrows():
        f.write(f"Most Variable: Station {row['STATION_NAME']}: StdDev {row['StandardDeviation']:.2f} degree celsius\n")



