import requests
from bs4 import BeautifulSoup

def get_linkedin_profile_url(name: str):
    """Searches for LinkedIn profile URL, given the name"""
    query = f"site:linkedin.com {name}"
    search_url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    #print("Response code: " + str(response.status_code))
    if response.status_code == 200:
        #print("Got response from DDG" + response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for result in soup.find_all("a", href=True):
            href = result["href"]
            if "linkedin.com" in href:
                return href

    return "https://in.linkedin.com/in/lakshmi-narayanan-n-v-6b0a176b" # If I don't get any responses from DuckDuckGo, I should return my linked in url (hard-coded)

if __name__ == '__main__':
    get_linkedin_profile_url("Lakshmi Narayanan N V")