import requests as rq
from lxml import html, etree
from components import vacancy as apigds
# Importing created librarys:
from core.func import class_parse
from core.func import combine_data

# &pg=2 iterate
def generate_url():
    url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1"
    num = 1
    while True:
        yield url
        num = num + 1
        url = url + "&pg=" + str(num)

g_url = generate_url()
name_and_class = {"name":"ga_listing", "company":"company-profile-name", "salary":"salary", "location":"location", "description":"card-description"}

def get_data(generate_url: object, num_pages: int, name_and_class: dict):
    name_list = []
    data_list = []
    parsing_dict = {}
    for step in range(num_pages):
        url = next(generate_url)
        page = rq.get(url).text
        content = html.fromstring(page)
        
        for name, clazz in name_and_class.items():
            if step == 0:
                el = class_parse(clazz, content)
                parsing_dict.update({name:el})
            else: 
                el = class_parse(clazz, content)
                value = parsing_dict[name]
                value.extend(el)
        
    for name, data in parsing_dict.items():
        name_list.append(name)
        data_list.append(data)
    
    data = combine_data(name_list, *data_list)

    return data
        
data = get_data(g_url, 1, name_and_class)


# Getting content from the site
#url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1"
#page = rq.get(url).text
#content = html.fromstring(page)

# Parsing
#name_list = class_parse("ga_listing", content)
#company_list = class_parse("company-profile-name", content)
#salary_list = class_parse("salary", content)
#location_list = class_parse("location", content)
#description_list = class_parse("card-description", content)

# Combining the data in objects
#names = ["name", "company", "salary", "location", "description"]
#data = combine_data(names, name_list, company_list, salary_list, location_list, description_list)

#Example: Generate data structure
#for el in data:
#    print("%s,%s,%s,%s,%s" % (el.name, el.company, el.salary, el.location, el.description))

# Terminal: Generate clases with GenerateDS
# python generateDS.py -o vacancy.py -s vacancysubs.py schema.xsd

# Building a xml document with GenerateDS
#_____________________________________________________________

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














