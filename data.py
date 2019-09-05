import numpy
import pandas as pd

driver_id_df = pd.read_csv("driver_ids.csv")
ride_id_df = pd.read_csv("ride_ids.csv")
rides_df = pd.read_csv("ride_timestamps.csv")

# gets all rides by driver
def list_all_rides(driver_id):
    df = ride_id_df.loc[ride_id_df['driver_id'] == driver_id]
    return df

# gets the specfic event for the given ride ID
def get_events(ride_id):
    df = rides_df.loc[rides_df['ride_id'] == ride_id]
    return df
    
# calculates the revenue generated for the given driver id
def get_driver_value(driver_id):
    df = list_all_rides(driver_id)
    value = 0
    count = 0
    for index, row in df.iterrows():
        count += 1
        curr = (row['ride_distance'] / 5280) * 1.15 + (row['ride_duration'] / 60) * .22 + 3.75
        curr += (curr * (row['ride_prime_time'] / 100))
        curr = max(curr, 5)
        curr = min(curr, 400)
        value += curr
    return round(value, 2), count

def get_all_driver_values():
    df = pd.DataFrame(driver_id_df['driver_id'].copy())
    values = []
    number_of_rides = []
    average = []

    for index, row in df.iterrows():
        value, count = get_driver_value(row['driver_id'])
        values.append(value)
        number_of_rides.append(count)
        if count == 0:
            average.append(0)
        else:
            average.append(round(value / count, 2))

    df['driver_value'] = values
    df['ride_count'] = number_of_rides
    df['average_value_per_ride'] = average
    df.to_csv('driver_values.csv')
    return df


print(get_all_driver_values())
