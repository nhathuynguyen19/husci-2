import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.announcement import AnnouncementInput
from typing import List

def crawl() -> List[AnnouncementInput]:
    result = []
    base_url = "https://ums.husc.edu.vn"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser") 
    container_div = (
        soup.find('div', class_='panel-main-content')
            .find('div', class_='row')
            .find('div', class_='col-xs-12')
            .find('div', class_='container-fluid')
    )
    raw_announcements = container_div.find_all('div')
    

    for raw_announcement in raw_announcements:
        a_tag = raw_announcement.select_one("p > a")
        small_tag = raw_announcement.select_one("p > small")
        
        title = a_tag.text.strip()
        content = raw_announcement.select("p")[1].text.strip()
        url = a_tag.get("href").strip()
        date_create = datetime.strptime(small_tag.text.strip("[]"), "%d/%m/%Y %H:%M")
        
        announcement_input = AnnouncementInput(
            title=title,
            content=content,
            url=base_url + url,
            date_create=date_create
        )
        
        result.append(announcement_input)
    
    return result
                    