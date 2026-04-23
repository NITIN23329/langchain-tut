from dotenv import load_dotenv
load_dotenv()


from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import requests
from typing import Dict, Any

tavily_client = TavilyClient()
mcp = FastMCP("local_mcp_server")


@mcp.tool()
def web_search(query: str)-> Dict[str, Any]: 
    """does web search for information"""
    print("tool called with query: ", query)
    return tavily_client.search(query)



@mcp.resource("github://langchain-ai/langchain-mcp-adapters/main/README.md")
def langchain_resource():
    """ Resources to fetch infromation about langchain mcp adapters"""

    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    try: 
        resp = requests.get(url)
        return resp.text
    except Exception as e:
        return f"Error : {e}"
        


@mcp.prompt()
def my_prompt(): 
    """Analyze data from a langchain-ai repo file with comprehensive insights"""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - github_file: Access the langchain-ai repo files

    If the user asks a question that is not related to LangChain, LangGraph or LangSmith, you should say "I'm sorry, I can only answer questions about LangChain, LangGraph and LangSmith."

    You may try multiple tool and resource calls to answer the user's question.

    You may also ask clarifying questions to the user to better understand their question.
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")