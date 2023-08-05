from zope.interface import implements

from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.subtypes.file import SchemaExtender as FileSchemaExtender

class ExtensionTextField(ExtensionField, TextField):
    """ derivative of textfield for extending schemas """

extended_fields = FileSchemaExtender.fields[:]
extended_fields.append(
        ExtensionTextField('textFromOcr',
            required = False,
            searchable = True,
            default = '',
            widget = TextAreaWidget(
                label="Text from OCR",
                description="Text from PDF documents using OCR",
                visible = {"edit": "invisible", "view": "invisible"},
            ))
)

class SchemaExtender(object):
    implements(ISchemaExtender)

    fields = extended_fields

    def __init__(self, context):
        self.context = context


    def getFields(self):
        return self.fields