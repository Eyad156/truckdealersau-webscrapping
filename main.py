import requests as req
from bs4 import BeautifulSoup as soup
import time
import csv

def main():
    urls = [
        'https://truckdealers.com.au/buy/trucks/',
        'https://truckdealers.com.au/buy/trucks/prime-movers/',
        'https://truckdealers.com.au/buy/trucks/tippers/',
        'https://truckdealers.com.au/buy/trailers/',
        'https://truckdealers.com.au/buy/trucks/tray-flat-bed-trucks/',
        'https://truckdealers.com.au/buy/buses/',
        'https://truckdealers.com.au/buy/truck-trailer-parts/',
        'https://truckdealers.com.au/buy/forklifts-telehandlers/'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    
    all_data = []  # List to store all the scraped data

    for url in urls:
        try:
            response = req.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                page_soup = soup(response.text, 'html.parser')
                
                # Find all the post elements on the page
                posts = page_soup.find_all("div", class_="truck-result odd")
                
                for post in posts:
                    # Adjust the selector as per the actual HTML structure of the page
                    name = post.find("h2", class_="details-title")
                    categories = post.find("span", class_="categories")
                    dealer_id = post.find("div", class_="serp-dealer-license")
                    dealer_used = post.find("div", class_="attribute dealer_used")
                    dealer_new = post.find("div", class_="attribute dealer_new")
                    
                    # Handle multiple elements with the same class
                    attributes = post.find_all("div", class_="attribute")
                    year, odometer, state = None, None, None
                    
                    # Extract specific attributes based on context or label
                    for attr in attributes:
                        if "Year:" in attr.get_text():
                            year = attr.get_text(strip=True)
                        elif "Odometer:" in attr.get_text():
                            odometer = attr.get_text(strip=True)
                        elif "State:" in attr.get_text():
                            state = attr.get_text(strip=True)

                    # Append the data to the all_data list as a dictionary
                    all_data.append({
                        "Name": name.get_text(strip=True) if name else "N/A",
                        "Categories": categories.get_text(strip=True) if categories else "N/A",
                        "Dealer ID": dealer_id.get_text(strip=True) if dealer_id else "N/A",
                        "Dealer Used": dealer_used.get_text(strip=True) if dealer_used else "N/A",
                        "Dealer New": dealer_new.get_text(strip=True) if dealer_new else "N/A",
                        "Year": year if year else "N/A",
                        "Odometer": odometer if odometer else "N/A",
                        "State": state if state else "N/A"
                    })

            else:
                print(f"The URL {url} returned status code {response.status_code}. It may be blocked.")
        
        except req.exceptions.RequestException as e:
            print(f"Error reaching {url}: {e}")
        
        time.sleep(2)

    # Write the data to a CSV file with line-by-line formatting
    with open('truck_data.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        for data in all_data:
            writer.writerow([f"Name: {data['Name']}"])
            writer.writerow([f"Categories: {data['Categories']}"])
            writer.writerow([f"Dealer ID: {data['Dealer ID']}"])
            writer.writerow([f"Dealer Used: {data['Dealer Used']}"])
            writer.writerow([f"Dealer New: {data['Dealer New']}"])
            writer.writerow([f"Year: {data['Year']}"])
            writer.writerow([f"Odometer: {data['Odometer']}"])
            writer.writerow([f"State: {data['State']}"])
            writer.writerow([])  # Blank line between records

    print("Data has been exported to truck_data.csv")

if __name__ == "__main__":
    main()
