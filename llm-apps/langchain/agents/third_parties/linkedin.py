import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from Linkedin profile"""

    if mock:
        linkedin_profile_url = "https://gist.github.com/lakshmi8/37b554f18b1011e04204d4ee23fe3ab5/raw"
        response = requests.get(linkedin_profile_url, timeout=10)
        scraped_data = response.json()
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey":  os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url
        }
        response = requests.get(api_endpoint, params=params, timeout=10)
        scraped_data = response.json().get("person")

    return scraped_data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://gist.github.com/lakshmi8/37b554f18b1011e04204d4ee23fe3ab5", True
        )
    )
