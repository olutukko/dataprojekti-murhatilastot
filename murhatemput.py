import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
                   'Record Source',
                   'City',
                   'Month',
                   'Crime Type',
                   'Victim Race',
                   'Perpetrator Race',
                   'Victim Age',
                   'Perpetrator Age']

df = df.drop(columns=columns_to_drop)

# Check for null values
null_values = df.isnull()
null_counts = null_values.sum()
print(f'Null values {null_counts}')

desc = df.describe()
info = df.info()

# Count rows
row_count = len(df)
print(f'Row count: {row_count}')


# Which gender kills which gender #

gender_count = df.groupby(['Perpetrator Sex', 'Victim Sex']).size().unstack(fill_value=0)
gender_percentage = gender_count.div(gender_count.sum(axis=1), axis=0) * 100

# Create a bar plot
ax = gender_percentage.plot(kind='bar', stacked=True, figsize=(10, 6), color=['lightpink', 'skyblue', 'lightgray'])
ax.set_ylabel('Percentage')
ax.set_xlabel('Perpetrator Sex')
ax.set_title('Gender Distribution in Crime: Perpetrator vs. Victim (%)')
ax.legend(title='Victim Sex', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# Weapon usage by state #

# Calculate the percentage of each weapon used in each state
weapon_counts_by_state = df.pivot_table(index='State', columns='Weapon', aggfunc='size', fill_value=0)
percentage_weapon_usage_by_state = weapon_counts_by_state.div(weapon_counts_by_state.sum(axis=1), axis=0) * 100

# Create the heatmap with percentage values
plt.figure(figsize=(16, 12))
sns.heatmap(percentage_weapon_usage_by_state, cmap='YlOrRd', annot=True, fmt='.2f', linewidths=.5, vmin=0, vmax=100)
plt.title('Statewise Distribution of Murder Weapons (%)')
plt.show()


# Weapon usage by year #

# Calculate the percentage of each weapon used in each year
weapon_counts_by_year = df.pivot_table(index='Year', columns='Weapon', aggfunc='size', fill_value=0)
percentage_weapon_usage_by_year = weapon_counts_by_year.div(weapon_counts_by_year.sum(axis=1), axis=0) * 100

# Create the heatmap with percentage values
plt.figure(figsize=(16, 12))
sns.heatmap(percentage_weapon_usage_by_year, cmap='YlOrRd', annot=True, fmt='.2f', linewidths=.5, vmin=0, vmax=100)
plt.title('Year-wise Distribution of Murder Weapons (%)')
plt.show()


# Weapon usage by gender #

# Calculate the percentage of each weapon used by gender 
weapon_counts_by_gender = df.pivot_table(index='Perpetrator Sex', columns='Weapon', aggfunc='size', fill_value=0)
percentage_weapon_usage_by_gender = weapon_counts_by_gender.div(weapon_counts_by_gender.sum(axis=1), axis=0) * 100

# Transpose
weapon_by_gender_transposed = percentage_weapon_usage_by_gender.T

# Create the heatmap with percentage values
plt.figure(figsize=(12, 8))
sns.heatmap(weapon_by_gender_transposed, cmap='YlOrRd', annot=True, fmt='.2f', linewidths=.5, vmin=0, vmax=100)
plt.title('Gender-wise Distribution of Murder Weapons (%)')
plt.show()


# Total murders per year #
murders_per_year = df['Year'].value_counts().sort_index()

# Create a line plot
plt.figure(figsize=(10, 6))
plt.plot(murders_per_year.index, murders_per_year.values, marker='o', linestyle='-', color='b')
plt.title('Number of Murders per Year')
plt.xlabel('Year')
plt.ylabel('Number of Murders')
plt.grid(True)
plt.show()


# Solved murders per year #

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
plt.show()


# Murder weapons total #

# Count the number of occurrences for each murder weapon
weapon_counts = df['Weapon'].value_counts()

# Create a bar chart
plt.figure(figsize=(12, 8))
weapon_counts.plot(kind='bar', color='lightcoral')
plt.title('Murder Weapons Used')
plt.xlabel('Weapon')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(12, 8))
weapon_counts.plot(kind='bar', color='lightcoral')

plt.yscale('log')  # Set y-axis to logarithmic scale
plt.title('Murder Weapons Used (Logarithmic Scale)')
plt.xlabel('Weapon')
plt.ylabel('Count (log scale)')
plt.xticks(rotation=90)
plt.show()



# Perpetrator sex #

# Count the number of male and female perpetrators
perpetrator_counts = df['Perpetrator Sex'].value_counts()

