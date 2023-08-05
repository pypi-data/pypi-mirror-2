"""
Formatting of UML model elements into text tests.
"""

import unittest

from gaphor.application import Application
from gaphor.UML.elementfactory import ElementFactory
from gaphor.UML.umlfmt import format
import gaphor.UML.uml2 as UML

factory = ElementFactory()

class AttributeTestCase(unittest.TestCase):

    def setUp(self):
        factory.init(Application)
        factory.flush()


    def tearDown(self):
        factory.shutdown()


    def test_simple_format(self):
        """Test simple attribute formatting
        """
        a = factory.create(UML.Property)
        a.name = 'myattr'
        self.assertEquals('+ myattr', format(a))

        a.typeValue = factory.create(UML.LiteralSpecification)
        a.typeValue.value = 'int'
        self.assertEquals('+ myattr: int', format(a))

