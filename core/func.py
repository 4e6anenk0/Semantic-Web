from xml.dom import minidom
from xml.etree.ElementTree import ElementTree, SubElement
from lxml import html, etree
from core.former import Former
import googletrans as translate
import langid
import re


def create_tag(name: str=None, text: str=None, attributes: dict=None, *, cdata: bool=False):

    doc = minidom.Document()

    if name is None:
            return doc

    tag = doc.createElement(name)
    
    if text is not None:
        if cdata is True:
            tag.appendChild(doc.createCDATASection(text))
        else:
            tag.appendChild(doc.createTextNode(text))
    
    if attributes is not None:
        for k, v in attributes.items():
            tag.setAttribute(k, str(v))
    
    return tag

def formatting(text: str):
    text = ' '.join(text.split())
    text = re.sub(r'(?<=[.])(?=[^\s])', r' ', text)
    return text

    
    """
    Функция, с помощью которой происходит парсинг данных с сайта по класу с помощью библиотеки lxml
    """
def class_parse(class_name: str, content):
    data = []
    for el in content.find_class(class_name):
        if el.text is not None:
            data.append(formatting(str(el.text)))
        else:
            data.append("Не указано")
            
    return data


    """
    Функция, которая из полученных данных с помощью класса  Former генерирует обьекты данных с
    с произвольным колличеством атрибутов.
    """
def combine_data(names: list, *args):
    if len(names) != len(list(args)):
        Exception()
    else:
        form_list = []
        for el in zip(*args):
            form = Former()
            itr = iter(names)
            for sub_el in el:
                form.add_atr(next(itr), sub_el)
            form_list.append(form)
    
    return form_list
    
# laba 2

def translate_text(root: object, where: str, src: str, dest: str):
    for el in root.iter(where):
        if langid.classify(el.text)[0] == src:
            translator = translate.Translator()
            new_value = translator.translate(el.text, dest, src)
            el.text = new_value.text
    return root

def replace_text(root: object, where: str, old: str, new: str):
    for el in root.iter(where):
        if el.text == old:
            el.text = new
    return root

def formatting_text(root: object, where: str, pattern: object, change):
    for el in root.iter(where):
        new_value = pattern.sub(change, el.text)
        el.text = new_value
    return root

def convert(value: float, from_value: str, to_value: str):
    usd_rates = {"UAH": 26.7, "EUR": 0.9, "USD": 1}
    new_value = (usd_rates["USD"] / usd_rates[from_value]) * value * usd_rates[to_value]
    return new_value

def extend(root: object, extend_tag: str, old: str, new: str, sub_el: dict, save_value = False, tag_for_save_value = None):
    for el in root.iter(extend_tag):
        if save_value is False:
            new_element = SubElement(el, new)
            for teg, text in sub_el.items():
                new_sub = SubElement(new_element, teg)
                new_sub.text = text
            old_element = el.find(old)
            el.remove(old_element)
            
        elif save_value is True:
            save = el.find(old).text
            new_element = SubElement(el, new)
            save_element = SubElement(new_element, tag_for_save_value)
            save_element.text = save
            for teg, text in sub_el.items():
                new_sub = SubElement(new_element, teg)
                new_sub.text = text
            old_element = el.find(old)
            el.remove(old_element)
    
    return root


def add_attr(root: object, where: str, generate_key = None, generate_value = None, x = None, y = None, **attrs):
    for el in root.iter(where):
        if generate_key is not None and generate_value is not None:
            el.set(generate_key(x), generate_value(y))
        else:
            for key, value in attrs:
                el.set(key, value)
    return root

def add_local_attr(root: object, where: str):
    for el in root.iter(where):
        el.set("local", langid.classify(el.text)[0])
    return root

# laba 3

def my_xpath(root: object, xpath: str):
    query = etree.XPath(xpath)
    return query(root)