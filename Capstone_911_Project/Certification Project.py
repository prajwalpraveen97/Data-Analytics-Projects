import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import data from csv into dataframe
df = pd.read_csv("911.csv.csv")
print(df.head(10).to_string())
print("\n")

# Check the data structure
print(df.info())
print("\n")

# Data Wrangling: Before analysis, it is importent to ensure there are no incorrect/missing data that could bias our result.
# It is called sample correction.

print(df.isnull().sum())
print("\n")

# Conclusion1: We Need to ignore the record which have not township/zip details.

# Removing null zip records

df_wrang_zip = df[pd.notnull(df['zip'])]
print(df_wrang_zip.isnull().sum())
print("\n")

# Removing null twp(township) records

df_wrang = df_wrang_zip[pd.notnull(df_wrang_zip['twp'])]
print(df_wrang.isnull().sum())
print("\n")

print(df_wrang.info())
print("\n")

# Starting Data Analysis

print(df_wrang.head().to_string())
print("\n")

# Top 10 zipcodes for 911 calls

print("Top 10 zipcodes for 911 calls:\n")
print(df_wrang['zip'].value_counts().head(10))
print("Zipcodes 19446 and 19090 are present\n")

# Top 4 townships (twp) for 911 calls

print("Top 4 townships (twp) for 911 calls:\n")
print(df_wrang['twp'].value_counts().head(4))
print("LOWER POTTSGROVE and HORSHAM are not present\n")

# https://www.geeksforgeeks.org/python-pandas-index-nunique/

print("The count of unique values in Title Column: ")
print(df_wrang['title'].nunique()) # --> To obtain the count of unique values in Title Column
print("\n")

# Creating two different field from existing data frame named as Department and Reason

print("Creating two different field from existing data frame named as Department and Reason: ")
df_wrang['Department'] = df_wrang['title'].apply(lambda val: val.split(':')[1])
df_wrang['Reason'] = df_wrang['title'].apply(lambda val: val.split(':')[0])
print(df_wrang.head().to_string())
print("\n")

# To check unique reason from Reason column

print("To check unique reason from Reason column:\n")
print(df_wrang['Reason'].unique())
print("\n")

# To check unique department from Department column

print("To check unique department from Department column:\n")
print(df_wrang['Department'].unique())
print("\n")

# What is the most common Reason for a 911 call based on Reason Column?

print("To check the most common Reason for a 911 call: \n")
print(df_wrang['Reason'].value_counts())
print("\n")

# Visual representation for the most common Reason for a 911 call
sns.countplot(x=df_wrang['Reason'])
plt.show()

# most common Reason for a 911 call through a Horizontal bar chart
df_wrang.groupby('Reason').count().sort_values('e',ascending=0)[:3]['e'].plot(kind='barh')
plt.show()

# Top 5 department for emergency call with visual representation

print("Top 5 department for emergency call with visual representation:\n")
print(df_wrang['Department'].value_counts().head(5))
print("\n")

# Top 5 department for emergency call with visual representation using horizontal bar chart

df_wrang.groupby('Department').count().sort_values('e',ascending=0)[:5]['e'].plot(kind='barh')
plt.show()

# Top 5 township for emergency calling with visual representation

print("Top 5 township for emergency calling with visual representation:\n")

print(df_wrang['twp'].value_counts()[:5])
print("\n")
df_wrang.groupby('twp').count().sort_values('e',ascending=0)[:5]['e'].plot(kind='barh')
plt.show()

# Top 5 township with reasons via visual representation

twplst = list(df_wrang['twp'].value_counts()[:5].index)
print("List for the Top 5 townships with majority 911 calls: ")
print(twplst)

plt.figure(figsize=(10,6))
sns.countplot(data=df_wrang[df_wrang['twp'].apply(lambda x:(True if x in twplst else False))],x='twp', hue='Reason')
plt.show()

# Finding the township with the highest 911 calls

plt.figure(figsize=(10,6))
sns.countplot(data=df_wrang[df_wrang['twp'].apply(lambda x:(True if x in twplst else False))],x='twp')
plt.show()

# DateTime Analysis for emergency calls

# Converting string column to Datetime format

df_wrang['timeStamp'] = pd.to_datetime(df_wrang['timeStamp'])
#print(df_wrang.info())

# Creating a new column for Month, Day of week

df_wrang['Month'] = df_wrang['timeStamp'].apply(lambda x: x.month)
df_wrang['DayOfWeek'] = df_wrang['timeStamp'].apply(lambda x: x.dayofweek)
#print(df_wrang.head())

# Creating new column for Month, Day of week
daydict = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
df_wrang['DayOfWeek'] = df_wrang['DayOfWeek'].map(daydict)

mondict = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
df_wrang['Month']=df_wrang['Month'].map(mondict)
print(df_wrang.head().to_string())
print("\n")

# To find which month saw highest calls for fire

plt.figure(figsize=(10,6))
sns.countplot(x='Month',data=df_wrang,hue='Reason')
plt.show()
print("Conclusion: June-Barbeque and Holidays time received maximum Fire call")

# To find  On which day traffic calls were lowest

plt.figure(figsize=(12,6))
sns.countplot(x='DayOfWeek', data=df_wrang, hue='Reason')
plt.show()
print("Conclusion: As expected-Sunday always less traffic")

# Creating Web Map for Traffic Calls

#removing unwanted columns
avail =df_wrang[0:100]

#initalizing folium map object as m and using the geographic mean of the data points to center the viewpoint; basemap defaults to OSM
map = folium.Map(location=[df_wrang["lat"].mean(), df_wrang["lng"].mean()], zoom_start=12)

#Iterate through edited dataframe to extract coordinates and property name for each record
for row in avail.iterrows():
    prop = str(row[1]['Reason'] == "Traffic")
    lat = row[1]["lat"]
    lon = row[1]["lng"]

#attach each record to a default marker style based on coordinates and add property name to popup window
    folium.Marker(location=[lat, lon], marker_color='red', popup="Traffic").add_to(map)

#outputting html document with code for an interactive map to working directory
map.save('map.html')
print("These are areas like Airport, State Park etc....")

