# _*_ coding utf-8 _*_
# 开发团队：电气自动化技术X班
# 开发人员：84486
# 开发时间：2023/7/23 15:49
# 文件名称：write_paper_Beijing.py
# 开发工具：PyCharm
# 程序内容：
##########################计算最冷月和最热月#######################################
#########################最冷月和最热月########################################
'''
import pandas as pd
# Load the data from the CSV file to dataframe
data = pd.read_csv('20020101_20211231_beijing.csv')
# Group by month and calculate the average temperature and Keep one decimal place
monthly_avg_temperature = round(data.groupby('MO')['T2M'].mean(),1)
# Find the Month with the minimum and maximum average temperature
min_avg_temp_month = monthly_avg_temperature.idxmin()
max_avg_temp_month = monthly_avg_temperature.idxmax()
# Find the minimum and maximum average temperatures
min_avg_temp = monthly_avg_temperature.min()
max_avg_temp = monthly_avg_temperature.max()
# Print the results
print(f"最小平均温度所在的月份: {min_avg_temp_month}")
print(f"最小平均温度: {min_avg_temp:.1f} °C")
print(f"最大平均温度所在的月份: {max_avg_temp_month}")
print(f"最大平均温度: {max_avg_temp:.1f} °C")
'''
#########################计算采暖期干球温度########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Step 1: Sort the 'T2M' column in descending order
sorted_data = data.sort_values(by='T2M', ascending=False)
# Step 2: Calculate the values corresponding to the specified percentiles
percentiles = {99.6: '99.6%',  99: '99%' }
# Calculate the indexes for the specified percentiles (rounded to the nearest integer)
percentile_indexes = {percentile: int(len(sorted_data) * (percentile / 100)) for percentile in percentiles}
# Extract the values corresponding to the percentiles
percentile_values = {percentiles[percentile]: sorted_data.iloc[index]['T2M'] for percentile, index in percentile_indexes.items()}
# Step 3: Print the results
for percentile, value in percentile_values.items():
    print(f"排名为{percentile}的T2M值为: {value:.1f} °C")
'''
################################计算湿球温度#################################
'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Function to calculate wet-bulb temperature (WB2M)
def calculate_wb2m(row):
    t2m = row['T2M']+273.15  # Dry-bulb temperature in Celsius
    rh2m = row['RH2M'] / 100  # Convert relative humidity to a ratio (divide by 100)
    ps = row['PS'] * 1000  # Convert atmospheric pressure to Pa (multiply by 1000)
    # Calculate wet-bulb temperature (WB2M) using CoolProp
    wb2m = HAPropsSI('Twb', 'T', t2m, 'R', rh2m, 'P', ps)
    # Convert the result from Kelvin to Celsius
    wb2m_celsius = wb2m - 273.15
    return round(wb2m_celsius, 2)
# Calculate wet-bulb temperature for each row and add it as a new column
data['WB2M'] = data.apply(calculate_wb2m, axis=1)
# Save the updated DataFrame back to the CSV file
data.to_csv('20020101_20211231_beijing.csv', index=False)
'''
################################计算露点温度#################################
'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Function to calculate dew point temperature (DP2M)
def calculate_dp2m(row):
    t2m = row['T2M']+273.15  # Dry-bulb temperature in Celsius
    rh2m = row['RH2M'] / 100  # Convert relative humidity to a ratio (divide by 100)
    ps = row['PS'] * 1000  # Convert atmospheric pressure to Pa (multiply by 1000)
    # Calculate dew point temperature (DP2M) using CoolProp
    dp2m = HAPropsSI('Tdp', 'T', t2m, 'R', rh2m, 'P', ps)
    # Convert the result from Kelvin to Celsius
    dp2m_celsius = dp2m - 273.15
    return round(dp2m_celsius,2)
# Calculate dew point temperature for each row and add it as a new column
data['DP2M'] = data.apply(calculate_dp2m, axis=1)
# Save the updated DataFrame back to the CSV file
data.to_csv('20020101_20211231_beijing.csv', index=False)
'''

##############################计算含湿量g/kg dry-air ########################################
'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Function to calculate humidity ratio (HuRadio2M)
def calculate_humidity_ratio(row):
    t2m = row['T2M']+273.15 # Dry-bulb temperature in Celsius
    rh2m = row['RH2M'] / 100  # Convert relative humidity to a ratio (divide by 100)
    ps = row['PS'] * 1000  # Convert atmospheric pressure to Pa (multiply by 1000)
    # Calculate humidity ratio (HuRadio2M) using CoolProp
    h2m = HAPropsSI('H', 'T', t2m, 'R', rh2m, 'P', ps)
    w2m = HAPropsSI('W', 'T', t2m, 'R', rh2m, 'P', ps)
    # Calculate humidity ratio (HuRadio2M) by dividing specific humidity by 1 - specific humidity
    hu_radio_2m = w2m / (1 - w2m)
    return round(hu_radio_2m*1000,2)
# Calculate humidity ratio for each row and add it as a new column
data['HuRadio2M'] = data.apply(calculate_humidity_ratio, axis=1)
# Save the updated DataFrame back to the CSV file
data.to_csv('20020101_20211231_beijing.csv', index=False)
'''
################################计算比焓重新计算 单位kJ/kg dry-air#################################
'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Function to calculate Enthalpy2M
def calculate_enthalpy(row):
    t2m = row['T2M']  # Dry-bulb temperature in Celsius
    rh2m = row['RH2M'] / 100  # Convert relative humidity to a ratio (divide by 100)
    ps = row['PS'] * 1000  # Convert atmospheric pressure to Pa (multiply by 1000)
    h2m = row['HuRadio2M']  # Humidity ratio in g/kg
    # Calculate the specific enthalpy (kJ/kg dry-air) using CoolProp
    enthalpy = HAPropsSI('H', 'T', t2m + 273.15, 'R', rh2m, 'P', ps) * 0.001  # Convert from J/kg to kJ/kg
    # Calculate the enthalpy including the humidity (kJ/kg dry-air)
    enthalpy_with_humidity = enthalpy + h2m
    return round(enthalpy_with_humidity, 3)
