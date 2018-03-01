import random
import json
from time import sleep

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def random_sleep(start=1, end=3):
   sleep(random.uniform(start, end))


# const values
DOMAIN = "https://www.work.ua"
START_URL = "https://www.work.ua/jobs-dnipro/"
PAGE = 460
RESULT = {}
i=0

# main parser
print("--start parse work ua --")
while True:
   payload = {"page": PAGE}
   headers = {'User-Agent': generate_user_agent()}
   response = requests.get(START_URL, params=payload, headers=headers)
   print("-"*50)
   print(response.url)
   random_sleep()
   PAGE += 1
   html_doc = response.text
   soup = BeautifulSoup(html_doc, 'html.parser')
   # div that contains all vacancies on page
   jobs_container_raw = soup.findAll("div", {"class": "col-md-8"})[0]
   # list of page vacancies (should be 14 items)
   jobs_list_raw = jobs_container_raw.findAll("div", {"class": "card-hover"})

   if not jobs_list_raw:
       break

   for card in jobs_list_raw:
       i += 1
       link = card.findAll("h2")[0].find_all('a', href=True)[0]
       job_url="https://www.work.ua" + link["href"]
       print(job_url)
       headers = {'User-Agent': generate_user_agent()}
       response = requests.get(job_url, params=payload, headers=headers)
       html_doc = response.text
       soup = BeautifulSoup(html_doc, 'html.parser')
       jobs_container = soup.findAll("div", {"class": "col-md-8"})[0].findAll("div",{"class": "card"})[1]
       job_title = jobs_container.findAll("h1",{"class": "cut-top"})[0].text
       #salary = jobs_container.findAll("h3",{"class": "wordwrap"})[0].text
       try:
           salary = jobs_container.findAll("h3",{"class": "wordwrap"})[0].text
       except IndexError:
           salary = "not specified"
       main_inf = jobs_container.findAll("dl",{"class": "dl-horizontal"})[0].text
       city= main_inf[main_inf.rfind("Город"):main_inf.find("Вид занятости")]

       print(city)



       # write result to dict as {id: {href: str, text: str}}

       RESULT.update({
           # get vacancy id from url (example /jobs/1232342 -> 1232342)
           i: {"vacancy" : job_title,
               "salary"  : salary,
               "url" : ("https://www.work.ua"+link["href"])
           }
       })
print("https://www.work.ua" + link["href"])
print("--end parse work ua --")

with open('data.json', 'w', encoding='utf-8') as outfile:
   json.dump(RESULT, outfile,ensure_ascii=False)

print("-- saved to file data.json --")