#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 16:06:54 2023

@author: rasse
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('database.csv')

columns_to_drop = ['Record ID',
                   'Agency Code',
                   'Agency Name',
                   'Agency Type',
                   'Incident',
                   'Victim Ethnicity',
                   'Perpetrator Ethnicity',
                   'Victim Count',
                   'Perpetrator Count',
                   'Record Source']

df = df.drop(columns=columns_to_drop)

# Replace age values of 998 with the median age of non-998 values
non_998_age = df[df['Victim Age'] != 998]['Victim Age']
median_age = non_998_age.median()
df['Victim Age'] = df['Victim Age'].replace(998, median_age)




#total murders per year
murders_per_year = df['Year'].value_counts().sort_index()

# Create a line plot
plt.figure(figsize=(10, 6))
plt.plot(murders_per_year.index, murders_per_year.values, marker='o', linestyle='-', color='b')
plt.title('Number of Murders per Year')
plt.xlabel('Year')
plt.ylabel('Number of Murders')
plt.grid(True)

# Show the plot
plt.show()




#solved murders per year
# Group the data by 'Year' and 'Crime Solved', and count the number of solved and unsolved crimes
crime_counts = df.groupby(['Year', 'Crime Solved'])['Year'].count().unstack().fillna(0)

# Create a line plot
plt.figure(figsize=(10, 6))
plt.plot(crime_counts.index, crime_counts['No'], marker='o', linestyle='-', color='r', label='Unsolved')
plt.plot(crime_counts.index, crime_counts['Yes'], marker='o', linestyle='-', color='b', label='Solved')
plt.title('Solved vs. Unsolved Crimes per Year')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()





#murder weapons total
# Filter the data for non-null 'Weapon' values
filtered_df = df.dropna(subset=['Weapon'])

# Count the number of occurrences for each murder weapon
weapon_counts = filtered_df['Weapon'].value_counts()

# Create a bar chart for murder weapons
plt.figure(figsize=(12, 8))
weapon_counts.plot(kind='bar', color='lightcoral')
plt.title('Murder Weapons Used')
plt.xlabel('Weapon')
plt.ylabel('Count')
plt.xticks(rotation=90)  # Rotate x-axis labels for readability

# Show the plot
plt.show()




#murder weapons per year
# Group the data by 'Year' and 'Weapon' and count the number of murders for each weapon type in each year
weapon_counts = df.groupby(['Year', 'Weapon'])['Weapon'].count().unstack().fillna(0)

# Define a custom color palette for the bars
custom_colors = ['#865e3c', '#0099ff', '#0000ff', '#c01c28', '#1D3557', '#f6d32d', '#ffbe6f', '#ff7800', '#c64600', '#6A0572', '#009933', '#D9BF77', '#a51d2d', '#ed333b', '#336699', '#77767b']


# Create a bar chart with rotated years and adjusted figure size and spacing
fig, ax = plt.subplots(figsize=(15, 8))

# Rotate the years on the x-axis by 90 degrees
ax.set_xticks(range(len(weapon_counts.index)))
ax.set_xticklabels(weapon_counts.index, rotation=90)

# Create a stacked bar chart with the custom color palette
weapon_counts.plot(kind='bar', stacked=True, color=custom_colors, ax=ax)
plt.title('Count of Murder Weapons by Year')
plt.xlabel('Year')
plt.ylabel('Number of Murders')
plt.legend(title='Weapon', loc='upper right', bbox_to_anchor=(1.2, 1))

# Adjust subplot spacing
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

# Show the plot
plt.show()




#murder sex
# Filter the data for non-null 'Perpetrator Sex' values
filtered_df = df.dropna(subset=['Perpetrator Sex'])

# Count the number of male and female perpetrators
perpetrator_counts = filtered_df['Perpetrator Sex'].value_counts()

# Create a bar chart
plt.figure(figsize=(8, 6))
perpetrator_counts.plot(kind='bar', color=['blue', 'red'])
plt.title('Correlation between Male and Female Perpetrators (Murderers)')
plt.xlabel('Perpetrator Sex')
plt.ylabel('Number of Perpetrators')
plt.xticks(rotation=0)  # Keep x-axis labels horizontal

# Show the plot
plt.show()





