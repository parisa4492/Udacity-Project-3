import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTHS_LIST = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

DAYS_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'] 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').title()
        print('Your selected city was: ', city) 
        if city not in CITY_DATA.keys():
            print('\nInvalid answer, please consider your spelling and try again by inputing either Chicago, New York City, or Washington')
            continue
            city = input('Would you like to see data for Chicago, New York City, or Washington?\n').title()            
        else:
            break
                 
        # Get user input for month (all, january, february, ... , june)  
    while True: 
        month = input('\nWhich month you would like to see the data (January, February, March, April, May, June or all)? Please type-out the full name of the month.\n').title()
        print('Your selected month was: ', month)
        if month not in MONTHS_LIST:
            print('\nInvalid answer, please consider your spelling and try again!')
            continue
            month = input('Which month you would like to see the data (January, February, March, April, May, June or all)? Please type out the full name of th month.\n').title()
        else:
            break
 
    # Get user input for day of week (all, monday, tuesday, ... sunday)   
    try:
        day = input('\nWhich day you would like to see the data? please type a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.\n').title()
        while day not in DAYS_LIST:
            print('\nInvalid answer, please consider your spelling and try again!')
            day = input('Which day you would like to see the data? please type a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.\n')      
        print('Your selected day was: ', day) 
                         
              
        return city, month, day
    except Exception as e:
        print('An error has occured with your inputs: {}'.format(e))           
    print('-'*40)
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    while True:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour
        
        # Filter by month
        if month != 'all':
            # Use the index of the months list to obtain the corresponding input
            month = MONTHS_LIST.index(month) + 1
              
            # Filter by month to get the dataframe
            df = df[df['month'] == month]
              
        # Filter by day of the week
        if day != 'all':
            # Filter by day to get the dataframe
            df = df[df['day_of_week'] == day.title()] 
            
        return df
    else: 
        print('An error has occured with loading your file: {}'.format(e))  

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    try:
        df['month'] = df['Start Time'].dt.month
        common_month = df['month'].mode()[0]
        popular_month = MONTHS_LIST[common_month-1].title()
        print('The most popular month in', city, 'is:', popular_month) 
    except Exception as e:
        print('Couldn\'t obtain the most common month, as an Error has occurred: {}'.format(e))
             
    # Display the most common day of week
    try:
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        common_day_of_week = df['day_of_week'].mode()[0]
        print('The most popular weekday in', city, 'is:', common_day_of_week) 
    except Exception as e:
        print('Couldn\'t obtain the most common day of week, as an Error has occurred: {}'.format(e))

    # Display the most common start hour
    try:
        df['hour'] = df['Start Time'].dt.hour
        common_start_hour = df['hour'].mode()[0]
        print('The most popular starting hour in', city, 'is:', common_start_hour) 
    except Exception as e:
        print('Couldn\'t obtain the most common start hour, as an Error has occurred: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    try:
        common_start_station = df['Start Station'].mode()[0]
        common_start_station_amount = df['Start Station'].value_counts()[0]
        print('The most popular start station in', city, 'is:', common_start_station, 'and was used', common_start_station_amount, 'times.') 
    except Exception as e:
        print('Couldn\'t obtain the most commonly used start station, as an Error has occurred: {}'.format(e))

    # Display most commonly used end station
    try:
        common_end_station = df['End Station'].mode()[0]
        common_end_station_amount = df['End Station'].value_counts()[0]
        print('The most popular end station in', city, 'is:', common_end_station, 'and was used', common_end_station_amount, 'times.') 
    except Exception as e:
        print('Couldn\'t obtain the most commonly used end station, as an Error has occurred: {}'.format(e))

    # Display most frequent combination of start station and end station trip
    try:
        df['Trip Combination'] = df['Start Station'] + ' to ' + df['Start Station']
        common_trip_combination = df['Trip Combination'].mode()[0]
        common_trip_combination_amount = df.groupby(['Start Station', 'End Station']).size().max()
        print('The most frequent combination of start station and end station trip is:\n', common_trip_combination, '\n and was driven', common_trip_combination_amount, 'times')
    except Exception as e:
        print('Couldn\'t obtain the most frequent combination of start station and end station trip, as an Error has occurred:{}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    try:
        df['Trip Duration'] = df['End Time'] - df['Start Time']
        total_travel_time = df['Trip Duration'].sum()
        print('The total travel time was:', total_travel_time)
    except Exception as e:
        print('Couldn\'t obtain the total travel time of users, as an Error has occurred: {}'.format(e))

    # Display mean travel time
    try:
        mean_travel_time = df['Trip Duration'].mean()
        print('The mean travel time was:', mean_travel_time)
    except Exception as e:
        print('Couldn\'t obtain the mean travel time of users, as an Error has occurred: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('The amount and type of users in', city, 'are as followed:\n', user_types)
    except Exception as e:
        print('Couldn\'t obtain the type of users, as an Error has occurred: {}'.format(e))
        
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('The amount and gender of users in', city, 'are as followed:\n', gender)
    except Exception as e:
        print('Couldn\'t obtain the amount and gender of users, as an Error has occurred: {}'.format(e))      
    

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode())
        print('The age range of our customers in', city, 'is:\n' 
              ' Oldest customer was born in:', earliest_birth_year, '\n' 
              ' Youngest customer: was born in:', recent_birth_year, '\n' 
              ' Most of our customers are born in:', common_birth_year)
    except Exception as e:
        print('Couldn\'t obtain the age range of our customers, as an Error has occurred: {}'.format(e))
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def individual_data(df):
    """Displays 5 rows of data from the csv files for the selected city."""
    
    user_response = ['yes', 'no']
    view_raw_data = ''
    
    # Display individual trip data upon request by the user
    start_loc = 0
    while view_raw_data not in user_response:
        print('\nWould you like to view 5 rows of individual trip data? please entre yes or no.')
        view_raw_data = input().lower()
        #The raw data from the df is displayed if user enters Yes
        if view_raw_data == 'yes':
            print(df.head())
        elif view_raw_data not in user_response:
            print('\nPlease check your input; it does not seem that your input matches with any of the accepted responses.')
            print('Restarting...\n')

    #Extra while loop provides the option to display extra infromation if the user wants to continue viewing the data
    while view_raw_data == 'yes':
        print('Would you like to view more raw data?')
        start_loc += 5
        view_raw_data = input().lower()
        #If user enters Yes, this displays the next 5 rows of data
        if view_raw_data == 'yes':
             print(df[start_loc:start_loc+5])
        #If user enters No, extra while loop will break and user will no longer be able to continue viewing the data
        elif view_raw_data != 'yes':
             break                
    print('-'*80)
                

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        individual_data(df)

        restart = input('\nWould you like to restart? please enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
