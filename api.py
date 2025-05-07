import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Booking.com search results page
url = "https://www.booking.com/searchresults.en-gb.html?ss=Marrakech&ssne=Marrakech&ssne_untouched=Marrakech&label=en-ma-booking-desktop-HFqwIxxzRAmHDiKj_ApqpgS652796016120%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1009974%3Ali%3Adec%3Adm&aid=2311236&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-38833&dest_type=city&group_adults=2&no_rooms=1&group_children=0"

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:    
    # Send HTTP request
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize lists to store data
    hotels_data = []
    
    # Find all hotel entries (adjust selector as needed)
    hotel_entries = soup.find_all('div', {'data-testid': 'property-card'})
    
    for hotel in hotel_entries:
        # Extraction des données de base / Basic data extraction
        name = hotel.find('div', class_='b87c397a13').get_text(strip=True) if hotel.find('div', class_='b87c397a13') else 'N/A'
        description = hotel.find('div', class_='fff1944c52').get_text(strip=True) if hotel.find('div', class_='fff1944c52') else 'N/A'
        review_score = hotel.find('div', class_='f63b14ab7a').get_text(strip=True) if hotel.find('div', class_='f63b14ab7a') else 'N/A'
        
        # Extraction de données supplémentaires / Additional data extraction
        price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        price = price_element.get_text(strip=True) if price_element else 'N/A'
        
        # Extraction de la note textuelle / Text rating extraction
        rating_element = hotel.find('div', class_='b5cd09854e')
        rating = rating_element.get_text(strip=True) if rating_element else 'N/A'
        
        # Extraction de la distance / Distance extraction
        distance_element = hotel.find('span', {'data-testid': 'distance'})
        distance = distance_element.get_text(strip=True) if distance_element else 'N/A'
        
        # Extraction des équipements / Facilities extraction
        facilities_element = hotel.find('div', class_='d22a7c133b')
        facilities = facilities_element.get_text(strip=True) if facilities_element else 'N/A'
        
        # Données constantes / Constant data
        city = 'Marrakech'  # Tous les hôtels sont à Marrakech / All hotels are in Marrakech
        date_scraped = pd.Timestamp.now().strftime('%Y-%m-%d')  # Date d'extraction / Scraping date
        
        # Append data to list with each variable in its own column
        hotels_data.append({
            'Nom_Hotel': name,
            'Description': description,
            'Note': review_score,
            'Evaluation_Textuelle': rating,
            'Prix': price,
            'Distance': distance,
            'Equipements': facilities,
            'Ville': city,
            'Date_Extraction': date_scraped
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(hotels_data)
    df.to_csv('marrakech_hotels.csv', index=False, encoding='utf-8')
    print("Données extraites avec succès et sauvegardées dans 'marrakech_hotels.csv'")
    print(f"Nombre d'hôtels extraits: {len(hotels_data)}")
    
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la récupération de la page: {e}")
except Exception as e:
    print(f"Une erreur s'est produite: {e}")