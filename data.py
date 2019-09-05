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
        curr = (row['ride_distance'] / 5280) * 1.15 + (row['ride_duration'] / 60) * .22 + 3.75
        curr += (curr * (row['ride_prime_time'] / 100))

        if curr < 5 or curr > 400:
            count += 1

        curr = max(curr, 5)
        curr = min(curr, 400)
        value += curr
    return round(value, 2), count

def get_all_driver_values():
    df = pd.DataFrame(driver_id_df['driver_id'].copy())
    l = []
    t = 0
    for index, row in df.iterrows():
        value, count = get_driver_value(row['driver_id'])
        l.append(value)
        t += count
    print("Rides Under/Over 5/400: " + str(t) + "    Total: 193503    " + " Percent: "  + str(t / 193503))
    df['driver_value'] = l
    df.to_csv('driver_values.csv')
    return df


print(get_all_driver_values())
