import json
from typing import List, Dict
import re
import requests

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_floor_numbers(name: str) -> tuple:
    match = re.findall(r"(\d+)\s*\.\s*(\d+)", name)
    if match:
        return int(match[0][0]), int(match[0][1])
    return -1, -1


def filter_apartments_by_criteria(properties: List[Dict], room_count: int) -> List[Dict]:
    filtered_apartments = []
    for prop in properties:
        rooms =  prop.get("propertyDetails", {}).get("rooms") == room_count
        available_from = prop.get("transactionDetails", {}).get("availableFrom")
        address = prop.get("location", {}).get("address", "")
        name = prop.get("name", "")
        floor, apartment_number = extract_floor_numbers(name)

        if rooms and available_from is not None and floor > 4:
            if "157 B" in address and apartment_number in {1, 2, 3}:
                filtered_apartments.append(prop)
            elif "157 A" in address and apartment_number in {6, 7, 8}:
                filtered_apartments.append(prop)
    return filtered_apartments

def display_apartments(apartments: List[Dict]) -> None:
    for apartment in apartments:
        print(f"Name: {apartment['name']}")
        print(f"Size: {apartment.get('propertyDetails', {}).get('size')} sqm")
        print(f"Price: {apartment.get('transactionDetails', {}).get('price')} DKK")
        print(F"Available from: {apartment.get('transactionDetails', {}).get('availableFrom')}")
        print("-" * 50)

def fetch_apartment_data() -> Dict:

    url = "https://app.propstep.com/api/embedded/find"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "da-DK,da;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ro;q=0.5",
        "content-type": "application/json",
        "origin": "https://app.propstep.com",
        "priority": "u=1, i",
        "referer": "https://app.propstep.com/embedded/da?key=63f8ccf90dc1b4354970c7c3.63f8ddd7d619490f64a14f4d&list=true&isometric=true&first=isometric",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133")',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    data = {"key": "63f8ccf90dc1b4354970c7c3.63f8ddd7d619490f64a14f4d"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")

if __name__ == '__main__':
    data = fetch_apartment_data()
    properties = data.get("properties", [])
    two_room_apartments = filter_apartments_by_criteria(properties, 2)
    display_apartments(two_room_apartments)