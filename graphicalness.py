'''''
graphing y aganist days

'''
#%%
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import linregress
import itertools
import seaborn as sns
#%%
sheet1 = pd.read_excel(r'M:\SH project\Image_Analysis\IA-data_copy3.xlsx', sheet_name=0)
sheet2 = pd.read_excel(r'M:\SH project\Image_Analysis\IA-data_copy3.xlsx', sheet_name=1)
print(sheet2)
# %%
#extracting fractal values
f1 = np.asfarray(sheet2.iloc[1:39,1])
f2 = np.asfarray(sheet2.iloc[1:39,3])
f3 = np.asfarray(sheet2.iloc[1:39,4])
pep = np.asfarray(sheet2.iloc[1:39,2])
#%%
#extracting areas
f1 = np.asfarray(sheet1.iloc[1:38,4])
#print(f1)
f2 = np.asfarray(sheet1.iloc[40:77,4])
#print(len(f2))
#print(f2)
f3 = np.asfarray(sheet1.iloc[77:114,4])
print(f3)
pep = np.asfarray(sheet2.iloc[1:39,2])
#print(pep)
print(len(pep))

# %%
#sorting through to find averages for each concentration so this is for a y vs days graph

# Dictionaries to hold variables for each classifier 
pep_values1 = {
    4.0: [],
    0.8: [],
    0.4: [],
    0.004: []  # Add other classifiers as needed
}
pep_values2 = {
    4.0: [],
    0.8: [],
    0.4: [],
    0.004: []  # Add other classifiers as needed
}
pep_values3 = {
    4.0: [],
    0.8: [],
    0.4: [],
    0.004: []  # Add other classifiers as needed
}
#%%
#clearing dictionaries so they can be reused
for conc in pep_values1:
    pep_values1[conc].clear()


for i, conc in enumerate(pep):
    if conc in pep_values1 and not pd.isna(f1[i]):
        pep_values1[conc].append(f1[i])

f1_means = []     

# Calculate the mean for each key
for conc, values in pep_values1.items():
    #filtering out false 0s from excel
    filt0 = [value for value in values if value != 0]
    
    if filt0:  # Check if the list is not empty
        mean_value = np.mean(filt0)
    else:
        mean_value = None  # Handle empty lists if needed
    f1_means.append((mean_value))

# Output the list of means + length as a check
print('the mean of f1 is' + str(f1_means))
print(len(f1_means))
#%%

for conc in pep_values2:
    pep_values2[conc].clear()

#finding mean values for second column

for i, conc in enumerate(pep):
    if conc in pep_values2 and not pd.isna(f2[i]):
        pep_values2[conc].append(f2[i])

f2_means = []

# Calculate the mean for each key
for conc, values in pep_values2.items():
    #filtering out 0s
    filt0 = [value for value in values if value != 0]

    if filt0:  # Check if the list is not empty
        mean_value = np.mean(filt0)
    else:
        mean_value = None  # Handle empty lists if needed
    f2_means.append((mean_value))

print('the mean of f2 is' + str(f2_means))
print(len(f2_means))
# %%
#finding mean values for 3rd function.

for conc in pep_values3:
    pep_values3[conc].clear()

for i, conc in enumerate(pep):
    if conc in pep_values3 and not pd.isna(f3[i]):
        pep_values3[conc].append(f3[i])

f3_means = []     

# Calculate the mean for each key
for conc, values in pep_values3.items():
    #no 0s
    filt0 = [value for value in values if value != 0]

    if filt0:  # Check if the list is not empty
        mean_value = np.mean(filt0)
    else:
        mean_value = None  # Handle empty lists if needed
    f3_means.append((mean_value))
    
print(len(f3_means))
print('the mean of f3 is' + str(f3_means))
# %%
#plotting y aganist days
y = f1_means + f2_means + f3_means
print(y)
print(len(y))
#days
x = [2,2,2,2,4,4,4,4,7,7,7,7]
#skip straight to cell labbeled linregress 2 if plotting y aganist days
#%%
#plotting y aganist concentration
#creating a zip to combine mean arrays into big tuple
zippy = zip(f1_means, f2_means, f3_means)

#flattening out each element to get an array sorted in order of concentration
y = np.array([element for pair in zip(f1_means, f2_means, f3_means) for element in pair])
#creating an x array of values to deal with 
x = np.array([4,4,4,0.8,0.8,0.8,0.4,0.4,0.4,0.004,0.004,0.004])
print(x)
print(y)


#%%
#lines of best fit for y aganist concetration
# are already categorised by days in orginal f_mean array
x_full = np.linspace(x[0], x[-1], 100)
x_pep = np.array([4,0.8,0.4,0.004])
#first linregress for day 1
s1, i1, r_value, p_value, std_err = linregress(x_pep, f1_means)
d1 = s1 * x_full + i1
#second
s2, i2, r_value, p_value, std_err = linregress(x_pep, f2_means)
d2 = s2 * x_full + i2
#third
s3, i3, r_value, p_value, std_err = linregress(x_pep, f3_means)
d3 = s3 * x_full + i3

#%%
#scatter ploy for y aganist concetration
#colour list
colours = itertools.cycle(["b", "r", "k"])

# Looping through the data, coloring the dots in groups
for i in range(len(x)):
    plt.scatter(x[i], y[i], color=next(colours))

#first interp
plt.plot(x_full, d1, color='blue', label='Day 2')
#
plt.plot(x_full, d2, color='red', label='Day 4')
#
plt.plot(x_full, d3, color='black', label='Day 7')


# Labeling the axes
plt.xlabel('Peptone concentration (g)')
plt.ylabel('Area (cm^2)')

# Title of the plot
plt.title('Average surface area aganist Concentration')
plt.legend(loc='upper left')

# Show the plot
plt.show()
# %%



#%%
#linregress 2 
#creating best fit lines to be plotted for y aganist days.
x4 = x[0::4]
y4 = y[0::4]
print(x4)

x_4 = x[1::4]
y_4= y[1::4]
print(x_4)

x_8 = x[2::4]
y_8 = y[2::4]

xs4 = x[3::4]
ys4= y[3::4]

#for smooth best fit
x_full = np.linspace(x[0], x[-1], 100)

#first fit
s1, i1, r_value, p_value, std_err = linregress(x4, y4)
y4_intp = s1 * x_full + i1

#second fit
s2, i2, r_value, p_value, std_err = linregress(x_4, y_4)
y_4_intp = s2 * x_full + i2
#third
s3, i3, r_value, p_value, std_err = linregress(x_8, y_8)
y_8_intp = s3 * x_full + i3
#fourth
s4, i4, r_value, p_value, std_err = linregress(xs4, ys4)
ys4_intp = s4 * x_full + i4
#%%
#scatter plot for y aganist days
#colour list
colours = itertools.cycle(["b", "r", "k", 'y'])

# Looping through the data, coloring the dots in groups
for i in range(len(x)):
    plt.scatter(x[i], y[i], color=next(colours))

#first interp
plt.plot(x_full, y4_intp, color='blue', label='4g')
#
plt.plot(x_full, y_4_intp, color='red', label='0.8g')
#
plt.plot(x_full, y_8_intp, color='black', label='0.4g')
#
plt.plot(x_full, ys4_intp, color='yellow', label='0.004g')

# Labeling the axes
plt.xlabel('Days')
plt.ylabel('Dimension)')

# Title of the plot
plt.title('Average surface dimension aganist days')
plt.legend(loc='upper left')

# Show the plot
plt.show()
# %%
