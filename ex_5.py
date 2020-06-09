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

g = rdf.Graph()

# Classes forming
vacancies_class = rdf.BNode()
vacancy_class = rdf.BNode()
company_class = rdf.BNode()
location_class = rdf.BNode()
salary_class = rdf.BNode()

g.add((vacancies_class, rdf.RDF.type, rdf.RDFS.Class))
g.add((vacancies_class, rdf.RDFS.comment, rdf.Literal('Describes the list of vacancies')))

g.add((vacancy_class, rdf.RDFS.subClassOf, vacancies_class))
g.add((vacancy_class, rdf.RDFS.comment, rdf.Literal('Describes vacancy like the object')))

g.add((company_class, rdf.RDFS.subClassOf, vacancy_class))
g.add((company_class, rdf.RDFS.comment, rdf.Literal('Describes company')))

g.add((location_class, rdf.RDFS.subClassOf, vacancy_class))
g.add((location_class, rdf.RDFS.comment, rdf.Literal('Describes location')))

g.add((salary_class, rdf.RDFS.subClassOf, vacancy_class))
g.add((salary_class, rdf.RDFS.comment, rdf.Literal('Describes salary')))

# Properties forming
name_prop = rdf.BNode()
company_prop = rdf.BNode()
salary_value_prop = rdf.BNode()
salary_label_prop = rdf.BNode()
location_name_prop = rdf.BNode()


########
g.add((name_prop, rdf.RDFS.domain, vacancy_class))
g.add((name_prop, rdf.RDFS.comment, rdf.Literal('Describes the name of vacancy')))
g.add((name_prop, rdf.RDFS.range, rdf.RDFS.Literal))

g.add((company_prop, rdf.RDFS.domain, vacancy_class))
g.add((company_prop, rdf.RDFS.comment, rdf.Literal('The name of company')))
g.add((company_prop, rdf.RDFS.range, rdf.RDFS.Literal))

g.add((salary_value_prop, rdf.RDFS.domain, salary_class))
g.add((salary_value_prop, rdf.RDFS.comment, rdf.Literal('Salary value')))
g.add((salary_value_prop, rdf.RDFS.range, rdf.RDFS.Literal))

g.add((salary_label_prop, rdf.RDFS.domain, salary_class))
g.add((salary_label_prop, rdf.RDFS.comment, rdf.Literal('Salary label')))
g.add((salary_label_prop, rdf.RDFS.range, rdf.RDFS.Literal))

g.add((location_name_prop, rdf.RDFS.domain, location_class))
g.add((location_name_prop, rdf.RDFS.comment, rdf.Literal('Name of location')))
g.add((location_name_prop, rdf.RDFS.range, rdf.RDFS.Literal))


root_resource = rdf.URIRef("https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=0&parentId=1")

g.add((root_resource, rdf.RDF.type, vacancies_class))

vacancies = rdf.BNode()
for el in list_vacancies_obj:
    vacancy = rdf.URIRef(el.id)
    g.add((vacancy, rdf.RDF.type, vacancy_class))

    name = rdf.BNode()
    name_value = rdf.Literal(el.name)
    g.add((vacancy, rdf.DC.title, name))
    g.add((name, rdf.RDF.value, name_value))
    g.add((name, rdf.RDF.type, name_prop))

    company = rdf.BNode()
    company_value = rdf.Literal(el.company)
    g.add((vacancy, rdf.DC.creator, company))
    g.add((company, rdf.RDF.value, company_value))
    g.add((company, rdf.RDF.type, company_prop))

    salary = rdf.BNode()
    salary_value = rdf.BNode()
    salary_value_value = rdf.Literal(el.salary_list.uah)
    g.add((salary, rdf.RDF.value, salary_value))
    g.add((salary_value, rdf.RDF.value, salary_value_value))
    g.add((salary_value, rdf.RDF.type, salary_value_prop))
    
    salary_label = rdf.BNode()
    salary_label_value = rdf.Literal(el.salary_list.uah_attr)
    g.add((salary, rdf.DC.type, salary_label))
    g.add((salary_label, rdf.RDF.value, salary_label_value))
    g.add((salary_label, rdf.RDF.type, salary_label_prop))
    g.add((vacancy, rdf.RDF.value, salary))

    description = rdf.BNode()
    g.add((vacancy, rdf.DC.description, description))
    description_value = rdf.Literal(el.description)
    description_label = rdf.Literal(el.description_attr)
    g.add((description, rdf.RDF.value, description_value))
    g.add((description, rdf.DC.title, description_label))

    location = rdf.BNode()
    location_value = rdf.Literal(el.location)
    g.add((vacancy, rdf.DC.title, location))
    g.add((location, rdf.RDF.value, location_value))
    g.add((location, rdf.RDF.type, location_name_prop))


g.add((root_resource, rdf.RDF.Bag, vacancies))


f = open('rdf_gen_2.rdt', 'wb') 
f.write(g.serialize(encoding="utf-8"))
f.close()

print(pyshacl.validate(g)[2])

for s, p, o in g:
    print(s, p, o)



