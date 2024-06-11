import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    total_rows = df.shape[0]
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((len(df[df['education'] == 'Bachelors']) / total_rows) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education_levels = ['Bachelors', 'Masters', 'Doctorate']

    higher_education_mask = df['education'].isin(higher_education_levels)
    how_many_higher_educated = len(df[higher_education_mask])

    high_income_mask = df['salary'] == '>50K'

    higher_education_high_income_count = len(df[higher_education_mask & high_income_mask])
    higher_education_rich = (higher_education_high_income_count / how_many_higher_educated) * 100
    higher_education_rich = round(higher_education_rich, 1)

    lower_education_mask = ~higher_education_mask
    how_many_lower_educated = len(df[lower_education_mask])
    lower_education_high_income_count = len(df[lower_education_mask & high_income_mask])
    lower_education_rich = round((lower_education_high_income_count / how_many_lower_educated) * 100, 1)
    

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_hours_workers = df[df['hours-per-week'] == min_work_hours]
    min_hours_high_income_workers = df[(df['hours-per-week'] == min_work_hours) & high_income_mask]
    num_min_workers = len(min_hours_high_income_workers)

    rich_percentage = round(num_min_workers/len(min_hours_workers) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    # Select only the columns of interest
    selection = df[['native-country', 'salary']]

    # Count total population per country
    total_population_counts = selection.groupby('native-country').size().reset_index(name='total_population')

    # Count high-income population per country
    high_income_counts = selection[selection['salary'] == '>50K'].groupby('native-country').size().reset_index(name='high_income_count')

    # Merge total population and high-income counts
    merged_data = pd.merge(total_population_counts, high_income_counts, on='native-country', how='left')

    # Calculate the percentage of high-income individuals per country
    merged_data['percentage_high_income'] = (merged_data['high_income_count'] / merged_data['total_population']) * 100

    # Find the country with the highest percentage of high-income individuals
    highest_earning_country = merged_data.loc[merged_data['percentage_high_income'].idxmax(), 'native-country']
    highest_earning_country_percentage = round(merged_data['percentage_high_income'].max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    # Filter the DataFrame for individuals earning more than 50K in India
    high_income_india = df[high_income_mask & (df['native-country'] == 'India')]

    # Count the occurrences of each occupation
    occupation_counts = high_income_india['occupation'].value_counts()

    # Identify the most popular occupation
    most_popular_occupation = occupation_counts.idxmax()

    print("Most popular occupation for those who earn >50K in India:", most_popular_occupation)
    top_IN_occupation = most_popular_occupation

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

if __name__ == "__main__":
    calculate_demographic_data()