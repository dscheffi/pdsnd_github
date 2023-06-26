import time
import pandas as pd
import numpy as np

#global variables

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_data = { 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 99}
day_data = { 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6, 'all': 99}
reverse_month = { 1:'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
reverse_day = { 0: 'Monday', 1:'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

#function definitions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input ('Would you like to see data for Chicago, New York City, or Washington? \n').lower() 
    while city not in CITY_DATA:
        city = input ('Please try again choosing beteween one of the given Options!\n Would you like to see data for Chicago, New York City, or Washington? \n').lower()
    else:
    # get user input for month (all, january, february, ... , june)
        month = input ('Would you like to filter the data by month? Please choose one of the following: \nJanuary, February, March, April, June or all: \n').lower() 
        while month not in month_data:
            month = input ('Please try again choosing beteween one of the given Options!\nWould you like to filter the data by month? Please choose one of the following: \nJanuary, February, March, April, June or all: \n').lower()
        else:
    # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input ('Would you like to filter the data by day? Please choose one of the following:\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all: \n').lower() 
            while day not in day_data:
                day = input ('Please try again choosing beteween one of the given Options!\n Would you like to filter the data by day? Please choose one of the following:\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all: \n').lower()
            else:
                print('You chose the city: {}, the month: {}, the day: {}'.format(city.title(), month.title(), day.title()))
                print('-'*40)
    return city, month, day

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()
   
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.lower()]
        # or: day.lower()
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', reverse_month[popular_month])

    # display the most common day of week
    df['Start Time'] = pd.DatetimeIndex(df['Start Time'])
    df['day'] = df['Start Time'].dt.weekday
    popular_day = df['day'].mode()[0]
    print('Most Frequent Weekday (only relevant if you selected ALL days before):', reverse_day[popular_day])
    
    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0] 
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end) 

    # display most frequent combination of start station and end station trip
    df['Combi Station'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combi = df['Combi Station'].mode()[0]
    print('Most Frequent Combination of Start and End Station:', popular_combi) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel) 

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of Users:\n', user_types)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Gender of Users:\n', gender_count)
    except: 
        print('Gender information is only available for New York City and Chicago. \nFor a different selection of city the result will be displayed.')

    # Display earliest, most recent, and most common year of birth
    try:
        yob_min = int(df['Birth Year'].min())
        print('Earliest Year of Birth: ', yob_min)
        yob_max = int(df['Birth Year'].max())
        print('Most Recent Year of Birth: ', yob_max)
        yob_common = int(df['Birth Year'].mode()[0])
        print('Most Common Year of Birth: ', yob_common)
    except: 
        print('Information on the Year of Birth is only available for New York City and Chicago. \nFor a different Selection of City the Result will be displayed.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    start_row, end_row = 0, 4
    raw_request = input ('Would you like to see raw data? yes / no: \n').lower() 
    while raw_request == 'yes':
        print(df.loc[start_row : end_row, :])
        start_row += 5
        end_row += 5
        raw_request = input ('Would you like to see 5 more rows of raw data? yes / no: \n').lower() 
    else :
        print('Goodbye!')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()