# Calculate Enthalpy2M for each row and add it as a new column
data['Enth2M'] = data.apply(calculate_enthalpy, axis=1)
# Save the updated DataFrame back to the CSV file
data.to_csv('20020101_20211231_beijing.csv', index=False)
'''

###########################制冷干球温度和对应湿球温度###########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Step 1: Sort the 'T2M' column in descending order
sorted_data_t2m = data.sort_values(by='T2M', ascending=False)
# Step 2: Calculate the values corresponding to the specified percentiles
percentiles = [0.4, 1, 2]
percentile_labels = ['0.4%', '1%', '2%']
percentile_values_t2m = {}
for percentile in percentiles:
    # Calculate the index for the current percentile (rounded to the nearest integer)
    percentile_index = int(len(sorted_data_t2m) * (percentile / 100))
    # Extract the value corresponding to the current percentile
    percentile_values_t2m[percentile_labels[percentiles.index(percentile)]] = sorted_data_t2m.iloc[percentile_index]['T2M']
# Step 3: Find the corresponding 'WB2M' values for each percentile and calculate the average 'WB2M'
t2m_data_0_4 = sorted_data_t2m[sorted_data_t2m['T2M'] == percentile_values_t2m['0.4%']]
t2m_data_1 = sorted_data_t2m[sorted_data_t2m['T2M'] == percentile_values_t2m['1%']]
t2m_data_2 = sorted_data_t2m[sorted_data_t2m['T2M'] == percentile_values_t2m['2%']]
average_wb2m_0_4 = t2m_data_0_4['WB2M'].mean()
average_wb2m_1 = t2m_data_1['WB2M'].mean()
average_wb2m_2 = t2m_data_2['WB2M'].mean()
# Step 4: Output the results
for percentile_label in percentile_labels:
    print(f"排名为{percentile_label}的T2M值为: {percentile_values_t2m[percentile_label]:.2f} °C")
print(f"排名为0.4%的T2M对应的平均湿球温度WB2M为: {average_wb2m_0_4:.2f} °C")
print(f"排名为1%的T2M对应的平均湿球温度WB2M为: {average_wb2m_1:.2f} °C")
print(f"排名为2%的T2M对应的平均湿球温度WB2M为: {average_wb2m_2:.2f} °C")
'''
##############################供暖期空气加湿用含湿量、露点温度和对应的平均干球温度 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Step 1: Sort the data by DP2M in descending order
sorted_data_dp = data.sort_values(by='DP2M', ascending=False)
# Step 2: Calculate the values corresponding to the 99.6% and 99% percentiles for DP2M
percentiles_dp = {99.6: int(len(sorted_data_dp) * 0.996) , 99: int(len(sorted_data_dp) * 0.99)}
percentile_values_dp = {
    percentile: sorted_data_dp.iloc[index ]['DP2M'] for percentile, index in percentiles_dp.items()}
# Step 3: Calculate the average T2M for each percentile of DP2M
mean_t2m_by_dp2m = {}
for percentile, dp2m in percentile_values_dp.items():
    t2m_values = sorted_data_dp[sorted_data_dp['DP2M'] == dp2m]['T2M']
    mean_t2m_by_dp2m[percentile] = t2m_values.mean()
# Step 4: Sort the data by HuR2M in descending order
sorted_data_hu = data.sort_values(by='HuRadio2M', ascending=False)
# Step 5: Calculate the values corresponding to the 99.6% and 99% percentiles for HuR2M
percentiles_hu = {99.6: int(len(sorted_data_hu) * 0.996) , 99: int(len(sorted_data_hu) * 0.99)}
percentile_values_hu = {
    percentile: sorted_data_hu.iloc[index ]['HuRadio2M'] for percentile, index in percentiles_hu.items()}
# Step 6: Output the results
print("99.6% 和 99% 的露点温度对应的平均干球温度：")
for percentile, t2m_mean in mean_t2m_by_dp2m.items():
    dp2m = percentile_values_dp[percentile]
    hu_r = percentile_values_hu[percentile]
    print(f"{percentile:.1f}% 的露点温度为 {dp2m:.2f} °C，对应的平均干球温度为 {t2m_mean:.1f} °C，对应的含湿量为 {hu_r:.1f}")

'''
##############################制冷期除湿用含湿量、露点温度和对应的平均干球温度 ########################################
'''import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Step 1: Sort the data by DP2M in descending order
sorted_data_dp = data.sort_values(by='DP2M', ascending=False)
# Step 2: Calculate the values corresponding to the 99.6% and 99% percentiles for DP2M
percentiles_dp = {0.4: int(len(sorted_data_dp) * 0.004) , 1: int(len(sorted_data_dp) * 0.01) ,2: int(len(sorted_data_dp) * 0.02)}
percentile_values_dp = {
    percentile: sorted_data_dp.iloc[index ]['DP2M'] for percentile, index in percentiles_dp.items()}
# Step 3: Calculate the average T2M for each percentile of DP2M
mean_t2m_by_dp2m = {}
for percentile, dp2m in percentile_values_dp.items():
    t2m_values = sorted_data_dp[sorted_data_dp['DP2M'] == dp2m]['T2M']
    mean_t2m_by_dp2m[percentile] = t2m_values.mean()
# Step 4: Sort the data by HuR2M in descending order
sorted_data_hu = data.sort_values(by='HuRadio2M', ascending=False)
# Step 5: Calculate the values corresponding to the 99.6% and 99% percentiles for HuR2M
percentiles_hu = {0.4: int(len(sorted_data_dp) * 0.004) , 1: int(len(sorted_data_dp) * 0.01) ,2: int(len(sorted_data_dp) * 0.02)}
percentile_values_hu = {
    percentile: sorted_data_hu.iloc[index ]['HuRadio2M'] for percentile, index in percentiles_hu.items()}
# Step 6: Output the results
for percentile, t2m_mean in mean_t2m_by_dp2m.items():
    dp2m = percentile_values_dp[percentile]
    hu_r = percentile_values_hu[percentile]
    print(f"{percentile:.1f}% 的露点温度为 {dp2m:.2f} °C，对应的平均干球温度为 {t2m_mean:.1f} °C，对应的含湿量为 {hu_r:.1f}")'''

##############################采暖期加湿和制冷期除湿用含湿量、露点温度和对应的平均干球温度 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Task 1: Sort 'HuRadio2M' (specific enthalpy) in descending order
sorted_data_hu_radio = data.sort_values(by='HuRadio2M', ascending=False)
# Task 2: Calculate percentiles for 'HuRadio2M' (specific enthalpy)
percentiles_hu_radio = [0.4, 1, 2, 99.6, 99]
percentiles_values_hu_radio = {percentile: sorted_data_hu_radio['HuRadio2M'].iloc[int(len(sorted_data_hu_radio) * (percentile / 100))] for percentile in percentiles_hu_radio}
# Task 3: Sort 'DP2M' (dew point temperature) in descending order
sorted_data_dp = data.sort_values(by='DP2M', ascending=False)
# Task 4: Calculate percentiles for 'DP2M' (dew point temperature)
percentiles_dp = [0.4, 1, 2, 99.6, 99]
percentiles_values_dp = {percentile: sorted_data_dp['DP2M'].iloc[int(len(sorted_data_dp) * (percentile / 100))] for percentile in percentiles_dp}
# Task 5: Calculate average 'T2M' (dry-bulb temperature) for different percentiles of 'DP2M'
average_t2m_for_dp_percentiles = {}
for percentile in percentiles_dp:
    dp_value = percentiles_values_dp[percentile]
    temp_data =round(sorted_data_dp[sorted_data_dp['DP2M'] == dp_value],1)
    average_t2m =round( temp_data['T2M'].mean(),2)
    average_t2m_for_dp_percentiles[percentile] = average_t2m
# Output results
print("Percentiles for HuRadio2M:",percentiles_values_hu_radio)
print("Percentiles for DP2M:",percentiles_values_dp)
print("Average T2M for different percentiles of DP2M:",average_t2m_for_dp_percentiles)
'''
##############################制冷期蒸发用湿球温度和对应的平均干球温度 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Step 1: Sort the 'WB2M' column in descending order
sorted_data_wb2m = data.sort_values(by='WB2M', ascending=False)
# Step 2: Calculate the values corresponding to the specified percentiles
percentiles = [0.4, 1, 2]
percentile_labels = ['0.4%', '1%', '2%']
percentile_values_wb2m = {}
for percentile in percentiles:
    # Calculate the index for the current percentile (rounded to the nearest integer)
    percentile_index = int(len(sorted_data_wb2m) * (percentile / 100))
    # Extract the value corresponding to the current percentile
    percentile_values_wb2m[percentile_labels[percentiles.index(percentile)]] = sorted_data_wb2m.iloc[percentile_index]['WB2M']