#victim sex
# Count the number of occurrences for each victim sex
victim_sex_counts = filtered_df['Victim Sex'].value_counts()

# Create a bar chart for victims by sex
plt.figure(figsize=(8, 6))
victim_sex_counts.plot(kind='bar', color='lightcoral')
plt.title('Victims by Sex')
plt.xlabel('Sex')
plt.ylabel('Count')

# Show the plot
plt.show()




#relationships
# Filter the data for non-null and non-'Unknown' 'Relationship' values
filtered_df = df.dropna(subset=['Relationship'])
filtered_df = filtered_df[filtered_df['Relationship'] != 'Unknown']

# Count the number of each type of relationship
relationship_counts = filtered_df['Relationship'].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))
relationship_counts.plot(kind='bar', color='skyblue')
plt.title('Correlation of Relationship between Murderer and Victim (Excluding "Unknown")')
plt.xlabel('Relationship')
plt.ylabel('Frequency')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

# Show the plot
plt.show()




#unknown vs known relationships
# Filter the data for solved crimes and count the number of known and unknown 'Relationship' values
solved_df = df[df['Crime Solved'] == 'Yes']
known_relationship_counts = solved_df[solved_df['Relationship'] != 'Unknown']['Relationship'].count()
unknown_relationship_counts = solved_df[solved_df['Relationship'] == 'Unknown']['Relationship'].count()

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(['Known Relationships', 'Unknown Relationships'], [known_relationship_counts, unknown_relationship_counts], color=['skyblue', 'lightcoral'])
plt.title('Comparison of Known and Unknown Relationships in Solved Crimes')
plt.ylabel('Frequency')

# Show the plot
plt.show()




#unknown murder weapons on solved cases
# Filter the data for solved crimes and count the number of cases with known and unknown murder weapons
solved_df = df[df['Crime Solved'] == 'Yes']
known_weapon_counts = solved_df[solved_df['Weapon'] != 'Unknown']['Weapon'].count()
unknown_weapon_counts = solved_df[solved_df['Weapon'] == 'Unknown']['Weapon'].count()

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(['Solved Cases with Known Weapon', 'Solved Cases with Unknown Weapon'], [known_weapon_counts, unknown_weapon_counts], color=['skyblue', 'lightcoral'])
plt.title('Comparison of Solved Cases with Known and Unknown Murder Weapons')
plt.ylabel('Frequency')

# Show the plot
plt.show()




#murderer race on solved cases
# Filter the data for solved crimes and non-null 'Perpetrator Race' values
solved_df = df[(df['Crime Solved'] == 'Yes') & (~df['Perpetrator Race'].isna())]

# Count the number of each race of perpetrators in solved cases
race_counts = solved_df['Perpetrator Race'].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))
race_counts.plot(kind='bar', color='skyblue')
plt.title('Comparison of Perpetrator Race in Solved Cases')
plt.xlabel('Race')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Keep x-axis labels horizontal

# Show the plot
plt.show()





#comparison on race on solvedvs unsolved
# Filter the data for non-null 'Victim Race' values
filtered_df = df[~df['Victim Race'].isna()]

# Count the total number of cases for Black and White victims in all cases
total_cases = filtered_df['Victim Race'].value_counts()

# Filter the data for solved crimes and count the number of cases for Black and White victims in solved cases
solved_df = df[df['Crime Solved'] == 'Yes']
solved_cases = solved_df['Victim Race'].value_counts()

# Create a bar chart comparing all cases and solved cases for Black and White victims
plt.figure(figsize=(10, 6))

width = 0.35
x = range(len(total_cases))

plt.bar([i - width / 2 for i in x], total_cases, width, label='All Cases', color='lightcoral')
plt.bar([i + width / 2 for i in x], solved_cases, width, label='Solved Cases', color='skyblue')

plt.title('Comparison of Victims race in All vs. Solved Cases')
plt.xlabel('Race')
plt.ylabel('Frequency')
plt.xticks(x, total_cases.index, rotation=45)

plt.legend()

# Show the plot
plt.show()




#murder weapons used by state
# Filter the data for non-null 'State' and 'Weapon' values
filtered_df = df.dropna(subset=['State', 'Weapon'])

# Group the data by 'State' and 'Weapon' and count the number of occurrences
weapon_counts = filtered_df.groupby(['State', 'Weapon']).size().unstack(fill_value=0)

