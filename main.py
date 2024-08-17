import requests as req
from bs4 import BeautifulSoup as soup
import time

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
                    dealer_used = post.find("div",class_="attribute dealer_used")
                    dealer_new = post.find("div",class_="attribute dealer_new")
                    year = post.find("div",class_="attribute-val")
                    # Get text if the elements are found
                    if name:
                        print("Name:", name.get_text(strip=True))
                    else:
                        print(f"Could not find the name in a post from {url}")
                        
                    if categories:
                        print("Categories:", categories.get_text(strip=True))
                    
                    if dealer_id:
                        print(dealer_id.get_text(strip=True))
                    if dealer_used:
                        print(dealer_used.get_text(strip=True))

                    if year:
                        print("Year:",year)
                    print("-" * 40)
                    
            else:
                print(f"The URL {url} returned status code {response.status_code}. It may be blocked.")
        
        except req.exceptions.RequestException as e:
            print(f"Error reaching {url}: {e}")
        
        time.sleep(2)
    
if __name__ == "__main__":
    main()
