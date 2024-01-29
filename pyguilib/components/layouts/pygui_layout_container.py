from pyguilib.components.layouts.pygui_layout_style import PyGuiLayoutStyle
from pyguilib.components.pygui_instance import PyGuiInstance


class PyGuiLayoutContainer(object):
    def __init__(self, **kwargs) -> "PyGuiLayoutContainer":
        super(PyGuiLayoutContainer, self).__init__()

        self._layout_instance_child_added_connection = None
        self._layout_instance_child_removed_connection = None

        self._applied_layout = None

    @property
    def applied_layout(self) -> PyGuiLayoutStyle:
        try:
            return self._applied_layout
        except AttributeError:
            return None

    def apply_layout(self, layout: PyGuiLayoutStyle):
        layout._instance = self

        if self.applied_layout is not None:
            raise Exception("Only one layout can be applied to a PyGuiInstance at a time")

        self._applied_layout = layout

        @PyGuiLayoutStyle._update_layout_order
        def _on_layout_instance_child_added(self, child: PyGuiInstance):
            layout._sorted_instance_childs.append(child)
            layout._sort_instance_childs()
            layout._on_layout_instance_child_added(child)

        @PyGuiLayoutStyle._update_layout_order
        def _on_layout_instance_child_removed(self, child: PyGuiInstance):
            layout._sorted_instance_childs.remove(child)
            layout._sort_instance_childs()
            layout._on_layout_instance_child_removed(layout, child)

        self._layout_instance_child_added_connection = self.child_added.connect(lambda child: _on_layout_instance_child_added(layout, child))
        self._layout_instance_child_removed_connection = self.child_removed.connect(lambda child: _on_layout_instance_child_removed(layout, child))

        for child_name in self._childrens:
            layout._sorted_instance_childs.append(self._childrens[child_name])
            layout._on_layout_instance_child_added(self._childrens[child_name])

        layout._sort_instance_childs()
        layout._on_layout_applied()

        @PyGuiLayoutStyle._update_layout_order
        def initialize(_):
            layout._sort_instance_childs()

        initialize(layout)