# Step 3: Find the corresponding 'T2M' values for each percentile and calculate the average 'T2M'
wb2m_data_0_4 = sorted_data_wb2m[sorted_data_wb2m['WB2M']== percentile_values_wb2m['0.4%']]
wb2m_data_1 = sorted_data_wb2m[sorted_data_wb2m['WB2M'] == percentile_values_wb2m['1%']]
wb2m_data_2 = sorted_data_wb2m[sorted_data_wb2m['WB2M'] == percentile_values_wb2m['2%']]
average_t2m_0_4 = wb2m_data_0_4['T2M'].mean()
average_t2m_1 = wb2m_data_1['T2M'].mean()
average_t2m_2 = wb2m_data_2['T2M'].mean()
# Step 4: Output the results
for percentile_label in percentile_labels:
    print(f"排名为{percentile_label}的湿球温度WB2M值为: {percentile_values_wb2m[percentile_label]:.2f} °C")
print(f"排名为0.4%的湿球温度WB2M对应的平均干球温度T2M为: {average_t2m_0_4:.2f} °C")
print(f"排名为1%的湿球温度WB2M对应的平均干球温度T2M为: {average_t2m_1:.2f} °C")
print(f"排名为2%的湿球温度WB2M对应的平均干球温度T2M为: {average_t2m_2:.2f} °C")
'''
##############################制冷期新风用比焓和对应的平均干球温度 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Task 1: Sort 'Enth2M' column in descending order
sorted_data = data.sort_values(by='Enth2M', ascending=False)
# Task 2: Calculate the 0.4%, 1%, and 2% percentiles for 'Enth2M'
percentile_0_4 = 0.4
percentile_1 = 1
percentile_2 = 2
enth_0_4 = sorted_data['Enth2M'].quantile(1 - percentile_0_4 / 100)
enth_1 = sorted_data['Enth2M'].quantile(1 - percentile_1 / 100)
enth_2 = sorted_data['Enth2M'].quantile(1 - percentile_2 / 100)
# Round the percentiles to the nearest integer
enth_0_4 = int(round(enth_0_4))
enth_1 = int(round(enth_1))
enth_2 = int(round(enth_2))
# Task 3: Find the corresponding 'T2M' values for each percentile and calculate the average 'T2M'
t2m_data_0_4 = sorted_data[sorted_data['Enth2M'] >= enth_0_4]
t2m_data_1 = sorted_data[sorted_data['Enth2M'] >= enth_1]
t2m_data_2 = sorted_data[sorted_data['Enth2M'] >= enth_2]
average_t2m_0_4 = t2m_data_0_4['T2M'].mean()
average_t2m_1 = t2m_data_1['T2M'].mean()
average_t2m_2 = t2m_data_2['T2M'].mean()
# Task 4: Output the results
print(f"Percentile 0.4%: Enth2M = {enth_0_4}, Average T2M = {average_t2m_0_4:.2f}")
print(f"Percentile 1%: Enth2M = {enth_1}, Average T2M = {average_t2m_1:.2f}")
print(f"Percentile 2%: Enth2M = {enth_2}, Average T2M = {average_t2m_2:.2f}")
'''

##############################最冷月风速和对应的平均干球温度 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Task 1: Sort 'WS10M' (wind speed at 10 meters) when MO=1 in descending order
sorted_data_ws10m = data[data['MO'] == 1].sort_values(by='WS10M', ascending=False)
# Task 2: Calculate percentiles for 'WS10M' (wind speed at 10 meters)
percentiles_ws10m = [0.4, 1]
percentiles_values_ws10m = {percentile: sorted_data_ws10m['WS10M'].iloc[int(len(sorted_data_ws10m) * (percentile / 100))] for percentile in percentiles_ws10m}
# Task 3: Calculate average 'T2M' (dry-bulb temperature) for different percentiles of 'WS10M'
average_t2m_for_ws10m_percentiles = {}
for percentile in percentiles_ws10m:
    ws10m_value = percentiles_values_ws10m[percentile]
    temp_data = sorted_data_ws10m[sorted_data_ws10m['WS10M'] == ws10m_value]
    average_t2m = temp_data['T2M'].mean()
    average_t2m_for_ws10m_percentiles[percentile] = round(average_t2m,2)
