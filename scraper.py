from bs4 import BeautifulSoup
from scheduler import Scheduler
import requests
import datetime
import secret
import time


USER = secret.USER
API = secret.API

def findEventLinks(soup: BeautifulSoup, base: str, daysFromNow: int):
    startInt, endInt = 0, 0
    links = []
    today = datetime.datetime.now().date()
    
    for span in soup.find_all("span", attrs = {"class": "sr-only"}):
        if span.get_text() == "Dato":
            eventDate = span.find_next_sibling("span")
            eventDate = eventDate.get_text().split(" ")[1]
            eventDate = eventDate.split(".")
            eventDate = datetime.date(today.year, int(eventDate[1]), int(eventDate[0]))
            
            if eventDate < today:
                startInt += 1
            
            if (eventDate - today).days < daysFromNow:
                endInt += 1
    
    for link in soup.find_all("a", href=True):
        href = link.get("href")
        
        if href and href.startswith(base):
            link = f"https://ifinavet.no{href}"
            links.append(f"https://ifinavet.no{href}")
            
    return links[startInt:endInt]

def getAvailableRegistrations(eventURLs: str):
    prefix = 'https://ifinavet.no/arrangementer/2023/host/'
    regDict = dict()
    
    for event in eventURLs:
        r = requests.get(event)
        soup = BeautifulSoup(r.content, "html.parser")
        
        srSpans = soup.find_all("span", attrs = {"class": "sr-only"})
        firstSpan = srSpans[3]
        
        availablePlaces = firstSpan.find_next_sibling("span").get_text().split(" ")
        eventName = event.replace(prefix, "").rstrip("/")
        
        regDict[eventName] = int(availablePlaces[0])
    
    return regDict
        
def sendNotification(message: str):
    requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": secret.API,
        "user": secret.USER,
        "message": message
    })

def formatMessage(regDict: dict):
    for value in regDict:
        if regDict[value] > 0:
            message = f"{regDict[value]} plass(er) på {value}"
            print(message)
            sendNotification(message)
    
def main():
    URL = "https://ifinavet.no/arrangementer/2023/host/"
    baseURL = "/arrangementer/2023/host/"
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    
    eventLinks = findEventLinks(soup, baseURL, 15)
    regDict = getAvailableRegistrations(eventLinks)

    formatMessage(regDict)
    
if __name__ == '__main__':
    schedule = Scheduler()
    schedule.minutely(datetime.time(minute = 5), main)
    
    while True:
        schedule.exec_jobs()
        time.sleep(1)