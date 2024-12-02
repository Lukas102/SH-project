'''''
further file for boxplots
'''
#%%
import pandas as pd
import numpy as np 
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
print(f1)
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
#%%
#for y aganist conc
#creating arrays to filter and turn into boxplots /~~~~
y = np.concatenate((f1, f2 , f3))
x = np.concatenate((pep, pep ,pep))
hue = np.repeat([2,4,7],37)
print(hue)
#print(x)
#print(y)
print(f'the length of x is {len(hue)} and it should be {37*3}')
# %%
#using this to remove 0s and NaNs from all equivalent positions
df = pd.DataFrame({
    'Group': x,
    'Classifier': hue,
    'Value': y
})

# Remove rows where 'Value' is 0 or NaN
df_cleaned = df[(df['Value'] != 0) & (~df['Value'].isna())]

# %%
# Creating boxplot straight from cleaned data frame
sns.boxplot(x='Group', y='Value', hue='Classifier', data=df_cleaned)

# Add labels and title
plt.xlabel('Peptone concentration(g)')
plt.ylabel('Biofilm area (cm^2)')
plt.title('Biofilm area aganist peptone concentration')
plt.legend(title='Days of growth')

# Show the plot
plt.show()
# %%
