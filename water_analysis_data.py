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

def scrape_water_quality_data():
    url = "https://www.charlottenc.gov/water/Water-Quality"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look specifically for the box with "Monthly Mineral Analysis"
        boxes = soup.find_all('div', class_=['side-box-content', 'side-box-section'])
        
        data = []
        for box in boxes:
            # Check if this box contains our data by looking for a known parameter
            if 'Alkalinity' in box.get_text():
                text = box.get_text(separator='\n')
                lines = text.split('\n')
                
                for line in lines:
                    line = clean_value(line)
                    if not line:
                        continue
                    
                    # Skip the title
                    if "Monthly Mineral Analysis" in line:
                        continue
                        
                    if "Samples were" in line:
                        data.append(["Metadata", line])
                        continue
                    
                    if '=' in line:
                        try:
                            parameter, value = line.split('=', 1)
                            if parameter and value:  # Only add if both parameter and value exist
                                data.append([parameter.strip(), value.strip()])
                        except ValueError:
                            continue
                
                # Once we've found and processed the correct box, we can break
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
            writer.writerow(["Parameter", "Value"])
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
            print(f"{item[0]}: {item[1]}")
    else:
        print("Failed to save data to CSV file.")

if __name__ == "__main__":
    main()