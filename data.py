import numpy
import pandas as pd
import datetime
import time
from datetime import date


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

# get the difference from the given dates
# date.today().strftime("%Y-%m-%d")
def get_date_difference(first, second):
    start = datetime.datetime.strptime(first, "%Y-%m-%d")
    end = datetime.datetime.strptime(second, "%Y-%m-%d")
    diff = end - start
    return diff.days

# return int representing when the ride was requested at
def get_time_zone(hour):
    if hour > 0 and hour <= 6:
        return 0
    elif hour > 6 and hour <= 10:
        return 1
    elif hour > 10 and hour <= 14:
        return 2
    elif hour > 14 and hour <= 19:
        return 3
    else:
        return 4

def get_prime_times(ride_id):
    list_of_prime = [0,0,0,0,0]
    curr_ride = get_events(ride_id)
    requested_at = curr_ride.loc[curr_ride['event'] == 'requested_at']
    requested_date_time = requested_at['timestamp'].to_string().split(' ')
    time = requested_date_time[-1]
    try:
        hour = int(time.split(':')[0])
        list_of_prime[get_time_zone(hour)] += 1
    except:
        print("Error: " + str(time))
    return list_of_prime

# print(get_prime_times('034f2e614a2f9fc7f1c2f77647d1b981'))

# returns all rides of the driver
def get_ride_times(driver_id):
    df = list_all_rides(driver_id)
    list_of_times = [0,0,0,0,0]
    for index, row in df.iterrows():
        curr_ride = get_events(row['ride_id'])
        requested_at = curr_ride.loc[curr_ride['event'] == 'requested_at']
        requested_date_time = requested_at['timestamp'].to_string().split(' ')
        ride_date = requested_date_time[-2]
        time = requested_date_time[-1]
        # try:
        #     list_of_times[5] = max(list_of_times[5], get_date_difference(ride_date, date.today().strftime("%Y-%m-%d")))
        # except:
        #     print("Error: " + driver_id)
        #     print("Curr Ride: " + curr_ride)
        #     print("Requested At: " + requested_at)

        try:
            hour = int(time.split(':')[0])
            list_of_times[get_time_zone(hour)] += 1
        except:
            print("Error: " + driver_id)
            print("Curr Ride: " + curr_ride)
            print("Requested At: " + requested_at)


    return list_of_times

# calculates the revenue generated for the given driver id
# returns the value (profit made) and the number of rides
def get_driver_value(driver_id):
    df = list_all_rides(driver_id)
    value = 0
    count = 0
    prime = 0
    prime_weight = 0
    prime_list = [0,0,0,0,0]
    for index, row in df.iterrows():
        count += 1
        curr = (row['ride_distance'] / 5280) * 1.15 + (row['ride_duration'] / 60) * .22 + 3.75
        curr += (curr * (row['ride_prime_time'] / 100))
        if (row['ride_prime_time'] != 0):
            prime += 1
            prime_weight += int(row['ride_prime_time'])
            prime_list = get_prime_times(row['ride_id'])
        curr = max(curr, 5)
        curr = min(curr, 400)
        value += curr
    return round(value, 2), count, prime, prime_weight, prime_list

# adds driver values, number of rides and average value per ride given to table
def get_all_driver_values(df):
    start_time = time.time()

    values = []
    number_of_rides = []
    average = []
    first = []
    second = []
    third = []
    fourth = []
    fifth = []
    prime_time = []
    prime_weights = []

    for index, row in df.iterrows():
        value, count, prime, prime_weight, prime_list = get_driver_value(row['driver_id'])
        values.append(value)
        number_of_rides.append(count)
        if count == 0:
            average.append(0)
        else:
            average.append(round(value / count, 2))
        
        # list_of_times = get_ride_times(row['driver_id'])
        first.append(prime_list[0])
        second.append(prime_list[1])
        third.append(prime_list[2])
        fourth.append(prime_list[3])
        fifth.append(prime_list[4])
        prime_time.append(prime)
        prime_weights.append(prime_weight)

        if ((index + 1) % 5 == 0):
            print(str(round((index + 1)/ len(df.index) * 100, 2)) + "%")

    df['driver_value'] = values
    df['ride_count'] = number_of_rides
    df['average_value_per_ride'] = average
    df['prime_time_count'] = prime_time
    df['prime_weight'] = prime_weights
    df['12:01 AM - 6 AM'] = first
    df['6:01 AM - 10 AM'] = second
    df['10:01 AM - 2 PM'] = third
    df['2:01 PM - 7 PM'] = fourth
    df['7:01 PM - 12 AM'] = fifth

    print("--- %s seconds ---" % (time.time() - start_time))

# constructs csv
def create_csv():
    df = pd.DataFrame(driver_id_df['driver_id'].copy())
    get_all_driver_values(df)
    df.to_csv('driver_profiles_prime.csv')

create_csv()