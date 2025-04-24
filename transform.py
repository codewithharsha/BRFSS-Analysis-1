import pandas as pd

# Read the .xpt file into a pandas DataFrame
import sys
df = pd.read_csv(sys.argv[1])


print("Completed reading data!!")
print("Mapping Categorical data!!")

label_mappings = {
    'MENTHLTH': {
        88: 'None',
        77: "Don't know/Not sure",
        99: 'Refused'
    },
    'ADDEPEV3': {
        1: 'Yes',
        2: 'No',
        7: "Don't know/Not sure",
        9: 'Refused'
    },
    'GENHLTH': {
        1: 'Excellent',
        2: 'Very good',
        3: 'Good',
        4: 'Fair',
        5: 'Poor',
        7: "Don't know/Not Sure",
        9: 'Refused'
    },
    'INCOME3': {
        1: 'Less than $10,000',
        2: '$10,000 to <$15,000',
        3: '$15,000 to <$20,000',
        4: '$20,000 to <$25,000',
        5: '$25,000 to <$35,000',
        6: '$35,000 to <$50,000',
        7: '$50,000 to <$75,000',
        8: '$75,000 to <$100,000',
        9: '$100,000 to <$150,000',
        10: '$150,000 to <$200,000',
        11: '$200,000 or more',
        77: "Don't know/Not sure",
        99: 'Refused'
    },
    'EMPLOY1': {
        1: 'Employed for wages',
        2: 'Self-employed',
        3: 'Out of work ≥1 year',
        4: 'Out of work <1 year',
        5: 'Homemaker',
        6: 'Student',
        7: 'Retired',
        8: 'Unable to work',
        9: 'Refused'
    },
    'EDUCA': {
        1: 'Never attended school or only kindergarten',
        2: 'Grades 1-8 (Elementary)',
        3: 'Grades 9-11 (Some HS)',
        4: 'HS Graduate (Grade 12 or GED)',
        5: 'Some college or tech school',
        6: 'College graduate (4+ years)',
        9: 'Refused'
    },
    '_HLTHPL1': {
        1: 'Have insurance',
        2: 'No insurance',
        9: "Don't know/Refused/Missing"
    },
    '_SEX': {
        1: 'Male',
        2: 'Female'
    },
    '_AGEG5YR': {
        1: '18-24',
        2: '25-29',
        3: '30-34',
        4: '35-39',
        5: '40-44',
        6: '45-49',
        7: '50-54',
        8: '55-59',
        9: '60-64',
        10: '65-69',
        11: '70-74',
        12: '75-79',
        13: '80+',
        14: "Don't know/Refused/Missing"
    },
    '_RACEGR3': {
        1: 'White only, Non-Hispanic',
        2: 'Black only, Non-Hispanic',
        3: 'Other race only, Non-Hispanic',
        4: 'Multiracial, Non-Hispanic',
        5: 'Hispanic',
        9: "Don't know/Refused"
    },
    '_STATE' : {
    1: "Alabama",
    2: "Alaska",
    4: "Arizona",
    5: "Arkansas",
    6: "California",
    8: "Colorado",
    9: "Connecticut",
    10: "Delaware",
    11: "District of Columbia",
    12: "Florida",
    13: "Georgia",
    15: "Hawaii",
    16: "Idaho",
    17: "Illinois",
    18: "Indiana",
    19: "Iowa",
    20: "Kansas",
    22: "Louisiana",
    23: "Maine",
    24: "Maryland",
    25: "Massachusetts",
    26: "Michigan",
    27: "Minnesota",
    28: "Mississippi",
    29: "Missouri",
    30: "Montana",
    31: "Nebraska",
    32: "Nevada",
    33: "New Hampshire",
    34: "New Jersey",
    35: "New Mexico",
    36: "New York",
    37: "North Carolina",
    38: "North Dakota",
    39: "Ohio",
    40: "Oklahoma",
    41: "Oregon",
    44: "Rhode Island",
    45: "South Carolina",
    46: "South Dakota",
    47: "Tennessee",
    48: "Texas",
    49: "Utah",
    50: "Vermont",
    51: "Virginia",
    53: "Washington",
    54: "West Virginia",
    55: "Wisconsin",
    56: "Wyoming",
    66: "Guam",
    72: "Puerto Rico",
    78: "Virgin Islands"
  }

}

