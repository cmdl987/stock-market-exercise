import requests
from bs4 import BeautifulSoup
import pandas as pd

# Connect to the url with data.
# It could be useful to list all IBEX35 companies in order to deploy
# a list with all indexes and being able to select one of them.
url = "https://www.infobolsa.es/cotizacion/historico-iberdrola"
my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"}

def get_request(url, headers):
    """
    Get an html parsed data content from the requested url. 

    Args:
        url (str): stock-market url to extract the data. 
        headers (dict): navigator parameters to allow data recolection.

    Returns:
       bs4.BeautifulSoup : html parsed content from the url.
    """
    my_request = requests.get(url, headers=headers)
    df = pd.read_html(my_request.text)
    table_columns = (df[0].columns.values.tolist())
    daily_results = df[1]
    daily_results.columns = table_columns
    #print(daily_results)
    return daily_results


df = get_request(url, my_headers)
csv_file
            
        

