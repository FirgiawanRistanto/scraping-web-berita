
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def get_detik_articles(url, count=25):
    articles = []
    page = 1
    while len(articles) < count:
        response = requests.get(f"{url}?page={page}", headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tags = soup.find_all('article')

        if not article_tags:
            break

        for article in article_tags:
            if len(articles) >= count:
                break
            
            title_tag = article.find('h3', class_='media__title')
            if title_tag and title_tag.find('a'):
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                
                if link.startswith('https://travel.detik.com'):
                    # Scrape time from article page
                    try:
                        article_response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        waktu_tag = article_soup.find('div', class_='detail__date')
                        waktu_raw = waktu_tag.get_text(strip=True) if waktu_tag else 'Tidak ada waktu'

                        if waktu_raw != 'Tidak ada waktu':
                            # Example: "Rabu, 29 Okt 2025 16:10 WIB"
                            # Remove weekday and parse
                            try:
                                waktu_part = waktu_raw.split(', ', 1)[1] # "29 Okt 2025 16:10 WIB"
                                
                                month_map_abbr = {
                                    'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar',
                                    'Apr': 'Apr', 'Mei': 'May', 'Jun': 'Jun',
                                    'Jul': 'Jul', 'Agu': 'Aug', 'Sep': 'Sep',
                                    'Okt': 'Oct', 'Nov': 'Nov', 'Des': 'Dec'
                                }
                                for id_month_abbr, en_month_full in month_map_abbr.items():
                                    waktu_part = waktu_part.replace(id_month_abbr, en_month_full)
                                
                                waktu = datetime.strptime(waktu_part, '%d %b %Y %H:%M WIB').strftime('%Y-%m-%d %H:%M:%S')
                            except Exception as ve: # Catch any parsing errors
                                print(f"Error parsing date from Detik Travel {link}: {ve}")
                                waktu = 'Error'
                        else:
                            waktu = waktu_raw # Keep 'Tidak ada waktu'
                    except Exception as e: # This catches errors from requests or BeautifulSoup
                        print(f"Error scraping time from {link}: {e}")
                        waktu = 'Error'
                    articles.append({
                        'judul': title,
                        'link': link,
                        'source': 'Detik Travel',
                        'kategori': 'Travel',
                        'waktu': waktu,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    time.sleep(0.5) # Politeness delay
        page += 1
    return articles

def get_liputan6_articles(url, count=25):
    articles = []
    page = 1
    while len(articles) < count:
        response = requests.get(f"{url}?page={page}", headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tags = soup.find_all('article', class_='articles--iridescent-list--item')

        if not article_tags:
            break

        for article in article_tags:
            if len(articles) >= count:
                break
            
            title_tag = article.find('h4').find('a')
            if title_tag:
                title = title_tag.get('title')
                link = title_tag.get('href')
                try:
                    article_response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    waktu = 'Tidak ada waktu' # Default value

                    # Try the new selector first
                    waktu_tag_new = article_soup.select_one('div.readpage__author__update > span')
                    if waktu_tag_new:
                        # Get all direct text nodes, filtering out comments
                        waktu_parts = [s for s in waktu_tag_new.contents if isinstance(s, str)]
                        waktu_text = "".join(waktu_parts).strip()
                        # Example: "Diperbaharui 29 Okt 2025, 13:00 WIB"
                        # Use regex to extract the date and time part
                        match = re.search(r'(\d{1,2}\s+\w+\s+\d{4},\s+\d{2}:\d{2})\s+WIB', waktu_text)
                        if match:
                            waktu_part = match.group(1)
                            
                            # Replace abbreviated Indonesian month names with full English names
                            month_map_abbr = {
                                'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                                'Apr': 'April', 'Mei': 'May', 'Jun': 'June',
                                'Jul': 'July', 'Agu': 'August', 'Sep': 'September',
                                'Okt': 'October', 'Nov': 'November', 'Des': 'December'
                            }
                            for id_month_abbr, en_month_full in month_map_abbr.items():
                                waktu_part = waktu_part.replace(id_month_abbr, en_month_full)
                            
                            # Parse the datetime string
                            waktu = datetime.strptime(waktu_part, '%d %B %Y, %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                    
                    if waktu == 'Tidak ada waktu': # If not found with the new selector, try the old one
                        waktu_tag_old = article_soup.find('span', class_='read-page-box__author__updated')
                        if waktu_tag_old:
                            waktu_text = waktu_tag_old.get_text(strip=True)
                            # Example: "Diterbitkan 29 Oktober 2025, 10:42 WIB"
                            # Use regex to extract the date and time part
                            match = re.search(r'(\d{1,2}\s+\w+\s+\d{4},\s+\d{2}:\d{2})\s+WIB', waktu_text)
                            if match:
                                waktu_part = match.group(1)
                                
                                # Replace full Indonesian month names with full English names
                                month_map_full = {
                                    'Januari': 'January', 'Februari': 'February', 'Maret': 'March',
                                    'April': 'April', 'Mei': 'May', 'Juni': 'June',
                                    'Juli': 'July', 'Agustus': 'August', 'September': 'September',
                                    'Oktober': 'October', 'November': 'November', 'Desember': 'December'
                                }
                                for id_month_full, en_month_full in month_map_full.items():
                                    waktu_part = waktu_part.replace(id_month_full, en_month_full)
                                
                                # Parse the datetime string
                                waktu = datetime.strptime(waktu_part, '%d %B %Y, %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    print(f"Error scraping date from {link}: {e}")
                    waktu = 'Error'
                category = 'Global'
                
                articles.append({
                    'judul': title,
                    'link': link,
                    'source': 'Liputan6 Global',
                    'kategori': category,
                    'waktu': waktu,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        page += 1
    return articles

if __name__ == '__main__':
    detik_url = 'https://travel.detik.com/'
    liputan6_url = 'https://www.liputan6.com/global'
    
    print(f"Scraping {detik_url}...")
    detik_articles = get_detik_articles(detik_url, 25)
    print(f"Found {len(detik_articles)} articles from Detik Travel.")
    
    print(f"Scraping {liputan6_url}...")
    liputan6_articles = get_liputan6_articles(liputan6_url, 25)
    print(f"Found {len(liputan6_articles)} articles from Liputan6 Global.")
    
    all_articles = detik_articles + liputan6_articles 
    df = pd.DataFrame(all_articles)
    df.to_csv('hasil_crawling_berita.csv', index=False, encoding='utf-8-sig')
    
    print(f"Successfully scraped {len(all_articles)} articles and saved to hasil_crawling_berita.csv")
    print(df.head())
