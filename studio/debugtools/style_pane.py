from hoverset.ui.widgets import Label

from studio.ui.widgets import Pane
from studio.feature.stylepane import StylePaneFramework, StyleGroup
from studio.debugtools.common import get_resolved_properties, get_base_class
from studio.debugtools import layouts
from studio.lib.properties import combine_properties


def get_combined_properties(widgets):
    """
    Return a dict of properties that are common to all widgets in the list.
    """
    if not widgets:
        return {}

    # get all the properties for each widget
    properties = [widget._dbg_properties for widget in widgets]

    return combine_properties(properties)


class AttributeGroup(StyleGroup):

    def __init__(self, master, pane, **cnf):
        super().__init__(master, pane, **cnf)
        self.label = "Attributes"
        self.bases = []

    def get_definition(self):
        for widget in self.widgets:
            if not hasattr(widget, '_dbg_properties'):
                setattr(widget, '_dbg_properties', get_resolved_properties(widget))
            else:
                widget._dbg_properties = get_resolved_properties(widget)

        return get_combined_properties(self.widgets)

    def _get_prop(self, prop, widget):
        return widget[prop]

    def _set_prop(self, prop, value, widget):
        widget.configure(**{prop: value})

    def can_optimize(self):
        return self.bases == list(set([get_base_class(widget) for widget in self.widgets]))

    def on_widgets_change(self):
        super().on_widgets_change()
        self.bases = bases = list(set([get_base_class(widget) for widget in self.widgets]))
        if len(bases) == 1:
            self.label = f"Attributes ({bases[0].__name__})"
        elif len(bases) > 1:
            self.label = f"Attributes (*)"
        else:
            self.label = "Attributes"


class LayoutGroup(StyleGroup):

    handles_layout = True

    def __init__(self, master, pane, **cnf):
        super().__init__(master, pane, **cnf)
        self.label = "Layout"
        self._layouts = []

    def _layout_def(self, widget):
        layout = layouts.get_layout(widget)
        if layout:
            return layout.get_def(widget)
        return {}

    def get_definition(self):
        return combine_properties([self._layout_def(widget) for widget in self.widgets])

    def _get_prop(self, prop, widget):
        layout = layouts.get_layout(widget)
        if layout:
            return layout.configure(widget)[prop]

    def _set_prop(self, prop, value, widget):
        layout = layouts.get_layout(widget)
        if layout:
            layout.configure(widget, **{prop: value})

    def can_optimize(self):
        return self._layouts == list(set(filter(lambda x: x, [layouts.get_layout(widget) for widget in self.widgets])))

    def on_widgets_change(self):
        super().on_widgets_change()

        self._layouts = list(set(filter(lambda x: x, [layouts.get_layout(widget) for widget in self.widgets])))

        if len(self._layouts) == 1:
            self.label = f"Layout ({self._layouts[0].name})"
        elif len(self._layouts) > 1:
            self.label = f"Layout (*)"
        elif all(not widget.winfo_ismapped() for widget in self.widgets):
            self._show_empty("Widget(s) not mapped")
            self.label = "Layout"
        else:
            self._show_empty("Unknown layout manager")
            self.label = "Layout"


class StylePane(StylePaneFramework, Pane):
    name = "Widget config"

    def __init__(self, master, debugger):
        super(StylePane, self).__init__(master)
        Label(self._header, **self.style.text_accent, text=self.name).pack(side="left")
        self.debugger = debugger
        self.setup_style_pane()
        self.add_group(LayoutGroup)
        self.add_group(AttributeGroup)
        self.debugger.bind("<<SelectionChanged>>", self.on_selection_changed, True)
        self.debugger.bind("<<WidgetModified>>", self._on_config_change)

    def _on_config_change(self, _):
        if self.debugger.active_widget in self.widgets:
            self.render_styles()

    def on_selection_changed(self, _):
        if self.debugger.selection:
            self._select(None, self.debugger.selection)
        else:
            self._select(None, [])

    def get_header(self):
        return self._header

    def last_action(self):
        pass

    def new_action(self, action):
        pass

    def widgets_modified(self, widgets):
        pass