# Output results
print("Percentiles for WS10M:")
print(percentiles_values_ws10m)
print("Average T2M for different percentiles of WS10M:")
print(average_t2m_for_ws10m_percentiles)
'''
##############################采暖期和供冷期平均风速和最频繁风向 ########################################
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('20020101_20211231_beijing.csv')
# Sort the data by 'T2M' in descending order
sorted_data_t2m = data.sort_values(by='T2M', ascending=False)
# Calculate the index position corresponding to the percentiles
index_0_4 = int(len(sorted_data_t2m) * 0.4 / 100)
index_99_6 = int(len(sorted_data_t2m) *99.6 / 100)
# Get the T2M values corresponding to the percentiles
t2m_0_4 = sorted_data_t2m.iloc[index_0_4]['T2M']
t2m_99_6 = sorted_data_t2m.iloc[index_99_6]['T2M']
# Task 3: Find the average 'WS10M' (wind speed) for T2M equals to 0.4% and 99.6%
t2m_data_0_4 = sorted_data_t2m[sorted_data_t2m['T2M'] == t2m_0_4]
t2m_data_99_6 = sorted_data_t2m[sorted_data_t2m['T2M'] == t2m_99_6]
average_ws_0_4 = t2m_data_0_4['WS10M'].mean()
average_ws_99_6 = t2m_data_99_6['WS10M'].mean()
# Task 4: Find the most frequent wind direction for T2M equals to 0.4% and 99.6%
most_frequent_wd_0_4 = t2m_data_0_4['WD10M'].mode().iloc[0]
most_frequent_wd_99_6 = t2m_data_99_6['WD10M'].mode().iloc[0]
# Output the results
print(f"0.4% percentile of T2M: {t2m_0_4:.2f}")
print(f"99.6% percentile of T2M: {t2m_99_6:.2f}")
print(f"Average wind speed for T2M = 0.4% percentile: {average_ws_0_4:.2f} m/s")
print(f"Average wind speed for T2M = 99.6% percentile: {average_ws_99_6:.2f} m/s")
print(f"Most frequent wind direction for T2M = 0.4% percentile: {most_frequent_wd_0_4}")
print(f"Most frequent wind direction for T2M = 99.6% percentile: {most_frequent_wd_99_6}")

'''
########################################Coldest Month
'''
import pandas as pd
# Read the Beijing.csv file
df = pd.read_csv('Beijing.csv')
# Calculate the monthly average dry bulb temperature
monthly_avg_temp = df.groupby('MO')['T2M'].mean()
# Find the month with the lowest average temperature
min_avg_temp_month = monthly_avg_temp.idxmin()
lowest_avg_temp = monthly_avg_temp.min()
# Print the results
print("Monthly Average Temperatures:")
print(monthly_avg_temp)
print(f"Month with Lowest Average Temperature: {min_avg_temp_month}")
print(f"Lowest Average Temperature: {lowest_avg_temp:.2f} °C")
'''
'''
import pandas as pd

# List of file names
file_names = ['Beijing.csv', 'Fuzhou.csv', 'Guangzhou.csv', 'Harbin.csv', 'Shanghai.csv', 'Shenyang.csv']

# Loop through each file and process data
for filename in file_names:
    city_name = filename.split('.')[0]
    df = pd.read_csv(filename)

    # Calculate the monthly average dry bulb temperature
    monthly_avg_temp = df.groupby('MO')['T2M'].mean()

    # Find the month with the lowest average temperature
    min_avg_temp_month = monthly_avg_temp.idxmin()
    lowest_avg_temp = monthly_avg_temp.min()

    # Print the results for each city
    print(f"City: {city_name}")
    # print("Monthly Average Temperatures:")
    # print(monthly_avg_temp)
    print(f"Month with Lowest Average Temperature: {min_avg_temp_month}")
    print(f"Lowest Average Temperature: {lowest_avg_temp:.2f} °C")
    print()
'''
'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI

# List of city CSV files
city_files = ['Harbin.csv', 'Shenyang.csv', 'Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']

# Loop through each city file
for city_file in city_files:
    # Read the city CSV file
    df = pd.read_csv(city_file)


    # Calculate the properties and add them to the dataframe
    def calculate_properties(row):
        T2M = row['T2M']
        RH2M = row['RH2M'] / 100  # Convert relative humidity to a fraction
        P = row['PS'] * 1000  # Convert pressure from kPa to Pa
        WB2M = HAPropsSI('Twb', 'T', T2M + 273.15, 'P', P, 'R', RH2M) - 273.15
        DP2W = HAPropsSI('Tdp', 'T', T2M + 273.15, 'P', P, 'R', RH2M) - 273.15
        HuRadio2M = HAPropsSI('W', 'T', T2M + 273.15, 'P', P, 'R', RH2M)
        Enth2M = HAPropsSI('H', 'T', T2M + 273.15, 'P', P, 'R', RH2M) / 1000  # Convert to kJ/kg
        row['WB2M'] = WB2M
        row['DP2W'] = DP2W
        row['HuRadio2M'] = HuRadio2M
        row['Enth2M'] = Enth2M
        return row


    # Apply the function to each row in the dataframe
    df = df.apply(calculate_properties, axis=1)

    # Save the modified dataframe back to a new CSV file
    output_file = city_file.replace('.csv', '_with_properties.csv')
    df.to_csv(output_file, index=False)
'''

'''
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI

# List of city CSV files
city_files = ['Harbin.csv', 'Shenyang.csv', 'Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']

# Loop through each city file
for city_file in city_files:
    # Read the city CSV file
    df = pd.read_csv(city_file)


    # Calculate the properties and add them to the dataframe
    def calculate_properties(row):
        T2M = row['T2M']
        RH2M = row['RH2M'] / 100  # Convert relative humidity to a fraction
        P = row['PS'] * 1000  # Convert pressure from kPa to Pa
        WB2M = HAPropsSI('Twb', 'T', T2M + 273.15, 'P', P, 'R', RH2M) - 273.15
        DP2W = HAPropsSI('Tdp', 'T', T2M + 273.15, 'P', P, 'R', RH2M) - 273.15
        HuRadio2M = HAPropsSI('W', 'T', T2M + 273.15, 'P', P, 'R', RH2M)
        Enth2M = HAPropsSI('H', 'T', T2M + 273.15, 'P', P, 'R', RH2M) - 2501000  # Convert to J/kg
        row['WB2M'] = WB2M
        row['DP2W'] = DP2W
        row['HuRadio2M'] = HuRadio2M
        row['Enth2M'] = Enth2M
        return row


    # Apply the function to each row in the dataframe
    df = df.apply(calculate_properties, axis=1)

    # Save the modified dataframe back to a new CSV file
    output_file = city_file.replace('.csv', '_with_properties.csv')
    df.to_csv(output_file, index=False)
'''
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('Beijing.csv')
# Step 1: Sort the 'T2M' column in descending order
sorted_data = data.sort_values(by='T2M', ascending=False)
# Step 2: Calculate the values corresponding to the specified percentiles
percentiles = {99.6: '99.6%',  99: '99%' }
# Calculate the indexes for the specified percentiles (rounded to the nearest integer)
percentile_indexes = {percentile: int(len(sorted_data) * (percentile / 100)) for percentile in percentiles}
# Extract the values corresponding to the percentiles
percentile_values = {percentiles[percentile]: sorted_data.iloc[index]['T2M'] for percentile, index in percentile_indexes.items()}
# Step 3: Print the results
for percentile, value in percentile_values.items():
    print(f"排名为{percentile}的T2M值为: {value:.1f} °C")
'''
'''
import pandas as pd

# List of file names
file_names = [ 'Harbin.csv', 'Shenyang.csv', 'Beijing.csv','Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']

# Percentiles to calculate
percentiles = {99.6: '99.6%', 99: '99%'}

# Loop through each file
for filename in file_names:
    city_name = filename.split('.')[0]

    # Load the data from the CSV file
    data = pd.read_csv(filename)

    # Sort the 'T2M' column in descending order
    sorted_data = data.sort_values(by='T2M', ascending=False)

    # Calculate the indexes for the specified percentiles (rounded to the nearest integer)
    percentile_indexes = {percentile: int(len(sorted_data) * (percentile / 100)) for percentile in percentiles}

    # Extract the values corresponding to the percentiles
    percentile_values = {percentiles[percentile]: sorted_data.iloc[index]['T2M'] for percentile, index in percentile_indexes.items()}

    # Print the results for each city
    print(f"City: {city_name}")
    for percentile, value in percentile_values.items():
        print(f"T2M value at {percentile} percentile: {value:.2f} °C")
    print()
'''

