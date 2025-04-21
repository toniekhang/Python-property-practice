import json
import csv

def extract_information(row: dict, wanted_info: dict) -> dict:
    """ Extract required information from a dictionary

    Args:
        row (dict): a row in csv file, containing the full information about an amenity
        wanted_info (dict): required information and data type of it

    Returns:
        dict: a dictionary of information of the amenity
    """
    data = {}
    for k,v in wanted_info.items(): # Looping to populate the dictionary
        data[k] = v(row[k])
    return data

def process_schools(file_name: str) -> dict:
    """Extract school essential information from csv file

    Args:
        file_name (str): csv file containing school information

    Returns:
        dict: {school_id: {nested dictionary of school attributes}}
    """
    with open(file_name, "r", encoding="utf-8-sig") as source:
        schools_full = csv.DictReader(source)
        wanted_info = {"school_no": str, "school_name": str, "school_type": str, "school_lat": float, "school_lon": float}
        schools = {} # Create output dictionary
        for row in schools_full: 
            try:
                school = extract_information(row,wanted_info) # Nested dictionary of the school attributes
                schools[school["school_no"]] = school # Populate the output dictionary
            except: # Ignore row with empty location
                continue
    return schools
            

def process_medicals(file_name: str) -> dict:
    """Extract essential information of clinics from csv file.

    Args:
        file_name (str): csv file containing clinic information

    Returns:
        dict: {gp_code: {nested dictionary of clinic attributes}}
    """
    with open(file_name, "r", encoding="utf-8-sig") as source:
        medicals_full = csv.DictReader(source)
        wanted_info = {"gp_code": str, "gp_name": str, "location": json.loads}
        medicals = {} # Create output dictionary
        for row in medicals_full: 
            try:
                medical = extract_information(row,wanted_info) # Nested dictionary of the medical attributes
                location = location_handling(medical["location"]) # Getting gp_lat and gp_long from the location attribute
                medical["gp_lat"] = location["gp_lat"]
                medical["gp_lon"] = location["gp_lon"]
                del medical["location"]
                medicals[medical["gp_code"]] = medical # Populate the output dictionary
            except: # Ignore the row containing NA value of location
                continue
    return medicals

def location_handling(location_dict: dict) -> dict:
    """Extracting gp coordinates from the location"""
    coordinates = {}
    coordinates["gp_lat"] = location_dict["lat"]
    coordinates["gp_lon"] = location_dict["lng"]
    return coordinates  

def process_sport(file_name: str) -> dict:
    """Extract essential information of sprot facilities from csv file.

    Args:
        file_name (str): csv file containing information of sport facilities

    Returns:
        dict: {facility_id: {nested dictionary of sport faciltiy attributes}}
    """
    # Read csv file containing the full information of sport facility
    with open(file_name, "r", encoding="utf-8-sig") as source:
        sport_full = csv.DictReader(source)
        wanted_info = {
            "facility_id": str,
            "facility_name": str,
            "sport_lat": float,
            "sport_lon": float,
            "sport_played": str
        }
        sports = {} # Create output dictionary
        for row in sport_full:
            try:
                sport = extract_information(row,wanted_info) # Nested dictionary of sport facility attributes
                sports[sport["facility_id"]] = sport # Populate the output dictionary
            except:
                continue
    return sports

def main():
    school_dict = process_schools('sample_melbourne_schools.csv')
    medical_dict = process_medicals('sample_melbourne_medical.csv')
    sport_dict = process_sport('sample_sport_facilities.csv')

    sample_medical_code = 'mgp0041'
    print(f"There are {len(school_dict)} schools and {len(sport_dict)} sport facilities in our dataset")
    print(f"The location for {medical_dict[sample_medical_code]['gp_name']} is {medical_dict[sample_medical_code]['gp_lat']}, {medical_dict[sample_medical_code]['gp_lon']}")

if __name__ == '__main__':
    main()
