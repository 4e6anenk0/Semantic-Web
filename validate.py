import xmlschema

# Validate
xsd = xmlschema.XMLSchema("components/schema.xsd")
result = xsd.is_valid("xml_gen.xml")

print(result)