# **************不同统计期典型城市的干球温度******************
'''
import matplotlib.pyplot as plt
import numpy as np
# City names
cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']

# # Temperature data for the 99.6% percentile for two different periods
# data_996_02_21 = [-30.02, -21.20, -14.42, -3.14, 2.30, 3.48]
# data_996_94_19 = [-27.4, -22.8, -11.6, -2.5, 4.8, 5.9]

# Temperature data for the 99% percentile for two different periods
data_99_02_21 = [-27.10, -19.35, -12.67, -1.88, 3.61, 5.04]
data_99_94_19 = [-25.2, -20.4, -9.8, -1.1, 5.9, 7.0]

# Create a Matplotlib figure
plt.figure(figsize=(4, 3))

# # Plot temperature trends for the 99.6% percentile with different line styles
# plt.plot(cities, data_996_02_21, marker='o', linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, data_996_94_19, marker='s', linestyle='--', label='94~19 (99.6%)')

# Plot temperature trends for the 99% percentile with different line styles
plt.plot(cities, data_99_02_21, marker='x', markersize=4, color='black', linewidth=1, linestyle='-', label='02~21 (99%)')
plt.plot(cities, data_99_94_19, marker='^', markersize=4, color='black', linewidth=1, linestyle='--', label='94~19 (99%)')

# Add title and labels
# plt.title('Temperature Trends for Different Percentiles in Different Periods')
plt.xlabel("City", fontsize=10)
plt.ylabel("Temperature (°C)", fontsize=10)
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
plt.xticks(rotation=0)  # 旋转标签为0度，使其正常显示

# Add legend, show the grid, and rotate x-axis labels
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3, borderaxespad=0, fontsize=8)
plt.grid(False)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
'''
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('Beijing_with_properties.csv')
# Step 1: Sort the data by DP2M in descending order
sorted_data_dp = data.sort_values(by='DP2W', ascending=False)
# Step 2: Calculate the values corresponding to the 99.6% and 99% percentiles for DP2M
percentiles_dp = {99.6: int(len(sorted_data_dp) * 0.996) , 99: int(len(sorted_data_dp) * 0.99)}
percentile_values_dp = {
    percentile: sorted_data_dp.iloc[index ]['DP2W'] for percentile, index in percentiles_dp.items()}
# Step 3: Calculate the average T2M for each percentile of DP2M
mean_t2m_by_dp2m = {}
for percentile, dp2m in percentile_values_dp.items():
    t2m_values = sorted_data_dp[sorted_data_dp['DP2W'] == dp2m]['T2M']
    mean_t2m_by_dp2m[percentile] = t2m_values.mean()
# Step 4: Sort the data by HuR2M in descending order
sorted_data_hu = data.sort_values(by='HuRadio2M', ascending=False)
# Step 5: Calculate the values corresponding to the 99.6% and 99% percentiles for HuR2M
percentiles_hu = {99.6: int(len(sorted_data_hu) * 0.996) , 99: int(len(sorted_data_hu) * 0.99)}
percentile_values_hu = {
    percentile: sorted_data_hu.iloc[index ]['HuRadio2M'] for percentile, index in percentiles_hu.items()}
# Step 6: Output the results
print("99.6% 和 99% 的露点温度对应的平均干球温度：")
for percentile, t2m_mean in mean_t2m_by_dp2m.items():
    dp2m = percentile_values_dp[percentile]
    hu_r = percentile_values_hu[percentile]*1000
    print(f"{percentile:.1f}% 的露点温度为 {dp2m:.2f} °C，对应的平均干球温度为 {t2m_mean:.2f} °C，对应的含湿量为 {hu_r:.2f}")
'''
'''
import pandas as pd
# Load the data from the CSV file
data = pd.read_csv('Beijing_with_properties.csv')
# Step 1: Sort the data by DP2M in descending order
sorted_data_dp = data.sort_values(by='DP2W', ascending=False)
# Step 2: Calculate the values corresponding to the 99.6% and 99% percentiles for DP2M
percentiles_dp = {99.6: 0.996, 99: 0.99}
percentile_values_dp = {}
for percentile, factor in percentiles_dp.items():
    index = int(len(sorted_data_dp) * factor)
    percentile_values_dp[percentile] = sorted_data_dp.iloc[index]['DP2W']
# Step 4: Sort the data by HuR2M in descending order
sorted_data_hu = data.sort_values(by='HuRadio2M', ascending=False)
# Step 5: Calculate the values corresponding to the 99.6% and 99% percentiles for HuR2M
percentile_values_hu = {}
for percentile, factor in percentiles_dp.items():
    index = int(len(sorted_data_hu) * factor)
    percentile_values_hu[percentile] = sorted_data_hu.iloc[index]['HuRadio2M'] * 1000
# Step 6: Output the results
print("99.6% 和 99% 的露点温度对应的平均干球温度和含湿量：")
for percentile in percentiles_dp.keys():
    t2m_mean = data[data['DP2W'] == percentile_values_dp[percentile]]['T2M'].mean()
    hu_r = percentile_values_hu[percentile]
    print(f"{percentile:.1f}% 的露点温度为 {percentile_values_dp[percentile]:.2f} °C，对应的平均干球温度为 {t2m_mean:.2f} °C，对应的含湿量为 {hu_r:.2f}")
'''
'''
import pandas as pd

# List of city files
city_files = ['Harbin_with_properties.csv', 'Shenyang_with_properties.csv', 'Beijing_with_properties.csv', 'Shanghai_with_properties.csv', 'Fuzhou_with_properties.csv', 'Guangzhou_with_properties.csv']

# Percentiles for calculation
percentiles_dp = {99.6: 0.996, 99: 0.99}

