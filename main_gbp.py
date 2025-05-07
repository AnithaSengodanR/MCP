from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os
from bs4 import BeautifulSoup # type: ignore
import json
import logging

load_dotenv()

# initialize server
mcp = FastMCP("tech_cashblocks")

USER_AGENT = "news-app/1.0"
logger = logging.getLogger("httpx")
GBP_APIS = {
    "CashblockList": "https://demoapps.tcsbancs.com/Core/accountManagement/account/blockList/101000000101814?pageNum=1&PageSize=22",
    "AccountDetailList" : "https://demoapps.tcsbancs.com/Core/accountManagement/account/balanceDetails/101000000101814?pageNum=1&PageSize=22"
}

async def fetch_GBPData(url: str):
    """It pulls and summarizes the List of cash blocks on an account."""
    async with httpx.AsyncClient() as client:
        try:
            logging.info(f"[DEBUG]Fetching data from {url}...")
           ## url ="https://demoapps.tcsbancs.com/Core/accountManagement/account/blockList/101000000101814?pageNum=1&PageSize=22"
            headers = {'userId': '1',
                       'entity': 'GPRDTTSTOU',
                       'languageCode': '1',
                       "Accept": "application/json"}
           ## print.log(f"[DEBUG]Fetching data from {url}...");
           
            response = await client.get(url,headers=headers, timeout=30.0)
           # logging.info("Response"+response.text );
            #logging.info("Response in Json"+response.json() );
         ##   soup = BeautifulSoup(response.text, "html.parser")
           ## paragraphs = soup.find_all("p")
            ##text = " ".join([p.get_text() for p in paragraphs[:5]]) 
            ##return text
            return response.json()
        except httpx.TimeoutException:
            return "Timeout error"

@mcp.tool()  
async def get_account_cashblks(source: str):
    """
    Fetches the List of Cashblocks created for an account.

    Args:
    source: Name of the Account number.

    Returns:
    List of cashblocks created in that account.
    """
   ## if source not in GBP_APIS:
     ##  raise ValueError(f"Source {source} is not supported.")

    cashblock_list = await fetch_GBPData(GBP_APIS['CashblockList'])
    return cashblock_list
@mcp.tool()
async def get_account_details(source: str):
    """
    Fetches the Account Balance Information of the given Account number.

    Args:
    source: Name of the Account number.

    Returns:
    Fetches the account balance details of the given account.
    """
   ## if source not in GBP_APIS:
     ##  raise ValueError(f"Source {source} is not supported.")

    account_balance = await fetch_GBPData(GBP_APIS['AccountDetailList'])
    return account_balance

if __name__ == "__main__":
    mcp.run(transport="stdio")