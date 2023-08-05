"""
This module contains the actions used in the Toolbox (lower left section
of the main window.

The Toolbox is bound to a diagram. When a diagram page (tab) is switched,
the actions bound to the toolbuttons should change as well.
"""

from zope import component
from gaphor.UML.event import DiagramItemCreateEvent
from gaphor import UML
from gaphor.diagram import items
from gaphor.core import _, inject, radio_action, build_action_group
from diagramtools import PlacementTool, DefaultTool
from groupingtools import GroupPlacementTool
from gaphas.item import SE

__all__ = [ 'DiagramToolbox', 'TOOLBOX_ACTIONS' ]

TOOLBOX_ACTIONS = (
    ('', (
        ('toolbox-pointer', _('Pointer'), 'gaphor-pointer'),
        ('toolbox-line', _('Line'), 'gaphor-line'),
        ('toolbox-box', _('Box'), 'gaphor-box'),
        ('toolbox-ellipse', _('Ellipse'), 'gaphor-ellipse'),
        ('toolbox-comment', _('Comment'), 'gaphor-comment'),
        ('toolbox-comment-line', _('Comment line'), 'gaphor-comment-line'),
    )), (_('Classes'), (
        ('toolbox-class', _('Class'), 'gaphor-class'),
        ('toolbox-interface', _('Interface'), 'gaphor-interface'),
        ('toolbox-package', _('Package'), 'gaphor-package'),
        ('toolbox-association', _('Association'), 'gaphor-association'),
        ('toolbox-dependency', _('Dependency'), 'gaphor-dependency'),
        ('toolbox-generalization', _('Generalization'), 'gaphor-generalization'),
        ('toolbox-implementation', _('Implementation'), 'gaphor-implementation'),
    )), (_('Components'), (
        ('toolbox-component', _('Component'), 'gaphor-component'),
        ('toolbox-artifact', _('Artifact'), 'gaphor-artifact'),
        ('toolbox-node', _('Node'), 'gaphor-node'),
        ('toolbox-device', _('Device'), 'gaphor-device'),
        ('toolbox-subsystem', _('Subsystem'), 'gaphor-subsystem'),
        ('toolbox-connector', _('Connector'), 'gaphor-connector'),
    )), (_('Actions'), (
        ('toolbox-action', _('Action'), 'gaphor-action'),
        ('toolbox-initial-node', _('Initial node'), 'gaphor-initial-node'),
        ('toolbox-activity-final-node', _('Activity final node'), 'gaphor-activity-final-node'),
        ('toolbox-flow-final-node', _('Flow final node'), 'gaphor-flow-final-node'),
        ('toolbox-decision-node', _('Decision/merge node'), 'gaphor-decision-node'),
        ('toolbox-fork-node', _('Fork/join node'), 'gaphor-fork-node'),
        ('toolbox-object-node', _('Object node'), 'gaphor-object-node'),
        ('toolbox-partition', _('Partition'), 'gaphor-partition'),
        ('toolbox-flow', _('Control/object flow'), 'gaphor-control-flow'),
    )), (_('Interactions'), (
        ('toolbox-lifeline', _('Lifeline'), 'gaphor-lifeline'),
        ('toolbox-message', _('Message'), 'gaphor-message'),
        ('toolbox-interaction', _('Interaction'), 'gaphor-interaction'),
    )), (_('States'), (
        ('toolbox-state', _('State'), 'gaphor-state'),
        ('toolbox-initial-pseudostate', _('Initial Pseudostate'), 'gaphor-initial-pseudostate'),
        ('toolbox-final-state', _('Final State'), 'gaphor-final-state'),
        ('toolbox-history-pseudostate', _('History Pseudostate'), 'gaphor-history-pseudostate'),
        ('toolbox-transition', _('Transition'), 'gaphor-transition'),
    )), (_('Use Cases'), (
        ('toolbox-usecase', _('Use case'), 'gaphor-usecase'),
        ('toolbox-actor', _('Actor'), 'gaphor-actor'),
        ('toolbox-usecase-association', _('Association'), 'gaphor-association'),
        ('toolbox-include', _('Include'), 'gaphor-include'),
        ('toolbox-extend', _('Extend'), 'gaphor-extend'),
    )), (_('Profiles'), (
        ('toolbox-profile', _('Profile'), 'gaphor-profile'),
        ('toolbox-metaclass', _('Metaclass'), 'gaphor-metaclass'),
        ('toolbox-stereotype', _('Stereotype'), 'gaphor-stereotype'),
        ('toolbox-extension', _('Extension'), 'gaphor-extension'),
    )),
    )


def itemiter(toolbox_actions):
    """
    Iterate toolbox items, irregardless section headers
    """
    for name, section in toolbox_actions:
        for e in section:
            yield e


