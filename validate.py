import xmlschema

# Validate
xsd = xmlschema.XMLSchema("schema.xsd")
result = xsd.is_valid("xml_gen.xml")

print(result)