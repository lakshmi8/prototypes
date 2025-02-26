from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import SecretStr

from parsers.output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup_profile_url
import os

def get_linkedin_summary(name: str) -> Summary:

    # Calling my Agent (linkedin_lookup_agent) to get the linkedin profile url
    linkedin_profile_url = lookup_profile_url(name=name)

    # Scraping the linked profile
    linkedin_profile_information = scrape_linkedin_profile(linkedin_profile_url)

    summary_template = """
        given the Linkedin profile information {information} about a person I want you to create:
        1. A short summary
        2. Two interesting facts about that person
        \n {format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        template=summary_template,
        input_variables=["information"],
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )

    #api_key = os.getenv("OPENAI_API_KEY")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please set *_API_KEY in your .env file.")
    secret_api_key = SecretStr(api_key)

    #llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=secret_api_key)
    llm = ChatDeepSeek(temperature=0, model_name="deepseek-reasoner", api_key=secret_api_key)

    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_profile_information})

    return res


if __name__ == "__main__":
    load_dotenv()

    summary = get_linkedin_summary(name="Lakshmi Narayanan N V")
