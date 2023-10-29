#***************干球温度************
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator, FixedLocator
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
plt.ylabel("Dry-bulb Temperature /°C", fontsize=10)
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
plt.xticks(rotation=0)  # 旋转标签为0度，使其正常显示
# Add legend, show the grid, and rotate x-axis labels
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=3, borderaxespad=0, fontsize=8, frameon=False)
plt.grid(False)
plt.tick_params(axis='both', direction='in', labelsize=8)
plt.tight_layout()
# Show the plot
plt.show()
'''
#***************露点温度************
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator
# City names
cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
# Dew point temperature data for the 99.6% percentile for two different periods
data_dew_996_02_21 = [-30.37, -24.64, -24.22, -8.75, -2.50, -4.65]
data_dew_996_94_19 = [-30.9, -28.4, -28.0, -12.2, -4.5, -7.1]
# Dew point temperature data for the 99% percentile for two different periods
data_dew_99_02_21 = [-27.81, -22.68, -22.03, -6.83, -0.76, -2.36]
data_dew_99_94_19 = [-28.9, -26.3, -25.8, -9.9, -2.2, -4.0]
# Create a Matplotlib figure with a white background and solid line frame
plt.figure(figsize=(4, 3), facecolor='white')
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
# Plot dew point temperature trends for the 99.6% percentile with different line styles
# plt.plot(cities, data_dew_996_02_21, marker='o',  color='black',  linewidth=1, linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, data_dew_996_94_19, marker='s',   color='black',  linewidth=1, linestyle='--', label='94~19 (99.6%)')
# Plot dew point temperature trends for the 99% percentile with different line styles
plt.plot(cities, data_dew_99_02_21, marker='x',   color='black',  linewidth=1, linestyle='-', label='02-21 (99%)')
plt.plot(cities, data_dew_99_94_19, marker='^',   color='black',  linewidth=1, linestyle='--', label='94-19 (99%)')
# Add title and labels
# plt.title('Dew Point Temperature Trends for Different Percentiles in Different Periods')
plt.xlabel('Cities', fontsize=10)
plt.ylabel('Dew Point Temperature /°C', fontsize=10)
# Add legend, show the grid, and adjust appearance
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=3, borderaxespad=0, fontsize=8, frameon=False)
plt.grid(False)
plt.tick_params(axis='both', direction='in') # 刻度线向内
plt.xticks(rotation=0, fontsize=8)  # Rotate x-axis labels horizontally
plt.tight_layout()
# Show the plot
plt.show()
'''
#***************含湿量************
'''
import matplotlib.pyplot as plt
# City names
cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
# Humidity data for the 99.6% percentile for two different periods
data_humidity_996_02_21 = [0.23, 0.40, 0.42, 1.76, 3.11, 2.53]
data_humidity_996_94_19 = [0.2, 0.3, 0.3, 1.3, 2.6, 2.1]
# Humidity data for the 99% percentile for two different periods
data_humidity_99_02_21 = [0.30, 0.49, 0.53, 2.09, 3.60, 3.08]
data_humidity_99_94_19 = [0.3, 0.3, 0.4, 1.6, 3.2, 2.7]
# Create a Matplotlib figure with a white background
plt.figure(figsize=(4, 3), facecolor='white')
# # Plot humidity trends for the 99.6% percentile with different line styles
# plt.plot(cities, data_humidity_996_02_21, marker='o',   color='black',  linewidth=1, linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, data_humidity_996_94_19, marker='s',   color='black',  linewidth=1, linestyle='--', label='94~19 (99.6%)')
# Plot humidity trends for the 99% percentile with different line styles
plt.plot(cities, data_humidity_99_02_21, marker='x',   color='black',  linewidth=1, linestyle='-', label='02~21 (99%)')
plt.plot(cities, data_humidity_99_94_19, marker='^',   color='black',  linewidth=1, linestyle='--', label='94~19 (99%)')
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
# Add title and labels
# plt.title('Humidity Trends for Different Percentiles in Different Periods')
plt.xlabel('Cities', fontsize=10)
plt.ylabel('Humidity/ g(kg•dry-air)', fontsize=10)
plt.tick_params(axis='both', direction='in') # 刻度线向内
# Add legend, show the grid, and adjust appearance
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), fancybox=True, shadow=False, ncol=3, borderaxespad=0, fontsize=8, frameon=False)
plt.grid(False)
plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
# Add top border to the plot
plt.gca().spines['top'].set_visible(True)
# Show the plot
plt.tight_layout()
plt.show()
'''
#***************露点温度对应的平均干球温度************
'''
import matplotlib.pyplot as plt
# City names
cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']
# Data for the two statistical periods
period_02_21_dew_996 = [-26.3, -17.1, -4.6, 3, 8.7, 11.7]
period_94_19_dew_996 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
period_02_21_dew_99 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
period_94_19_dew_99 = [-24.2, -16.8, -3.7, 3.3, 8.9, 12.1]
# Create a Matplotlib figure
plt.figure(figsize=(4, 3))
# Plot dew point temperature trends for the 99.6% percentile with different line styles
# plt.plot(cities, period_02_21_dew_996, marker='o', markersize=4, color='black', linewidth=1, linestyle='-', label='02~21 (99.6%)')
# plt.plot(cities, period_94_19_dew_996, marker='s',markersize=4, color='black', linewidth=1,  linestyle='--', label='94~19 (99.6%)')
# Plot dew point temperature trends for the 99% percentile with different line styles
plt.plot(cities, period_02_21_dew_99, marker='x',markersize=4, color='black', linewidth=1,  linestyle='-', label='02~21 (99%)')
plt.plot(cities, period_94_19_dew_99, marker='^', markersize=4, color='black', linewidth=1, linestyle='--', label='94~19 (99%)')
# Add title and labels
# plt.title('Average Dry-Bulb Temperature Corresponding to Dew Point Temperature')
plt.xlabel('Cities', fontsize=10)
plt.ylabel('Dry-bulb Temperature /°C', fontsize=10)
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
# Add legend, show the grid, and adjust appearance
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), fancybox=True, shadow=False, ncol=3, borderaxespad=0, fontsize=8, frameon=False)
plt.grid(False)
plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
plt.gca().spines['top'].set_visible(True)    # Add solid top frame
plt.gca().spines['right'].set_visible(True)  # Add solid right frame
plt.gca().spines['bottom'].set_linestyle('-')  # Solid bottom frame
plt.gca().spines['left'].set_linestyle('-')    # Solid left frame
plt.tick_params(axis='both', direction='in', labelsize=8)
plt.tight_layout()
# Show the plot
plt.show()

'''
#***************风速************
import matplotlib.pyplot as plt
# City names
cities = ['Harbin', 'Shenyang', 'Beijing', 'Shanghai', 'Fuzhou', 'Guangzhou']

