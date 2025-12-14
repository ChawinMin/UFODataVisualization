import folium
import pandas as pd
import os

# Load your dataset here
ufo_data_path = 'ufo_sightings (1).csv'
ufo_data = pd.read_csv(ufo_data_path, sep=',', nrows=100000)

# The name of the month. Default is January
monthname = "January"

# All the months in an array
months = ["January", "February", "March", "April", "May",
          "June", "July", "August", "September", "October", "November", "December"]

# Function to create a map for a specific year
def create_ufo_sightings_map(year, data):

    year_exists = ufo_data['Dates.Sighted.Year'].isin([year]).any()
    if not year_exists:
        return print(f"The year {year} doesn't exist within this database")

    # folder for the year
    folder = f'ufo_sightings_{year}'
    
    # Check if the folder exists, and if not, create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # for loop to go through all the months
    for mymonth in range(1,13):

        # Creates and formats the month number
        formatted_month = f"{mymonth:02d}"

        # Create a base map centered around the United States
        ufo_map = folium.Map(location=[47.033281, -130.732018], zoom_start=4)

        # Filter the dataset for the specified year and month
        filtered_data = data[(data['Dates.Sighted.Year'] == year) & (data['Dates.Sighted.Month'] == mymonth)]
    
        # Iterate over the filtered dataset and add markers to the map
        for index, sighting in filtered_data.iterrows():
            
            # Goes through all the months to find the correct one
            lastmonth = 0
            for month in months:
                if(mymonth == months.index(month) + lastmonth + 1):
                    lastmonth = months.index(month)
                    monthname = month
                    break

            # Creates the UFO marker location
            folium.Marker(
                location=[sighting['Location.Coordinates.Latitude '], sighting['Location.Coordinates.Longitude ']],
                tooltip=f"State: {sighting['Location.State']} Coords: {sighting['Location.Coordinates.Latitude ']}, {sighting['Location.Coordinates.Longitude ']}",
                icon=folium.Icon(icon_size=(40, 40), color = "red"),
            ).add_to(ufo_map)
            
            # Creates the date of the map
            folium.Marker(
                [36.598285, -142.378694],
                icon=folium.DivIcon(
                icon_size=(250,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 20pt">{monthname}, {year}</div>',
                )
            ).add_to(ufo_map)

        # Save the map to an HTML file
        ufo_map.save(f'{folder}/ufo_sightings_map_{year}_{formatted_month}_{monthname}.html')

# Ask the player to put in a year
myyear = int(input("Please input a year: "))

# Create and save a map for any year by the user
create_ufo_sightings_map(myyear, ufo_data)

# Ask the user if they want to keep continuing
while(True):
    userInput = input("Do you wish to keep entering years? (Yes or no): ")
    normalized_input = userInput.strip().lower()
    if normalized_input.startswith('y'):
        myyear = int(input("Please input a year: "))
    else:
        print("Have a nice day, thank you for using our program <3")
        break
    create_ufo_sightings_map(myyear, ufo_data)