import pandas as pd
import random
import os  # Add os module for file path handling

# Color constants
COLORS = {
    "RESET": "\033[0m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "BOLD": "\033[1m"
}

# Party-specific colors (for Turkish political parties)
PARTY_COLORS = {
    "AKP": COLORS["YELLOW"],
    "CHP": COLORS["RED"],
    "MHP": COLORS["GREEN"],
    "HDP": COLORS["MAGENTA"]
    # Add other parties as needed
}

# Function to get color for a party
def get_party_color(party):
    return PARTY_COLORS.get(party, COLORS["WHITE"])

def load_data(file_name):
    df = pd.read_csv(file_name)
    df = df.dropna(axis=1, how='all')  # drop completely empty columns
    return df

def average_and_prediction(df, selected_count=5):
    selected_polls = df.sample(n=selected_count)
    averages = selected_polls.mean()

    prediction = {}
    for party, rate in averages.items():
        variation = random.uniform(-1.0, 1.0)  # ±1 deviation
        predicted_rate = max(0, round(rate + variation, 2))  # ensure not negative
        prediction[party] = predicted_rate

    return prediction

def print_prediction(prediction):
    print(f"\n{COLORS['BOLD']}{COLORS['CYAN']}📊 Election Prediction (%):{COLORS['RESET']}\n")
    
    total_seats = 550
    seat_distribution = {}

    # Filter parties that pass 10% threshold
    eligible_parties = {party: rate for party, rate in prediction.items() if rate >= 10}
    total_eligible_percentage = sum(eligible_parties.values())
    
    # Calculate seats only for eligible parties
    for party, rate in sorted(prediction.items(), key=lambda x: x[1], reverse=True):
        color = get_party_color(party)
        
        if rate >= 10:
            # Calculate seats proportionally from the eligible parties' total votes
            seats = int(round((rate / total_eligible_percentage) * total_seats))
            seat_distribution[party] = seats
            print(f"{color}{party:<15}: {COLORS['BOLD']}{rate:>5.2f} % ({seats} MV){COLORS['RESET']}")
        else:
            # Parties below threshold get 0 seats
            seat_distribution[party] = 0
            print(f"{color}{party:<15}: {COLORS['BOLD']}{rate:>5.2f} % (0 MV - Below 10% threshold){COLORS['RESET']}")

    # Check for rounding issues and adjust to ensure exactly 550 seats
    total_allocated = sum(seat_distribution.values())
    if total_allocated != total_seats and eligible_parties:
        # Adjust seats for the party with the highest votes
        top_party = max(eligible_parties.items(), key=lambda x: x[1])[0]
        seat_distribution[top_party] += (total_seats - total_allocated)
        
    print(f"\n{COLORS['BOLD']}Total Seats Allocated: {sum(seat_distribution.values())}/550{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}Note: Parties with less than 10% votes receive no seats.{COLORS['RESET']}")

def main():
    print(f"\n{COLORS['BOLD']}{COLORS['GREEN']}📁 Which dataset would you like to use?{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}1 - {COLORS['BOLD']}June 2015{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}2 - {COLORS['BOLD']}November 2015{COLORS['RESET']}")
    choice = input(f"\n{COLORS['YELLOW']}Your choice (1 or 2): {COLORS['RESET']}")
    
    # Get directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if choice == "1":
        file_path = os.path.join(script_dir, "june.csv")
        df = load_data(file_path)
        print(f"{COLORS['GREEN']}Loading June 2015 dataset...{COLORS['RESET']}")
    elif choice == "2":
        file_path = os.path.join(script_dir, "november.csv")
        df = load_data(file_path)
        print(f"{COLORS['GREEN']}Loading November 2015 dataset...{COLORS['RESET']}")
    else:
        print(f"{COLORS['RED']}Invalid choice.{COLORS['RESET']}")
        return

    prediction = average_and_prediction(df)
    print_prediction(prediction)

if __name__ == "__main__":
    main()