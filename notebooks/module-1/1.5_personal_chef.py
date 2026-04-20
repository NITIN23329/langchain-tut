from dotenv import load_dotenv
load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite-preview',max_tokens=500)

from langchain.tools import tool
from tavily import TavilyClient
from typing import Dict, Any

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]: 
    """This method does web search"""
    return tavily_client.search(query)


from langchain.agents import create_agent

system_prompt = """
You are a world class chef. 
Your task is to recommend receipies from the ingredients specified by user by searching for it on web. 
Moreover you need to answer any queries user has regarding to cooking receipes. 
You can use tools whenevery necessary. 
"""
agent = create_agent(model = model, 
                     tools = [web_search],
                    system_prompt = system_prompt)