# Transpose the DataFrame to switch places between weapons and states
weapon_counts = weapon_counts.T

# Create a stacked bar chart
plt.figure(figsize=(14, 8))

# Plot a stacked bar for each weapon
for weapon in weapon_counts.index:
    plt.bar(weapon_counts.columns, weapon_counts.loc[weapon], label=weapon)

plt.title('Comparison of Murder Weapons by State')
plt.xlabel('State')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.legend(title='Weapon', loc='upper right')




#murders by month
# Filter the data for non-null 'Month' values
filtered_df = df.dropna(subset=['Month'])

# Define a custom order for the months
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Count the number of murders by month and order the results
month_counts = filtered_df['Month'].value_counts().reindex(month_order)

# Create a bar chart
plt.figure(figsize=(10, 6))
month_counts.plot(kind='bar', color='lightcoral')
plt.title('Murder Count by Month')
plt.xlabel('Month')
plt.ylabel('Count')

# Show the plot
plt.show()




#murders by season
# Define a dictionary to map months to seasons
month_to_season = {
    'January': 'Winter',
    'February': 'Winter',
    'March': 'Spring',
    'April': 'Spring',
    'May': 'Spring',
    'June': 'Summer',
    'July': 'Summer',
    'August': 'Summer',
    'September': 'Fall',
    'October': 'Fall',
    'November': 'Fall',
    'December': 'Winter'
}

# Filter the data for non-null 'Month' values
filtered_df = df.dropna(subset=['Month'])

# Map months to seasons
filtered_df['Season'] = filtered_df['Month'].map(month_to_season)

# Count the number of murders in each season
season_counts = filtered_df['Season'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(season_counts, labels=season_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightblue', 'lightgreen', 'lightsalmon'])
plt.title('Murders by Season')

# Show the plot
plt.show()




#unsolved murder seasons
# Define a dictionary to map months to seasons
month_to_season = {
    'January': 'Winter',
    'February': 'Winter',
    'March': 'Spring',
    'April': 'Spring',
    'May': 'Spring',
    'June': 'Summer',
    'July': 'Summer',
    'August': 'Summer',
    'September': 'Fall',
    'October': 'Fall',
    'November': 'Fall',
    'December': 'Winter'
}

# Filter the data for unsolved cases with non-null 'Month' values
unsolved_df = df[(df['Crime Solved'] == 'No') & ~df['Month'].isna()]

# Map months to seasons
unsolved_df['Season'] = unsolved_df['Month'].map(month_to_season)

# Count the number of unsolved murders in each season
season_counts = unsolved_df['Season'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(season_counts, labels=season_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightblue', 'lightgreen', 'lightsalmon'])
plt.title('Unsolved Murders by Season')

# Show the plot
plt.show()





#solved vs unolved cases per state
# Filter the data for non-null 'State' and 'Crime Solved' values
filtered_df = df.dropna(subset=['State', 'Crime Solved'])

# Group the data by 'State' and 'Crime Solved' and count the number of occurrences
murder_counts = filtered_df.groupby(['State', 'Crime Solved']).size().unstack(fill_value=0)

# Get a list of all states
states = murder_counts.index

# Define the width of the bars
bar_width = 0.4

# Create a grouped bar chart
plt.figure(figsize=(14, 8))

# Set colors for solved and unsolved bars (switched)
colors = ['lightgreen', 'lightcoral']

# Plot separate bars for each state (solved and unsolved)
for i, state in enumerate(states):
    solved_counts = murder_counts.loc[state]['Yes']
    unsolved_counts = murder_counts.loc[state]['No']

    # Position the bars side by side
    plt.bar(i - bar_width / 2, solved_counts, width=bar_width, label=f'{state} - Solved', color=colors[0])
    plt.bar(i + bar_width / 2, unsolved_counts, width=bar_width, label=f'{state} - Unsolved', color=colors[1])

# Set x-axis labels with state names
plt.xticks(range(len(states)), states, rotation=90)

plt.title('Comparison of Solved vs Unsolved Murders by State')
plt.xlabel('State')
plt.ylabel('Count')

# Remove the legend
plt.legend().set_visible(False)

# Show the plot
plt.show()