columns_to_decode = list(label_mappings.keys())

for col in columns_to_decode:
    df[col] = df[col].replace(label_mappings[col])

data = df[columns_to_decode]

print("Completed mapping lables!!")

data.shape

data.isnull().sum()

len(data['_STATE'].unique())

"""Generate weather data!"""

df_weather = pd.read_csv('weather_data.csv')

print("Fetcehd Weather data!!")

df_weather.shape

# Create a new column index combining Date and weather type
df_weather['Date'] = pd.to_datetime(df_weather['Date'])
df_weather['Date_str'] = df_weather['Date'].dt.strftime('%Y-%m-%d')

# Pivot table to wide format
df_weather_pivot = df_weather.pivot_table(
    index='State',
    columns='Date_str',
    values=['Temperature (C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Weather Type'],
    aggfunc='first'
)

# Flatten multi-level column names
df_weather_pivot.columns = [f"{col[1]}_{col[0]}" for col in df_weather_pivot.columns]
df_weather_pivot.reset_index(inplace=True)

df_weather_pivot.shape

if '_STATE' in data.columns:
    data = data.rename(columns={'_STATE': 'State'})

df_final = pd.merge(data, df_weather_pivot, on='State', how='left')

print("Completed merging with weather data!!")

print(f"Original rows before removing unwanted rows: {len(df_final)}")

# Define unwanted values
unwanted_values = [
    "Don't know/Not sure",
    "Refused",
    "Don't know/Refused/Missing",
    "Don't know/Refused"
]

# Remove rows containing any of the unwanted values in any column
df_final = df_final[~df_final.apply(lambda row: row.astype(str).isin(unwanted_values).any(), axis=1)].reset_index(drop=True)

# Preview cleaned data
print("Completed removing unwanted rows like Don't know/Not sure,Refused,Don't know/Refused/MissingDon't know/Refused!!")
print(f"No.of rows of after removing unwanted rows: {len(df_final)}")

df_final.isnull().sum()

df_final = df_final.dropna(subset=["EMPLOY1", "_RACEGR3", "EDUCA", "GENHLTH"])

print("Completed removing rows with null values in columns like employ,racegr3,education and genhlth!!")

# Calculate mode (most common value)
income_mode = df_final['INCOME3'].mode()[0]
print("Mode of income column is",income_mode)

# Fill null values with mode
df_final['INCOME3'].fillna(income_mode, inplace=True)
print("Completed filling null values of income column with mode!!")

# Convert MENTHLTH to numeric, turning invalid values into NaN
df_final['MENTHLTH'] = pd.to_numeric(df_final['MENTHLTH'], errors='coerce')

# Now, apply the PoorMentalHealth feature engineering
df_final['PoorMentalHealth'] = df_final['MENTHLTH'].apply(lambda x: 1 if pd.notnull(x) and x >= 14 else 0)

state_mental_health_pct = (
    df_final.groupby('State')['PoorMentalHealth']
    .mean()
    .mul(100)
    .round(2)
    .reset_index()
    .rename(columns={'PoorMentalHealth': 'PoorMentalHealthPct'})
)

def categorize_mental_health(x):
    if pd.isnull(x):
        return "Unknown"
    elif x >= 14:
        return "High Distress"
    elif x >= 7:
        return "Moderate"
    else:
        return "Low"

df_final['MENTHLTH_Level'] = df_final['MENTHLTH'].apply(categorize_mental_health)

print("Dataset shape after feature engineering",df_final.shape)

print("Handled null values of MENTHLTH column by replacing them with meadian value!!")

df_final['MENTHLTH'] = df_final['MENTHLTH'].fillna(df_final['MENTHLTH'].median())

print("The chunk size after processing is",df_final.shape)

df_final.to_csv('processed.csv', index=False)

print("The transformed dataset is saved!!")