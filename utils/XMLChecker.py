from lxml import etree
import logging

class XMLChecker:
    def __init__(self, schema_path):
        with open(schema_path) as f:
            schema = etree.XMLSchema(file=f)
        self.parser = etree.XMLParser(schema=schema)

    def check(self, file_path):
        etree.parse(file_path, self.parser)
