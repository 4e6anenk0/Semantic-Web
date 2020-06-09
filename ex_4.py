import rdflib as rdf

from core.former import Former
from lxml import etree
import pyshacl

tree = etree.parse("xml_gen_update.xml")
root = tree.getroot()

list_vacancies_obj = []
for el in root.iter("vacancy"):
    id_vacancy = el.attrib["ID"]
    name = el.find("name").text
    company = el.find("company").text
    location = el.find("location").text
    description = el.find("description").text
    description_attr = el.find("description").attrib["local"]
    vacancy = Former()
    vacancy.add_atr("id", id_vacancy)
    vacancy.add_atr("name", name)
    vacancy.add_atr("company", company)
    vacancy.add_atr("location", location)
    vacancy.add_atr("description", description)
    vacancy.add_atr("description_attr", description_attr)
    salary = Former()
    salary_list = el.find("salary_list")
    uah = salary_list.find("UAH").text
    usd = salary_list.find("USD").text
    eur = salary_list.find("EUR").text
    uah_attr = salary_list.find("UAH").attrib["curency"]
    usd_attr = salary_list.find("USD").attrib["curency"]
    eur_attr = salary_list.find("EUR").attrib["curency"]
    salary.add_atr("uah", uah)
    salary.add_atr("usd", usd)
    salary.add_atr("eur", eur)
    salary.add_atr("uah_attr", uah_attr)
    salary.add_atr("usd_attr", usd_attr)
    salary.add_atr("eur_attr", eur_attr)
    vacancy.add_atr("salary_list", salary)
    list_vacancies_obj.append(vacancy)

# for el in list_vacancies_obj:
#    print("Vacancy ID: {}. Name: {}, company: {}, location: {}. Description: {} Salary: {},{}; {},{}; {},{}."
#    .format(el.id, el.name, el.company, el.location, el.description,
#    el.salary_list.uah, el.salary_list.uah_attr, el.salary_list.usd,
#    el.salary_list.usd_attr, el.salary_list.eur, el.salary_list.eur_attr))


g = rdf.Graph()


root_resource = rdf.URIRef("https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1")

vacancies = rdf.BNode()

for el in list_vacancies_obj:
    vacancy = rdf.URIRef(el.id)
    name = rdf.Literal(el.name)
    g.add((vacancy, rdf.DC.title, name))
    company = rdf.Literal(el.company)
    g.add((vacancy, rdf.DC.creator, company))
    location = rdf.Literal(el.location)
    g.add((vacancy, rdf.DC.title, location))
    description = rdf.BNode()
    description_text = rdf.Literal(el.description)
    description_label = rdf.Literal(el.description_attr)
    g.add((description, rdf.DC.description, description_text))
    g.add((description, rdf.DC.language, description_label))
    g.add((vacancy, rdf.DC.type, description))
    salary = rdf.BNode()
    uah = rdf.Literal(el.salary_list.uah)
    uah_label = rdf.Literal(el.salary_list.uah_attr)
    g.add((salary, rdf.RDF.value, uah))
    g.add((salary, rdf.DC.title, uah_label))
    usd = rdf.Literal(el.salary_list.usd)
    usd_label = rdf.Literal(el.salary_list.usd_attr)
    g.add((salary, rdf.RDF.value, usd))
    g.add((salary, rdf.DC.title, usd_label))
    eur = rdf.Literal(el.salary_list.eur)
    eur_label = rdf.Literal(el.salary_list.eur_attr)
    g.add((salary, rdf.RDF.value, eur))
    g.add((salary, rdf.DC.title, eur_label))
    g.add((vacancy, rdf.DC.type, salary))
    g.add((vacancies, rdf.RDF.li, vacancy))
g.add((root_resource, rdf.RDF.Bag, vacancies))



f = open("rdf_gen.rdf", "wb")
f.write(g.serialize(encoding="utf-8"))
f.close

print(pyshacl.validate(g)[2])

eng = 0
other = 0
for el in list_vacancies_obj:
    
    if el.description_attr == "en":
        eng = eng + 1
    else:
        other = other + 1

procent = 100 / (eng + other)
eng = eng * procent
other = other * procent

print("Количество страниц с английским описанием: {}%, а с другим языком: {}%".format(eng, other))

sum_triplet = 0
for s, p, o in g:
    sum_triplet = sum_triplet + 1

print("Было сгенерированно триплетов: {}".format(sum_triplet))

for el in list_vacancies_obj:
    if el.description_attr == "en":
        print(el.description)
    
    