# Loop through each city file
for city_file in city_files:
    print(f"Analyzing data for {city_file}:")

    # Load the data from the CSV file
    data = pd.read_csv(city_file)

    # Step 1: Round 'DP2W' values to 2 decimal places
    data['DP2W'] = data['DP2W'].round(2)

    # Step 2: Sort the data by DP2M in descending order
    sorted_data_dp = data.sort_values(by='DP2W', ascending=False)

    # Step 3: Calculate the values corresponding to the percentiles for DP2M
    percentile_values_dp = {}
    for percentile, factor in percentiles_dp.items():
        index = int(len(sorted_data_dp) * factor+1)
        percentile_values_dp[percentile] = sorted_data_dp.iloc[index]['DP2W']

    # Step 4: Calculate the average T2M values for the specified DP2W percentiles
    t2m_means = {}
    for percentile, dp2w in percentile_values_dp.items():
        t2m_mean = data[data['DP2W'] == dp2w]['T2M'].mean()
        t2m_means[percentile] = t2m_mean

    # Step 5: Sort the data by HuR2M in descending order
    sorted_data_hu = data.sort_values(by='HuRadio2M', ascending=False)

    # Step 6: Calculate the values corresponding to the percentiles for HuR2M
    percentile_values_hu = {}
    for percentile, factor in percentiles_dp.items():
        index = int(len(sorted_data_hu) * factor)
        percentile_values_hu[percentile] = sorted_data_hu.iloc[index]['HuRadio2M'] * 1000

    # Step 7: Output the results
    print("99.6% 和 99% 的露点温度对应的平均干球温度和含湿量：")
    for percentile in percentiles_dp.keys():
        dp2w = percentile_values_dp[percentile]
        hu_r = percentile_values_hu[percentile]
        t2m_mean = t2m_means[percentile]
        print(f"{percentile:.1f}% 的露点温度为 {dp2w:.2f} °C，对应的含湿量为 {hu_r:.2f}，对应的平均干球温度为 {t2m_mean:.2f} °C")

    print()  # Print an empty line for separating cities
'''

 #
#
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.ticker import FixedLocator
# # City names
# cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
#
# # # Dew point temperature data for the 99.6% percentile for two different periods
# # data_dew_996_02_21 = [-30.37, -24.64, -24.22, -8.75, -2.50, -4.65]
# # data_dew_996_94_19 = [-30.9, -28.4, -28.0, -12.2, -4.5, -7.1]
#
# # Dew point temperature data for the 99% percentile for two different periods
# data_dew_99_02_21 = [-27.81, -22.68, -22.03, -6.83, -0.76, -2.36]
# data_dew_99_94_19 = [-28.9, -26.3, -25.8, -9.9, -2.2, -4.0]
#
# # Create a Matplotlib figure with a white background and solid line frame
# plt.figure(figsize=(4, 3), facecolor='white')
# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['right'].set_visible(False)
#
# # # Plot dew point temperature trends for the 99.6% percentile with different line styles
# # plt.plot(cities, data_dew_996_02_21, marker='o',  color='black',  linewidth=1, linestyle='-', label='02~21 (99.6%)')
# # plt.plot(cities, data_dew_996_94_19, marker='s',   color='black',  linewidth=1, linestyle='--', label='94~19 (99.6%)')
#
# # Plot dew point temperature trends for the 99% percentile with different line styles
# plt.plot(cities, data_dew_99_02_21, marker='x',   color='black',  linewidth=1, linestyle='-', label='02~21 (99%)')
# plt.plot(cities, data_dew_99_94_19, marker='^',   color='black',  linewidth=1, linestyle='--', label='94~19 (99%)')
#
# # Add title and labels
# # plt.title('Dew Point Temperature Trends for Different Percentiles in Different Periods')
# plt.xlabel('Cities', fontsize=8)
# plt.ylabel('Dew Point Temperature /°C', fontsize=8)
# # Add legend, show the grid, and adjust appearance
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3, borderaxespad=0, fontsize=8)
#
# plt.grid(False)
# plt.tick_params(axis='both', direction='in') # 刻度线向内
# plt.xticks(rotation=0, fontsize=8)  # Rotate x-axis labels horizontally
# plt.tight_layout()
# # Show the plot
# plt.show()


#**************画图含湿量******************
'''
# import matplotlib.pyplot as plt
#
# # City names
# cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
#
# # Humidity data for the 99.6% percentile for two different periods
# data_humidity_996_02_21 = [0.23, 0.40, 0.42, 1.76, 3.11, 2.53]
# data_humidity_996_94_19 = [0.2, 0.3, 0.3, 1.3, 2.6, 2.1]
#
# # Humidity data for the 99% percentile for two different periods
# data_humidity_99_02_21 = [0.30, 0.49, 0.53, 2.09, 3.60, 3.08]
# data_humidity_99_94_19 = [0.3, 0.3, 0.4, 1.6, 3.2, 2.7]
#
# # Create a Matplotlib figure with a white background
# plt.figure(figsize=(10, 6), facecolor='white')
#
# # Plot humidity trends for the 99.6% percentile with different line styles
# plt.plot(cities, data_humidity_996_02_21, marker='o', linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, data_humidity_996_94_19, marker='s', linestyle='--', label='94~19 (99.6%)')
#
# # Plot humidity trends for the 99% percentile with different line styles
# plt.plot(cities, data_humidity_99_02_21, marker='x', linestyle='-', label='02~21 (99%)')
# plt.plot(cities, data_humidity_99_94_19, marker='^', linestyle='--', label='94~19 (99%)')
#
# # Add title and labels
# plt.title('Humidity Trends for Different Percentiles in Different Periods')
# plt.xlabel('Cities')
# plt.ylabel('Humidity')
#
# # Add legend, show the grid, and adjust appearance
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
#
# # Add top border to the plot
# plt.gca().spines['top'].set_visible(True)
#
# # Show the plot
# plt.tight_layout()
# plt.show()

# **************画图******************

# import matplotlib.pyplot as plt
# 
# # City names
# cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
# 
# # Data for the two statistical periods
# period_02_21_dew_996 = [-26.3, -17.1, -4.6, 3, 8.7, 11.7]
# period_94_19_dew_996 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
# 
# period_02_21_dew_99 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
# period_94_19_dew_99 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
# 
# # Create a Matplotlib figure
# plt.figure(figsize=(10, 6))
# 
# # Plot dew point temperature trends for the 99.6% percentile with different line styles
# plt.plot(cities, period_02_21_dew_996, marker='o', linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, period_94_19_dew_996, marker='s', linestyle='--', label='94~19 (99.6%)')
# 
# # Plot dew point temperature trends for the 99% percentile with different line styles
# plt.plot(cities, period_02_21_dew_99, marker='x', linestyle='-', label='02~21 (99%)')
# plt.plot(cities, period_94_19_dew_99, marker='^', linestyle='--', label='94~19 (99%)')
# 
# # Add title and labels
# plt.title('Average Dry-Bulb Temperature Corresponding to Dew Point Temperature')
# plt.xlabel('Cities')
# plt.ylabel('Temperature (°C)')
# 
# # Add legend, show the grid, and adjust appearance
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
# plt.gca().spines['top'].set_visible(True)    # Add solid top frame
# plt.gca().spines['right'].set_visible(True)  # Add solid right frame
# plt.gca().spines['bottom'].set_linestyle('-')  # Solid bottom frame
# plt.gca().spines['left'].set_linestyle('-')    # Solid left frame
# plt.tight_layout()
# # Show the plot
# plt.show()

