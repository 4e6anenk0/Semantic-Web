from rdflib import Graph


g = Graph()
g.parse('rdf_gen_2.rdf')

qres = g.query(
    '''SELECT (COUNT(*) as ?pCount)
        WHERE
        {
          ?s ?p ?o .
        }
        '''
)

for el in qres:
    print("Количество триплетов: {}".format(el[0]))

qres1 = g.query(
    '''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?o
        WHERE
        {
          ?vacancy dc:title ?name .
          ?name rdf:value ?o .
        }
    LIMIT 1'''
)


for row in qres1:
    print(f'Название вакансии, выборка из 1 елемента: {row[0]}')
print('\n\t')

qres2 = g.query(
    '''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?salary_value_value
        WHERE
        {
          ?salary rdf:value ?salary_value .
          ?salary_value rdf:value ?salary_value_value .
        }
        '''
)


for row in qres2:
    print(f'Зарплата": {row[0]}')
print('\n\t')


qres3 = g.query(
    '''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?name
        WHERE
        {
          ?s dc:title ?name .
        }
        '''
)

for row in qres3:
    print(f'Обьект с помощью предиката dc:title: {row[0]}')
print('\n\t')

qres4 = g.query(
    '''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?comment
        WHERE
        {
          ?vacancy_class dc:title ?o .
          ?sub_class rdfs:subClassOf ?class .
          ?sub_class rdfs:comment ?comment .
        }
        '''
)

for row in qres4:
    print(f'Название подкласса класса "вакансия": {row[0]}')
print('\n\t')

qres5 = g.query(
    '''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?p (COUNT(?p) as ?pCount)
        WHERE
        {
          ?s ?p ?o .
        }
    GROUP BY ?p
    '''
)

for row in qres5:
    print(f'Количество троек с предикатом "{row[0]}": {row[1]}')
print('\n\t')

qres6 = g.query(
'''PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT (COUNT(?comment) as ?pCount)
        WHERE
        {
          ?vacancy_class dc:title ?o .
          ?sub_class rdfs:subClassOf ?class .
          ?sub_class rdfs:comment ?comment .
        }
    '''
)

for row in qres6:
    print(f'Количество описаний подклассов «Вакансия»: {row[0]}')
print('\n\t')