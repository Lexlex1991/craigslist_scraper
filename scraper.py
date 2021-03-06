import requests
from bs4 import BeautifulSoup
import sys
import pprint 

def fetch_search_results(
    query=None, minAsk=None, maxAsk=None, bedrooms=None
):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://boston.craigslist.org/search/abo'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    return resp.content, resp.encoding

#Writing search results to html file

def write_results(_self_):    
    foo = resp.content
    with open('apartments.html', 'w') as outfile:
        outfile.write(foo)
    

#Read search results

def read_search_results():
    look_up = open('apartments.html')
    result = look_up.read()
    return resp.content, resp.encoding

#Parse from source

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

#Extracting listings

def extract_listings(parsed):
    location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all('p', class_='row', attrs=location_attrs)
    extracted = []
    for listing in listings:
        location = {key: listing.attrs.get(key, '') for key in location_attrs}
        link = listing.find('span', class_='pl').find('a')
        price_span = listing.find('span', class_='price')   # 
        this_listing = {
            'location': location,
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price_span.string.strip(),             # 
            'size': price_span.next_sibling.strip(' \n-/')  # 
        }
        extracted.append(this_listing)
    return extracted


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(
            minAsk=0, maxAsk=1700, bedrooms=2
        )
    doc = parse_source(html, encoding)    
    listings = extract_listings(doc)
    print len(listings)
    pprint.pprint(listings[0])       
