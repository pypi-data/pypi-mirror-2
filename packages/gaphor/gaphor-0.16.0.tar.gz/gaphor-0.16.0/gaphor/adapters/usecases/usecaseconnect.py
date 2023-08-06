"""
Use cases related connection adapters.
"""

from zope import component
from gaphor import UML
from gaphor.diagram import items
from gaphor.adapters.connectors import RelationshipConnect


class IncludeConnect(RelationshipConnect):
    """
    Connect use cases with an include item relationship.
    """
    component.adapts(items.UseCaseItem, items.IncludeItem)

    CAN_RECONNECT = True

    def allow(self, handle, port):
        line = self.line
        element = self.element

        if not (element.subject and isinstance(element.subject, UML.UseCase)):
            return None

        return super(IncludeConnect, self).allow(handle, port)


    def reconnect(self, handle, port):
        self.reconnect_relationship(handle, 'addition', 'includingCase')


    def connect_subject(self, handle):
        relation = self.relationship_or_new(UML.Include,
                    ('addition', None),
                    ('includingCase', 'include'))
        self.line.subject = relation

component.provideAdapter(IncludeConnect)


class ExtendConnect(RelationshipConnect):
    """
    Connect use cases with an extend item relationship.
    """
    component.adapts(items.UseCaseItem, items.ExtendItem)

    CAN_RECONNECT = True

    def allow(self, handle, port):
        line = self.line
        element = self.element
        
        if not (element.subject and isinstance(element.subject, UML.UseCase)):
            return None

        return super(ExtendConnect, self).allow(handle, port)

    def reconnect(self, handle, port):
        self.reconnect_relationship(handle, 'extendedCase', 'extension')

    def connect_subject(self, handle):
        relation = self.relationship_or_new(UML.Extend,
                    ('extendedCase', None),
                    ('extension', 'extend'))
        self.line.subject = relation

component.provideAdapter(ExtendConnect)

# vim:sw=4:et:ai

