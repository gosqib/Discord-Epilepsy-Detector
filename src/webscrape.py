from bs4 import BeautifulSoup#type:ignore
from urllib.request import urlopen
import requests#type:ignore

from keyvars.mytypes import FileName

def get_tenor(link: str) -> FileName:
    """tenor is the name of discord text gifs
    this function webscrapes that gif since it's not possible to extract is from the 
    discord message component. after the source has been extracted from the html, this
    function downloads it with another webscrape since it's not possible to download with
    the specific beautifulsoup object
    """
    html = urlopen(link).read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    gif = soup.find_all('div', class_='Gif')[0]

    gif = soup.find_all('div', class_='Gif')[0]
    download_location = gif.next['src']

    file_name = (
        link
            .replace('/', '')
            .replace(':', '')
    )
    with open(file_name, 'wb') as f:
        f.write(requests.get(download_location).content)
    
    return file_name # this will be passed into a method that will require the file name in 
                     # the current directory