# Create a bar chart
plt.figure(figsize=(8, 6))
perpetrator_counts.plot(kind='bar', color=['lightblue', 'grey'])
plt.title('Male and Female Perpetrators')
plt.xlabel('Perpetrator Sex')
plt.ylabel('Number of Perpetrators')
plt.xticks(rotation=0)
plt.show()


# Victim sex #

# Count the number of occurrences for each victim sex
victim_counts = df['Victim Sex'].value_counts()

# Create a bar chart for victims by sex
plt.figure(figsize=(8, 6))
victim_counts.plot(kind='bar', color='lightcoral')
plt.title('Victims by Sex')
plt.xlabel('Sex')
plt.ylabel('Count')
plt.show()


# Relationship between victim and perpetrator

# Count the number of each type of relationship
filtered_df = df[df['Relationship'] != 'Unknown']
relationship_counts = filtered_df['Relationship'].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))
relationship_counts.plot(kind='bar', color='skyblue')
plt.title('Relationship between Victim and Perpetrator (Excluding "Unknown")')
plt.xlabel('Frequency')
plt.ylabel('Number of Relationships')
plt.xticks(rotation=90) 
plt.show()

#logarithmic version
plt.figure(figsize=(10, 6))
relationship_counts[relationship_counts.index != 'Unknown'].plot(kind='bar', color='skyblue')

plt.yscale('log')  # Set y-axis to logarithmic scale
plt.title('Relationship between Victim and Perpetrator (Excluding "Unknown")')
plt.xlabel('Frequency')
plt.ylabel('Number of Relationships (log scale)')
plt.xticks(rotation=90)
plt.show()




# Unknown vs known relationships when crime is solved #

# Filter the data for solved crimes and count the number of known and unknown 'Relationship' values
solved_df = df[df['Crime Solved'] == 'Yes']
known_relationship_counts = solved_df[solved_df['Relationship'] != 'Unknown']['Relationship'].count()
unknown_relationship_counts = solved_df[solved_df['Relationship'] == 'Unknown']['Relationship'].count()

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(['Known Relationships', 'Unknown Relationships'], [known_relationship_counts, unknown_relationship_counts], color=['skyblue', 'lightcoral'])
plt.title('Comparison of Known and Unknown Relationships in Solved Crimes')
plt.ylabel('Frequency')
plt.show()


# Unknown murder weapons on solved cases #

# Count the number of cases with known and unknown murder weapons
known_weapon_counts = solved_df[solved_df['Weapon'] != 'Unknown']['Weapon'].count()
unknown_weapon_counts = solved_df[solved_df['Weapon'] == 'Unknown']['Weapon'].count()

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(['Solved Cases with Known Weapon', 'Solved Cases with Unknown Weapon'], [known_weapon_counts, unknown_weapon_counts], color=['skyblue', 'lightcoral'])
plt.title('Comparison of Solved Cases with Known and Unknown Murder Weapons')
plt.ylabel('Frequency')
plt.show()


# Solved vs unsolved cases per state

# Group the data by 'State' and 'Crime Solved' and count the number of occurrences
murder_counts = df.groupby(['State', 'Crime Solved']).size().unstack(fill_value=0)
states = murder_counts.index

# Define the width of the bars
bar_width = 0.4
plt.figure(figsize=(14, 8))
colors = ['lightgreen', 'lightcoral']

# Plot separate bars for each state (solved and unsolved)
for i, state in enumerate(states):
    solved_counts = murder_counts.loc[state]['Yes']
    unsolved_counts = murder_counts.loc[state]['No']

    # Position the bars side by side
    plt.bar(i - bar_width / 2, solved_counts, width=bar_width, label=f'{state} - Solved', color=colors[0])
    plt.bar(i + bar_width / 2, unsolved_counts, width=bar_width, label=f'{state} - Unsolved', color=colors[1])

plt.xticks(range(len(states)), states, rotation=90)
plt.title('Comparison of Solved vs Unsolved Murders by State')
plt.xlabel('State')
plt.ylabel('Count')
plt.legend().set_visible(False)
plt.show()

#solved unsolved logarithmic
plt.figure(figsize=(14, 8))
colors = ['lightgreen', 'lightcoral']

for i, state in enumerate(states):
    solved_counts = murder_counts.loc[state]['Yes']
    unsolved_counts = murder_counts.loc[state]['No']

    plt.bar(i - bar_width / 2, solved_counts, width=bar_width, label=f'{state} - Solved', color=colors[0])
    plt.bar(i + bar_width / 2, unsolved_counts, width=bar_width, label=f'{state} - Unsolved', color=colors[1])

plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xticks(range(len(states)), states, rotation=90)
plt.title('Comparison of Solved vs Unsolved Murders by State (Logarithmic Scale)')
plt.xlabel('State')
plt.ylabel('Count (log scale)')
plt.legend().set_visible(False)
plt.show()