# Mean wind speed data for the 99.6% annual cumulative frequency for two different periods
data_mcws_02_21 = [2.97, 3.79, 4.50, 4.77, 4.75, 4.12]
data_mcws_94_19 = [1.4, 1.4, 2.8, 2.5, 3.2, 3.3]
# Create a Matplotlib figure with solid line frame
plt.figure(figsize=(4, 3))
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
# Plot mean wind speed vs. cities for the 99.6% annual cumulative frequency with different line styles
plt.plot(cities, data_mcws_02_21, marker='x',  color='black',  linewidth=1, linestyle='-', label='02-21 (99.6%)')
plt.plot(cities, data_mcws_94_19, marker='^',  color='black',  linewidth=1, linestyle='--', label='94-19 (99.6%)')
# Add title and labels
# plt.title('Mean Wind Speed vs. Cities for 99.6% Annual Cumulative Frequency in Different Periods')
plt.xlabel('Cities', fontsize=10)
plt.ylabel('Mean Wind Speed / (m/s)', fontsize=10)
# Add legend, show the grid, and adjust appearance
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=3, borderaxespad=0, fontsize=8, frameon=False)
plt.grid(False)
plt.tick_params(axis='both', direction='in', labelsize=8) # 刻度线向内
plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
plt.tight_layout()
# Show the plot
plt.show()