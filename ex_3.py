from lxml import etree
from core.func import my_xpath
import re

def parse_xml(path):
    with open(path, 'r') as file:
        xml_text = file.read()
    return etree.XML(xml_text)

root = parse_xml('xml_gen_update.xml')


count_elements = int(my_xpath(root, 'count(//vacancies/vacancy)'))
print("Количество вакансий в корневом узле: {}".format(count_elements))

attributes_info = my_xpath(root, '//vacancies/vacancy/@ID')
print("Вывод значений атрибутов по всем вакансиям: {}".format(attributes_info))

first_element_attribute_info = my_xpath(root, "//vacancies/vacancy[{}]/{}/text()".format(1, "company"))
print("Получение значения по тегу: {}".format(first_element_attribute_info[0]))

contain_several_words = my_xpath(root, "count(//vacancies/vacancy/company[contains(text(),' ')]) + 1")
print("Количество названий компаний состоящих более чем из 2 слова: {}".format(contain_several_words))

complicated_element = my_xpath(root, "(//vacancies/vacancy[{}]/descendant::*)[{}]/text()".format(1, 1))
complicated_element2 = my_xpath(root, "(//vacancies/vacancy[{}]/descendant::*)[{}]/text()".format(1, 2))
complicated_element3 = my_xpath(root, "(//vacancies/vacancy[{}]/descendant::*)[{}]/text()".format(1, 3))
complicated_element.append(complicated_element2[0])
complicated_element.append(complicated_element3[0])

complicated_element = [line.rstrip() for line in complicated_element]
print("Вывод составного значения. Вакансия: {}, требуется: {}, Расположение: {}".format(*complicated_element))

xpath = '//vacancies/vacancy/salary_list/UAH[number(text()) >= {} and number(text()) <= {}]/text()'.format(50000, 55000)
tag_name_with_name_and = my_xpath(root, xpath)
print("Найдено зарплаты, удовлетворяющие диапазону: {}".format(tag_name_with_name_and))


def every_fifth_element(root):
    qwery = my_xpath(root, '//vacancies/vacancy[position() mod 5 = 0]/@ID')
    element_number = list(map(lambda x: str(int(x) + 1), qwery))
    element_info_each_fifth = my_xpath(root, '//vacancies/vacancy[position() mod 5 = 0]/name/text()')
    element_rating = my_xpath(root, '//vacancies/vacancy[position() mod 5 = 0]/company/text()')
    element_rating = list(map(lambda x: str(x), element_rating))
    return element_number, element_info_each_fifth, element_rating


every_fifth_element_list = []
for el in zip(*every_fifth_element(root)):
    el = list(el)
    every_fifth_element_list.append(el)

for el in every_fifth_element_list:
    el = [line.rstrip() for line in el]
    print("Вывод каждой пятой: {}".format(el)) 