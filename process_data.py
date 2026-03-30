import pandas as pd
import datetime
import glob
import os

def format_seconds(s):
    if pd.isna(s) or s == "": 
        return ""
    return str(datetime.timedelta(seconds=int(s)))

def process_latest_activities():
    # Zoek naar het meest recente activiteitenbestand in de 'data' map
    files = glob.glob("data/activities_*.csv")
    if not files:
        print("Geen activiteitenbestanden gevonden om te verwerken.")
        return

    input_file = max(files, key=os.path.getctime)
    print(f"Verwerken van bestand: {input_file}")

    df = pd.read_csv(input_file)

    # Berekeningen en conversies
    df['Afstand (km)'] = (df['distance'] / 1000).round(2)
    df['Gem. Snelheid (km/u)'] = (df['average_speed'] * 3.6).round(1)
    df['Max. Snelheid (km/u)'] = (df['max_speed'] * 3.6).round(1)
    df['Bewegingstijd'] = df['moving_time'].apply(format_seconds)
    df['Totale tijd'] = df['elapsed_time'].apply(format_seconds)
    df['Hoogtemeters (m)'] = df['total_elevation_gain'].round(0)

    # Selectie en hernoemen van kolommen
    column_mapping = {
        'start_date_local': 'Datum',
        'name': 'Naam',
        'type': 'Type',
        'Afstand (km)': 'Afstand (km)',
        'Bewegingstijd': 'Bewegingstijd',
        'Totale tijd': 'Totale tijd',
        'Gem. Snelheid (km/u)': 'Gem. Snelheid (km/u)',
        'Max. Snelheid (km/u)': 'Max. Snelheid (km/u)',
        'average_heartrate': 'Gem. Hartslag',
        'icu_average_watts': 'Gem. Vermogen (W)',
        'Hoogtemeters (m)': 'Hoogtemeters (m)',
        'calories': 'Calorieën',
        'average_cadence': 'Gem. Cadans'
    }

    # Filter op beschikbare kolommen
    cols_to_keep = [c for c in column_mapping.keys() if c in df.columns or c in ['Afstand (km)', 'Gem. Snelheid (km/u)', 'Max. Snelheid (km/u)', 'Bewegingstijd', 'Totale tijd', 'Hoogtemeters (m)']]
    formatted_df = df[cols_to_keep].rename(columns=column_mapping)

    # Opslaan als een vast bestand voor de GitHub Action artifact
    output_path = "data/activities_formatted.csv"
    formatted_df.to_csv(output_path, index=False)
    print(f"Succesvol opgeslagen in: {output_path}")

if __name__ == "__main__":
    process_latest_activities()
