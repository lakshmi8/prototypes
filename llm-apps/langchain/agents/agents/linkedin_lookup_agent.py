from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_core.pydantic_v1 import SecretStr

from tools.tools import get_linkedin_profile_url
import os

load_dotenv()


def lookup_profile_url(name: str):
    #api_key = os.getenv("OPENAI_API_KEY")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please set *_API_KEY in your .env file.")
    secret_api_key = SecretStr(api_key)

    #llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=secret_api_key)
    llm = ChatDeepSeek(temperature=0, model_name="deepseek-reasoner", api_key=secret_api_key)
    tools_for_agent = [
        Tool(
            name="WebCrawler for LinkedIn profile URL",
            func=get_linkedin_profile_url,
            description="This tool is useful when you need to get a LinkedIn profile URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    template = """Given the full name {name_of_person}, I want you to get me the LinkedIn profile URL of that person. Your answer should contain only the URL"""
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup_profile_url(name="Lakshmi Narayanan N V"))
