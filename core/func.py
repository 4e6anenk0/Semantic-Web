from xml.dom import minidom
from lxml import html
from core.former import Former


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

    
    """
    Функция, с помощью которой происходит парсинг данных с сайта по класу с помощью библиотеки lxml
    """
def class_parse(class_name: str, content):
    data = []
    for el in content.find_class(class_name):
        if el.text is not None:
            data.append(str(el.text))
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
    



