import xml.etree.ElementTree as et
import re
from core.func import translate_text
from core.func import replace_text
from core.func import formatting_text
from core.func import extend
from core.func import add_attr
from core.func import add_local_attr
from core.func import convert
import xml.dom.minidom as md
import langid


tree = et.parse("xml_gen.xml")
root = tree.getroot()

# step 1
mod_root = translate_text(root, "description", "ru", "uk")

# step 2
mod_root = replace_text(mod_root, "salary", "Не указано", "0")

# step 3
pattern = re.compile(" грн")
mod_root = formatting_text(mod_root, "salary", pattern, "")

# Delete \xa0
pattern = re.compile("\xa0")
mod_root = formatting_text(mod_root, "salary", pattern, "")

pattern = re.compile(" ")
mod_root = formatting_text(mod_root, "salary", pattern, "")


# step 4

#value = convert(2000, "UAH", "USD")
#print(value)

dict_el = {"USD" : "USD", "EUR" : "EUR"}
mod_root = extend(mod_root, "vacancy", "salary", "salary_list", dict_el, True, "UAH")

#конвертация валют
for el in mod_root.iter("salary_list"):
    salary = 0
    for sub_el in el:
        if sub_el.tag == "UAH":
           salary = sub_el.text
        elif sub_el.tag != "UAH":
            sub_el.text = str(int(convert(float(salary), "UAH", sub_el.tag)))

# step 5 

mod_root = add_local_attr(mod_root, "description")

# step 6 

def gener_y():
    result = 0
    while True:
        yield str(result)
        result = result + 1

generator = gener_y()

mod_root = add_attr(mod_root, "vacancy", lambda x: x, next, "ID", generator)

# step 7

mod_root = add_attr(mod_root, "UAH", lambda x: x, lambda y: y, "curency", "uah")
mod_root = add_attr(mod_root, "USD", lambda x: x, lambda y: y, "curency", "usd")
mod_root = add_attr(mod_root, "EUR", lambda x: x, lambda y: y, "curency", "eur")

mod_root = replace_text(mod_root, "UAH", "0", "Не указано")
mod_root = replace_text(mod_root, "USD", "0", "Не указано")
mod_root = replace_text(mod_root, "EUR", "0", "Не указано")
       
# Write 
xmlstr = md.parseString(et.tostring(mod_root)).toprettyxml()

f = open("xml_gen_update.xml", "wb")

f.write(xmlstr.encode("utf-8"))

f.close()

