import pandas as pd
import os
import random
import time

# Terminal colors
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "CYAN": "\033[96m",
    "YELLOW": "\033[93m",
    "MAGENTA": "\033[95m",
    "BLUE": "\033[94m",
    "WHITE": "\033[97m"
}

def get_color(party):
    colors = {
        "AKP": COLORS["YELLOW"],
        "CHP": COLORS["RED"],
        "İYİ": COLORS["CYAN"],
        "MHP": COLORS["MAGENTA"],
        "Other": COLORS["WHITE"]
    }
    return colors.get(party, COLORS["WHITE"])

def make_prediction(df, city, poll_count=3):
    selected = df.sample(n=min(poll_count, len(df)))
    averages = selected.mean()

    prediction = {}
    for party in averages.index:
        deviation = random.uniform(-1, 1)
        rate = max(0, round(averages[party] + deviation, 2))
        prediction[party] = rate

    winner = max(prediction, key=prediction.get)
    
    output = []
    output.append(f"{COLORS['BOLD']}{COLORS['BLUE']}📍 {city.upper()} Prediction:{COLORS['RESET']}")
    for party, rate in sorted(prediction.items(), key=lambda x: x[1], reverse=True):
        output.append(f"{get_color(party)}{party:<8}: {COLORS['BOLD']}{rate}%{COLORS['RESET']}")
    output.append(f"{COLORS['GREEN']}🏆 Predicted winner: {COLORS['BOLD']}{winner}{COLORS['RESET']}")
    
    return output

def display_side_by_side(left_prediction, right_prediction):
    max_lines = max(len(left_prediction) if left_prediction else 0, 
                    len(right_prediction) if right_prediction else 0)
    
    for i in range(max_lines):
        left_line = left_prediction[i] if left_prediction and i < len(left_prediction) else ""
        right_line = right_prediction[i] if right_prediction and i < len(right_prediction) else ""
        print(f"{left_line:<50} {right_line}")
    
    print()

def main():
    # Folder containing CSV files
    path = os.path.dirname(os.path.abspath(__file__))
    city_files = {
        "Adana": "anketler/adana_2019_oy_oranlari.csv",
        "Ankara": "anketler/ankara_2019_oy_oranlari.csv",
        "Antalya": "anketler/antalya_2019_oy_oranlari.csv",
        "Balıkesir": "anketler/balıkesir_2019_oy_oranlari.csv",
        "Bursa": "anketler/bursa_2019_oy_oranlari.csv",
        "Denizli": "anketler/denizli_2019_oy_oranlari.csv",
        "Eskişehir": "anketler/eskişehir_2019_oy_oranlari.csv",
        "Hatay": "anketler/hatay_2019_oy_oranlari.csv",
        "İstanbul": "anketler/istanbul_2019_oy_oranlari.csv",
        "İzmir": "anketler/izmir_2019_oy_oranlari.csv"
    }

    for x in range(0, 4):
        b = "🗳 2019 Local Election Prediction Simulation Starting" + "." * x
        print(f"{COLORS['BOLD']}{COLORS['CYAN']}{b}{COLORS['RESET']}", end="\r")
        time.sleep(0.5)
    
    print()  # Add a newline after the loading animation
    
    # Convert to list for easier pairing
    city_list = list(city_files.items())
    
    # Process cities in pairs
    for i in range(0, len(city_list), 2):
        left_city, left_file = city_list[i]
        left_file_path = os.path.join(path, left_file)
        left_prediction = None
        
        if os.path.exists(left_file_path):
            df = pd.read_csv(left_file_path)
            left_prediction = make_prediction(df, left_city)
        else:
            left_prediction = [f"{COLORS['RED']}File not found: {left_file}{COLORS['RESET']}"]
        
        # Check if there's a right city in this pair
        right_prediction = None
        if i + 1 < len(city_list):
            right_city, right_file = city_list[i + 1]
            right_file_path = os.path.join(path, right_file)
            
            if os.path.exists(right_file_path):
                df = pd.read_csv(right_file_path)
                right_prediction = make_prediction(df, right_city)
            else:
                right_prediction = [f"{COLORS['RED']}File not found: {right_file}{COLORS['RESET']}"]
        
        display_side_by_side(left_prediction, right_prediction)

if __name__ == "__main__":
    main()