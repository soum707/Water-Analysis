import requests
from bs4 import BeautifulSoup
import csv
import re

def clean_value(value):
    value = value.replace('&nbsp;', ' ')
    value = value.replace('\n', ' ')
    value = value.replace('&lt;', '<')
    value = re.sub(r'\s+', ' ', value)
    return value.strip()

def extract_numeric_value(value_str):
    # Extract numeric value and handle '<' cases
    try:
        # Remove any spaces before checking for '<'
        value_str = value_str.strip()
        
        # Handle '<' cases
        if value_str.startswith('<'):
            # Remove '<' and any spaces after it
            numeric_str = value_str[1:].strip()
        else:
            numeric_str = value_str
            
        # Extract the first number found
        match = re.search(r'([\d.]+)', numeric_str)
        if match:
            return float(match.group(1))
        return None
    except:
        return None

def scrape_water_quality_data():
    url = "https://www.charlottenc.gov/water/Water-Quality"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        boxes = soup.find_all('div', class_=['side-box-content', 'side-box-section'])
        
        data = []
        for box in boxes:
            if 'Alkalinity' in box.get_text():
                text = box.get_text(separator='\n')
                lines = text.split('\n')
                
                for line in lines:
                    line = clean_value(line)
                    if not line or "Monthly Mineral Analysis" in line:
                        continue
                        
                    if "Samples were" in line:
                        data.append(["Metadata", line, None])  # Add None for numeric value
                        continue
                    
                    if '=' in line:
                        try:
                            parameter, value = line.split('=', 1)
                            if parameter and value:
                                value = value.strip()
                                numeric_value = extract_numeric_value(value)
                                data.append([parameter.strip(), value, numeric_value])
                        except ValueError:
                            continue
                
                break

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Full error:", str(e))
        return []

def save_to_csv(data, filename="water_quality_data.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Mineral", "Value", "Numeric_Value"])  # Added new column header
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

def main():
    print("Starting water quality data scraping...")
    data = scrape_water_quality_data()
    
    if not data:
        print("No data was scraped. Please check if the website structure has changed.")
        return
    
    if save_to_csv(data):
        print(f"\nData successfully scraped and saved to water_quality_data.csv")
        print(f"Total records: {len(data)}")
        
        print("\nExtracted data:")
        for item in data:
            # Format the numeric value for display
            numeric_str = f"(Numeric: {item[2]})" if item[2] is not None else ""
            print(f"{item[0]}: {item[1]} {numeric_str}")
    else:
        print("Failed to save data to CSV file.")

if __name__ == "__main__":
    main()