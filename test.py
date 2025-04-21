import csv

def process_sport(file_name: str) -> dict:
    source = open(file_name, "r")
    sport_full = csv.DictReader(source)
    wanted_info = {
        "facility_id": str,
        "facility_name": str,
        "sport_lat": float,
        "sport_lon": float,
        "sport_played": str
    }
    sports = {}
    for row in sport_full:
        sport = {}
        try:
            for attribute, conversion in wanted_info.items():
                sport[attribute] = conversion(row[attribute])
            sports[sport["facility_id"]] = sport
        except:
            continue
    source.close()
    return sports

print(process_sport("sample_sport_facilities.csv"))