#*********计算风速***********

# import pandas as pd
# # Load the data from the CSV file
# data = pd.read_csv('Beijing.csv')
# # Task 1: Sort 'WS10M' (wind speed at 10 meters) when MO=1 in descending order
# sorted_data_ws10m = data[data['MO'] == 1].sort_values(by='WS10M', ascending=False)
# # Task 2: Calculate percentiles for 'WS10M' (wind speed at 10 meters)
# percentiles_ws10m = [0.4, 1]
# percentiles_values_ws10m = {percentile: sorted_data_ws10m['WS10M'].iloc[int(len(sorted_data_ws10m) * (percentile / 100))] for percentile in percentiles_ws10m}
# # Task 3: Calculate average 'T2M' (dry-bulb temperature) for different percentiles of 'WS10M'
# average_t2m_for_ws10m_percentiles = {}
# for percentile in percentiles_ws10m:
#     ws10m_value = percentiles_values_ws10m[percentile]
#     temp_data = sorted_data_ws10m[sorted_data_ws10m['WS10M'] == ws10m_value]
#     average_t2m = temp_data['T2M'].mean()
#     average_t2m_for_ws10m_percentiles[percentile] = round(average_t2m,2)
# # Output results
# print("Percentiles for WS10M:")
# print(percentiles_values_ws10m)
# print("Average T2M for different percentiles of WS10M:")
# print(average_t2m_for_ws10m_percentiles)

#*********计算风速***********

# import pandas as pd
# import math
# 
# # Load the data from the CSV file
# data = pd.read_csv('Beijing.csv')
# 
# # Step 1: Sort 'WS10M' column in descending order
# sorted_data_ws10m = data.sort_values(by='WS10M', ascending=False)
# 
# # Step 2: Calculate the values corresponding to 0.4% and 1% percentiles of 'WS10M'
# percentiles = [0.4, 1]
# percentile_values_ws10m = {percentile: sorted_data_ws10m['WS10M'].iloc[math.ceil(len(sorted_data_ws10m) * (percentile / 100)) - 1] for percentile in percentiles}
# 
# # Step 3: Calculate average 'T2M' for the specified percentiles of 'WS10M'
# average_t2m_for_percentiles = {}
# for percentile in percentiles:
#     ws10m_value = percentile_values_ws10m[percentile]
#     temp_data = sorted_data_ws10m[sorted_data_ws10m['WS10M'] == ws10m_value]
#     average_t2m = temp_data['T2M'].mean()
#     average_t2m_for_percentiles[percentile] = round(average_t2m, 2)
# 
# # Display the results
# print("WS10M Percentiles and Corresponding Average T2M:")
# for percentile, ws10m_value in percentile_values_ws10m.items():
#     print(f"WS10M {percentile:.1f}% Value: {ws10m_value:.2f}")
#     print(f"Average T2M for WS10M {percentile:.1f}%: {average_t2m_for_percentiles[percentile]:.2f}")
#     print()


# List of city filenames
# city_files = ['Harbin.csv', 'Shenyang.csv', 'Beijing.csv', 'Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']

#*********计算风速和干球温度***********

# import pandas as pd
# 
# # Load the data from the CSV file
# data = pd.read_csv('Beijing.csv')
# 
# # Task 0: Filter data for January and round 'WS10M' to one decimal place
# january_data = data[data['MO'] == 1].copy()
# january_data.loc[:, 'WS10M'] = january_data['WS10M'].round(1)
# 
# # Task 1: Sort 'WS10M' column in descending order for January data
# sorted_data_ws10m = january_data.sort_values(by='WS10M', ascending=False)
# 
# # Task 2: Calculate values corresponding to 0.4% and 1% percentiles of 'WS10M' for January data
# percentiles = [0.4, 1]
# percentile_values_ws10m = {percentile: sorted_data_ws10m['WS10M'].iloc[int(len(sorted_data_ws10m) * (percentile / 100))] for percentile in percentiles}
# 
# # Task 3: Calculate average 'T2M' for the specified percentiles of 'WS10M'
# average_t2m_for_percentiles = {}
# for percentile in percentiles:
#     ws10m_value = percentile_values_ws10m[percentile]
#     temp_data = sorted_data_ws10m[sorted_data_ws10m['WS10M'] == ws10m_value]
#     average_t2m = temp_data['T2M'].mean()
#     average_t2m_for_percentiles[percentile] = round(average_t2m, 2)
# 
# # Display the results
# print("WS10M Percentiles and Corresponding Average T2M for January:")
# for percentile, ws10m_value in percentile_values_ws10m.items():
#     print(f"WS10M {percentile:.1f}% Value: {ws10m_value:.1f}")
#     print(f"Average T2M for WS10M {percentile:.1f}%: {average_t2m_for_percentiles[percentile]:.2f}")
#     print()

#*********计算风速***********

# import pandas as pd
# 
# # List of city filenames
# city_files = ['Harbin.csv', 'Shenyang.csv', 'Beijing.csv', 'Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']
# 
# # Iterate through each city's data file
# for city_file in city_files:
#     print(f"City: {city_file}")
# 
#     # Load the data from the CSV file
#     data = pd.read_csv(city_file)
# 
#     # Task 0: Filter data for January and round 'WS10M' to one decimal place
#     january_data = data[data['MO'] == 1].copy()
#     january_data.loc[:, 'WS10M'] = january_data['WS10M'].round(1)
# 
#     # Task 1: Sort 'WS10M' column in descending order for January data
#     sorted_data_ws10m = january_data.sort_values(by='WS10M', ascending=False)
# 
#     # Task 2: Calculate values corresponding to 0.4% and 1% percentiles of 'WS10M' for January data
#     percentiles = [0.4, 1]
#     percentile_values_ws10m = {percentile: sorted_data_ws10m['WS10M'].iloc[int(len(sorted_data_ws10m) * (percentile / 100))] for percentile in percentiles}
# 
#     # Task 3: Calculate average 'T2M' for the specified percentiles of 'WS10M'
#     average_t2m_for_percentiles = {}
#     for percentile in percentiles:
#         ws10m_value = percentile_values_ws10m[percentile]
#         temp_data = sorted_data_ws10m[sorted_data_ws10m['WS10M'] == ws10m_value]
#         average_t2m = temp_data['T2M'].mean()
#         average_t2m_for_percentiles[percentile] = round(average_t2m, 2)
# 
#     # Output results for the current city
#     print("WS10M Percentiles and Corresponding Average T2M for January:")
#     for percentile, ws10m_value in percentile_values_ws10m.items():
#         print(f"WS10M {percentile:.1f}% Value: {ws10m_value:.1f}")
#         print(f"Average T2M for WS10M {percentile:.1f}%: {average_t2m_for_percentiles[percentile]:.2f}")
#         print()


