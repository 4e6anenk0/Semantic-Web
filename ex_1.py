import requests as rq
from lxml import html, etree
import vacancy as apigds 
# Importing created librarys:
from core.func import class_parse
from core.func import combine_data
from core.func import create_tag


# Getting content from the site
url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1"
page = rq.get(url).text
content = html.fromstring(page)

# Parsing
name_list = class_parse("ga_listing", content)
company_list = class_parse("company-profile-name", content)
salary_list = class_parse("salary", content)
location_list = class_parse("location", content)
description_list = class_parse("card-description", content)

# Combining the data in objects
names = ["name", "company", "salary", "location", "description"]
data = combine_data(names, name_list, company_list, salary_list, location_list, description_list)

# Example: Generate data structure
#for el in data:
#    print("%s,%s,%s,%s,%s" % (el.name, el.company, el.salary, el.location, el.description))

# Terminal: Generate clases with GenerateDS
# python generateDS.py -o vacancy.py -s vacancysubs.py schema.xsd

# Building a xml document with GenerateDS
vacancies_obj = apigds.vacancies()

f = open("xml_gen.xml", "tw", encoding="utf-8")

for count, el in enumerate(data):
    vacancy_obj = apigds.vacancyType(name=el.name, company=el.company, salary=el.salary, location=el.location, description=el.description)
    vacancies_obj.add_vacancy(vacancy_obj)

vacancies_obj.export(f, 0)

f.close()

#exemple: parsing with xpath
#name = content.xpath('//a[@class = "ga_listing"]/text()')
#company = content.xpath('//a[@class = "company-profile-name"]/text()')
#salary = content.xpath('//span[@class = "salary"]/text()')