class DiagramToolbox(object):
    """
    Composite class for DiagramTab (diagramtab.py).
    """

    element_factory = inject('element_factory')
    properties = inject('properties')


    def __init__(self, diagram, view):
        self.view = view
        self.diagram = diagram
        self.action_group = build_action_group(self)

    namespace = property(lambda s: s.diagram.namespace)


    def get_tool(self, tool_name):
        """
        Return a tool associated with an id (action name).
        """
        return getattr(self, tool_name.replace('-', '_'))()


    @radio_action(names=zip(*list(itemiter(TOOLBOX_ACTIONS)))[0],
                  labels=zip(*list(itemiter(TOOLBOX_ACTIONS)))[1],
                  stock_ids=zip(*list(itemiter(TOOLBOX_ACTIONS)))[2])
    def _set_toolbox_action(self, id):
        """
        Activate a tool based on its index in the TOOLBOX_ACTIONS list.
        """
        tool_name = list(itemiter(TOOLBOX_ACTIONS))[id][0]
        self.view.tool = self.get_tool(tool_name)

    def _item_factory(self, item_class, subject_class=None, extra_func=None):
        """
        ``extra_func`` may be a function accepting the newly created item.
        """
        def factory_method(parent=None):
            if subject_class:
                subject = self.element_factory.create(subject_class)
            else:
                subject = None
            item = self.diagram.create(item_class, subject=subject,
                    parent=parent)
            if extra_func: extra_func(item)
            return item
        factory_method.item_class = item_class
        return factory_method

    def _namespace_item_factory(self, item_class, subject_class, stereotype=None, name=None):
        """
        Returns a factory method for Namespace classes.
        To be used by the PlacementTool.
        """
        def factory_method(parent=None):
            subject = self.element_factory.create(subject_class)
            item = self.diagram.create(item_class, subject=subject, parent=parent)
            subject.package = self.namespace
            if name is not None:
                subject.name = name
            elif stereotype:
                subject.name = 'New%s' % stereotype.capitalize()
            else:
                subject.name = 'New%s' % subject_class.__name__
            return item
        factory_method.item_class = item_class
        return factory_method

    def _after_handler(self, new_item):
        if self.properties('reset-tool-after-create', False):
            self.action_group.get_action('toolbox-pointer').activate()
        component.handle(DiagramItemCreateEvent(new_item))


    ##
    ## Toolbox actions
    ##

    def toolbox_pointer(self):
        if self.view:
            return DefaultTool()

    def toolbox_line(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.Line),
                after_handler=self._after_handler)

    def toolbox_box(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.Box),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_ellipse(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.Ellipse),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_comment(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.CommentItem, UML.Comment),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_comment_line(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.CommentLineItem),
                after_handler=self._after_handler)

    # Classes:

    def toolbox_class(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ClassItem,
                                                          UML.Class),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_interface(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.InterfaceItem,
                                                          UML.Interface),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_package(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.PackageItem,
                                                          UML.Package),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_association(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.AssociationItem),
                after_handler=self._after_handler)

    def toolbox_dependency(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.DependencyItem),
                after_handler=self._after_handler)

    def toolbox_generalization(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.GeneralizationItem),
                after_handler=self._after_handler)

    def toolbox_implementation(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.ImplementationItem),
                after_handler=self._after_handler)

    # Components:

    def toolbox_component(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ComponentItem,
                    UML.Component),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_artifact(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ArtifactItem,
                                                          UML.Artifact),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.NodeItem,
                    UML.Node),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_device(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.NodeItem,
                                                          UML.Device),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_subsystem(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.SubsystemItem,
                    UML.Component, 'subsystem'),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_connector(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.ConnectorItem),
                after_handler=self._after_handler)

    # Actions:

    def toolbox_action(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ActionItem,
                                                          UML.Action),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_initial_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.InitialNodeItem,
                                                UML.InitialNode),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_activity_final_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.ActivityFinalNodeItem,
                                                UML.ActivityFinalNode),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_flow_final_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.FlowFinalNodeItem,
                                                UML.FlowFinalNode),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_decision_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.DecisionNodeItem,
                                                UML.DecisionNode),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_fork_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.ForkNodeItem,
                                                UML.JoinNode),
                handle_index=1,
                after_handler=self._after_handler)

    def toolbox_object_node(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ObjectNodeItem,
                                                          UML.ObjectNode),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_partition(self):
        # note no subject, which is created by grouping adapter
        return GroupPlacementTool(self.view,
                item_factory=self._item_factory(items.PartitionItem),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_flow(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.FlowItem),
                after_handler=self._after_handler)

    # Interactions:
    def toolbox_interaction(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.InteractionItem,
                    UML.Interaction),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_lifeline(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.LifelineItem,
                    UML.Lifeline),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_message(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.MessageItem),
                after_handler=self._after_handler)

    # States:
    def toolbox_state(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.StateItem,
                    UML.State),
                handle_index=SE,
                after_handler=self._after_handler)

    def _toolbox_pseudostate(self, kind):
        def set_state(item):
            item.subject.kind = kind
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.InitialPseudostateItem,
                                                UML.Pseudostate, set_state),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_initial_pseudostate(self):
        def set_state(item):
            item.subject.kind = 'initial'
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.InitialPseudostateItem,
                                                UML.Pseudostate, set_state),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_history_pseudostate(self):
        def set_state(item):
            item.subject.kind = 'shallowHistory'
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.HistoryPseudostateItem,
                                                UML.Pseudostate, set_state),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_final_state(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.FinalStateItem,
                                                UML.FinalState),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_transition(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.TransitionItem),
                after_handler=self._after_handler)

    # Use cases:

    def toolbox_usecase(self):
        return GroupPlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.UseCaseItem,
                                                          UML.UseCase),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_actor(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ActorItem,
                                                          UML.Actor),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_usecase_association(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.AssociationItem),
                after_handler=self._after_handler)

    def toolbox_include(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.IncludeItem),
                after_handler=self._after_handler)

    def toolbox_extend(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.ExtendItem),
                after_handler=self._after_handler)

    # Profiles:

    def toolbox_profile(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.PackageItem,
                                                          UML.Profile),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_metaclass(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.MetaclassItem,
                    UML.Class, 'metaclass', name='Class'),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_stereotype(self):
        return PlacementTool(self.view,
                item_factory=self._namespace_item_factory(items.ClassItem,
                                                          UML.Stereotype),
                handle_index=SE,
                after_handler=self._after_handler)

    def toolbox_extension(self):
        return PlacementTool(self.view,
                item_factory=self._item_factory(items.ExtensionItem),
                after_handler=self._after_handler)


# vim:sw=4:et:ai