#*********计算风速和最频率风向1***********

# import pandas as pd
# import math
# data = pd.read_csv('Beijing.csv') # Load the data from the CSV file
# # Step 1: Sort 'T2M' column in descending order
# sorted_data = data.sort_values(by='T2M', ascending=False)
# # Step 2: Calculate the value corresponding to 99.6% percentile of 'T2M'
# t2m_rank = int(math.ceil(len(sorted_data) * (99.6 / 100)))
# t2m_99_6 = sorted_data['T2M'].iloc[t2m_rank - 1]
# # Step 3: Get the corresponding 'WS10M' and 'WD10M' for the 99.6% T2M value
# t2m_data_99_6 = sorted_data[sorted_data['T2M'] == t2m_99_6]
# ws_99_6 = round(t2m_data_99_6['WS10M'].mean(), 2)
# wd_99_6 = round(t2m_data_99_6['WD10M'].mean(), 2)  # Calculate the average WD10M
# # Step 4: Calculate the average 'WS10M' for the specified T2M value
# average_ws_99_6 = t2m_data_99_6['WS10M'].mean()
# average_ws_99_6_kmh = average_ws_99_6 * 3.6 # Convert average_ws_99_6 from m/s to km/h
# # Step 5:Display the results
# print(f"T2M 99.6% Value: {t2m_99_6:.2f}")
# print(f"WS10M for T2M 99.6%: {ws_99_6:.2f}")
# print(f"Average WS10M for T2M 99.6%: {average_ws_99_6:.2f} m/s")
# print(f"Most Frequent WD10M for T2M 99.6%: {wd_99_6:.2f}")  # Display the average WD10M

#*********计算风速和最频繁风向2************

# import pandas as pd
# import math
#
# def analyze_city_weather_data(city_csv):
#     data = pd.read_csv(city_csv)  # Load the data from the CSV file
#     # Step 1: Sort 'T2M' column in descending order
#     sorted_data = data.sort_values(by='T2M', ascending=False)
#     # Step 2: Calculate the value corresponding to 99.6% percentile of 'T2M'
#     t2m_rank = int(math.ceil(len(sorted_data) * (99.6 / 100)))
#     t2m_99_6 = sorted_data['T2M'].iloc[t2m_rank - 1]
#     # Step 3: Get the corresponding 'WS10M' and 'WD10M' for the 99.6% T2M value
#     t2m_data_99_6 = sorted_data[sorted_data['T2M'] == t2m_99_6]
#     ws_99_6 = round(t2m_data_99_6['WS10M'].mean(), 2)
#     wd_99_6 = round(t2m_data_99_6['WD10M'].mean(), 2)  # Calculate the average WD10M
#     # Step 4: Calculate the average 'WS10M' for the specified T2M value
#     average_ws_99_6 = t2m_data_99_6['WS10M'].mean()
#     average_ws_99_6_kmh = average_ws_99_6 * 3.6  # Convert average_ws_99_6 from m/s to km/h
#     # Step 5: Display the results
#     print(f"{city_csv} Analysis:")
#     print(f"T2M 99.6% Value: {t2m_99_6:.2f}")
#     print(f"WS10M for T2M 99.6%: {ws_99_6:.2f}")
#     print(f"Most Frequent WD10M for T2M 99.6%: {wd_99_6:.2f}")
#     print("\n")
#
# # List of cities' CSV files
# cities = ['Harbin.csv', 'Shenyang.csv', 'Beijing.csv', 'Shanghai.csv', 'Fuzhou.csv', 'Guangzhou.csv']
#
# # Analyze weather data for each city
# for city_csv in cities:
#     analyze_city_weather_data(city_csv)



# **************画图平均风速******************


# import matplotlib.pyplot as plt
#
# # City names
# cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
#
# # Mean wind speed data for the 99.6% annual cumulative frequency for two different periods
# data_mcws_02_21 = [2.97, 3.79, 4.50, 4.77, 4.75, 4.12]
# data_mcws_94_19 = [1.4, 1.4, 2.8, 2.5, 3.2, 3.3]
#
# # Create a Matplotlib figure with solid line frame
# plt.figure(figsize=(10, 6))
# plt.gca().spines['top'].set_visible(True)
# plt.gca().spines['right'].set_visible(True)
#
# # Plot mean wind speed vs. cities for the 99.6% annual cumulative frequency with different line styles
# plt.plot(cities, data_mcws_02_21, marker='o', linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, data_mcws_94_19, marker='s', linestyle='--', label='94~19 (99.6%)')
#
# # Add title and labels
# plt.title('Mean Wind Speed vs. Cities for 99.6% Annual Cumulative Frequency in Different Periods')
# plt.xlabel('Cities')
# plt.ylabel('Mean Wind Speed (m/s)')
#
# # Add legend, show the grid, and adjust appearance
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
# plt.tight_layout()
#
# # Show the plot
# plt.show()

#*********画图风向**************

# import matplotlib.pyplot as plt
# import numpy as np
# # 风向数据
# cities = ['Guangzhou','Fuzhou','Shanghai','Beijing','Shenyang', 'Harbin']
# pcwd_021 = [18.23,52.86,338.32,321.04,225.53, 288.94 ]
# pcwd_9419 = [ 0,320, 310,0,70,180]
# # 将角度从度数转换为弧度
# angles_021 = np.radians(pcwd_021)
# angles_9419 = np.radians(pcwd_9419)
# # 调整180度对应的角度
# adjusted_angles_9419 = np.where(angles_9419 == np.radians(180), np.radians(180) - np.radians(5), angles_9419)
# # 创建画布和子图
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, polar=True)
# # 绘制散点图
# sc_021 = ax.scatter(angles_021, range(len(cities)), label='02-21', marker='o', s=100)
# sc_9419 = ax.scatter(adjusted_angles_9419, range(len(cities)), label='94-19', marker='x', s=100)
# # 添加城市名称标签
# for i, city in enumerate(cities):
#     ax.annotate(city, (angles_021[i], i), textcoords="offset points", xytext=(5,5), ha='center')
#     ax.annotate(city, (adjusted_angles_9419[i], i), textcoords="offset points", xytext=(5,5), ha='center')
# # 设置雷达图的角度范围和标签
# ax.set_theta_direction(-1)
# ax.set_theta_offset(np.pi / 2.0)
# ax.set_rlabel_position(0)
# ax.set_xticks(np.radians([0, 90, 180, 270]))
# ax.set_xticklabels(['North\n0°', 'East\n90°', 'South\n180°', 'West\n270°'])
# # 添加网格和标题
# ax.grid(True)
# ax.set_title("To 99.6%DB PCWD", va='bottom')
# # 添加图例
# ax.legend(loc='upper right')
# # 显示图表
# plt.show()


