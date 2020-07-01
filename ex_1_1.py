import requests as rq
from lxml import html, etree
from components import vacancy as apigds
import csv
# Importing created librarys:
from core.func import class_parse
from core.func import combine_data
from core.func import generate_url
from core.func import get_data_as_obj
from core.func import get_data_as_dict

url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1"
g_url = generate_url(url, "&pg=")

name_and_class = {
    "name":"ga_listing",
    "company":"company-profile-name",
    "salary":"salary",
    "location":"location",
    "description":"card-description"
}

data = get_data_as_obj(g_url, 1, name_and_class)

with open('vacancies.csv', mode='w') as csv_file:
    fieldnames = ["name", "company", "salary", "location", "description"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for el in data:
        writer.writerow({
        "name":el.name,
        "company":el.company,
        "salary":el.salary,
        "location":el.location,
        "description":el.description
        })


with open("vacancies.csv") as csv_file:
    print(csv_file.read())
