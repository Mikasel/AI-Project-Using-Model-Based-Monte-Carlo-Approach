import numpy as np
import random
import datetime

# Constants

starting_points = {
    "Uskudar": "Istanbul",
    "Kadikoy": "Istanbul",
    "Besiktas": "Istanbul",
    "Zincirlikuyu": "Istanbul",
    "Sariyer": "Istanbul",
    "Beylikduzu": "Istanbul",
    "Kartal": "Istanbul",
    "Unalan": "Istanbul",
    "Mecidiyekoy": "Istanbul",
    "Eminonu": "Istanbul"
}

travel_times = {
    "Besiktas": 68,
    "Mecidiyekoy": 35,
    "Eminonu": 29,
    "Unalan": 64,
    "Kartal": 27 + 64,
    "Beylikduzu": 83,
    "Sariyer": 33 + 35,
    "Kadikoy_Eminonu": 30 + 29,
    "Kadikoy_Unalan": 8 + 64,
    "Uskudar_Besiktas": 15 + 68,
    "Uskudar_Kazlicesme": 40 + 20
}

routes = {
    "Kartal": ["M4 Metro", "34G Metrobus"],
    "Beylikduzu": ["34G Metrobus"],
    "Sariyer": ["M2 Metro", "34G Metrobus"],
    "Besiktas": ["Bus"],
    "Kadikoy_Eminonu": ["Ferry", "Bus"],
    "Kadikoy_Unalan": ["M4 Metro", "34G Metrobus"],
    "Uskudar_Besiktas": ["Ferry", "Bus"],
    "Uskudar_Kazlicesme": ["B1 Marmaray", "Bus"]
}

# Dynamic factors

def adjust_for_weather(time, date):
    # Increase travel time by 20% during rainy conditions
    # Assuming more rain in fall and winter (September to February)
    if date.month in [9, 10, 11, 12, 1, 2]:
        return time * 1.2
    return time

def adjust_for_rush_hour(time, departure_time):
    # Increase travel time by 30% during rush hours (7-9 AM and 5-7 PM)
    if (7 <= departure_time.hour < 9) or (17 <= departure_time.hour < 19):
        return time * 1.4
    return time

def simulate_conditions(base_time, departure_time, date):
    base_time = adjust_for_weather(base_time, date)
    base_time = adjust_for_rush_hour(base_time, departure_time)
    return base_time

# Model-Based Monte Carlo Algorithm

def monte_carlo_route_planning(starting_point, departure_time, date, simulations=100):
    base_time = travel_times.get(starting_point, 0)
    total_time = 0
    
    for _ in range(simulations):
        total_time += simulate_conditions(base_time, departure_time, date)
    
    average_time = total_time / simulations
    return average_time

def calculate_average_travel_times(starting_point):
    rush_hour_times = []
    rainy_month_times = []

    # Simulate rush hour (7:00 AM)
    rush_hour_time = datetime.time(7, 0)
    # Simulate non-rush hour (1:00 PM)
    non_rush_hour_time = datetime.time(13, 0)

    # Iterate over all rainy months
    for month in [9, 10, 11, 12, 1, 2]:
        # Simulate each month on the 15th
        date = datetime.date(2024, month, 15)
        
        # Calculate for rush hour
        rush_hour_times.append(monte_carlo_route_planning(starting_point, rush_hour_time, date))
        
        # Calculate for non-rush hour
        rainy_month_times.append(monte_carlo_route_planning(starting_point, non_rush_hour_time, date))

    # Calculate averages
    avg_rush_hour_time = np.mean(rush_hour_times)
    avg_rainy_month_time = np.mean(rainy_month_times)
    
    return avg_rush_hour_time, avg_rainy_month_time

# Main execution
if __name__ == "__main__":
    print("Available starting points:")
    for key in travel_times.keys():
        print(f"- {key.replace('_', ' ')}")
    
    user_input = input("Enter your starting point: ").strip().replace(' ', '_')
    
    if user_input in travel_times:
        departure_date_str = input("Enter your departure date (YYYY-MM-DD): ").strip()
        departure_time_str = input("Enter your departure time (HH:MM): ").strip()

        try:
            departure_date = datetime.datetime.strptime(departure_date_str, "%Y-%m-%d").date()
            departure_time = datetime.datetime.strptime(departure_time_str, "%H:%M").time()
            
            estimated_time = monte_carlo_route_planning(user_input, departure_time, departure_date)
            avg_rush_hour_time, avg_rainy_month_time = calculate_average_travel_times(user_input)
            
            print(f"Estimated travel time from {user_input.replace('_', ' ')} to Biruni University: {estimated_time:.2f} minutes")
            print(f"Average travel time during rush hours: {avg_rush_hour_time:.2f} minutes")
            print(f"Average travel time during rainy months: {avg_rainy_month_time:.2f} minutes")
        except ValueError:
            print("Invalid date or time format. Please try again.")
    else:
        print("Invalid starting point. Please try again.")
