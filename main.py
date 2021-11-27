import requests
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent
import time

funcs = "
get_random_ua() 
get_response()
get_list()
main()
log()
"




def get_random_ua():
    return UserAgent().random


def log(text, type):
    if type.lower == "w":
        print(f"[WARNING]: {text}")
    elif type.lower == "i":
        print(f"[INFO]: {text}")


def get_response(query):
    url = f"https://jp.b-ok.as/s/{query}/?languages%5B0%5D=english&extensions%5B0%5D=pdf"
    random_ua = get_random_ua()
    headers = {"User-Agent":random_ua}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        log("bad response", "w")
        time.sleep(5)
        get_response(query)


def get_book_info_json(response):
    soup = bs4(response, "html.parser")
    results = soup.select("#searchResultBox > div > div > table")
    list_json = []

    for book in results:
        name = book.find("h3").find("a").text
        link = book.find("h3").find("a").get("href")
        
        try:
            pub = book.select_one("tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div:nth-child(2)").text
        except Exception as e:
            print(e)
            pub = ""
        
        try:
            authors = [authour.text for authour in book.select("tbody > tr:nth-child(1) > td > div.authors > a")]
        except:
            authors = []
        
        try:
            year = book.select_one("tbody > tr:nth-child(2) > td > div.bookDetailsBox > div.bookProperty.property_year > div.property_value").text
        except:
            year = ""
        
        try:
            rating = book.select_one("tbody > tr:nth-child(2) > td > div.bookDetailsBox > div.bookProperty.property_rating > div").text.replace(" ","").replace("\n","")
        except:
            rating = ""
        
        entry_json = {
            "name":name,
            "url":link, 
            "publisher":pub,
            "authors":authors,
            "year":year,
            "rating":rating,
            }
        
        list_json.append(book_entry_json)


    return list_json





def main():
    print("This is a library! Not a script!")
    exit()



if __name__=="__main__":
    main()
