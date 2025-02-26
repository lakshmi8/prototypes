import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from Linkedin profile"""
    response = requests.get(linkedin_profile_url, timeout=10)
    data = response.json()
    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        )
    )
