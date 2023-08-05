#!/usr/bin/env python
# coding: utf-8
"""
    formular.widgets
    ~~~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from cgi import escape
from itertools import imap, chain

from formular._utils import _is_choice_selected, _iter_choices, _make_name

PLAINTEXT_ELEMENTS = set(["textarea"])
CDATA_ELEMENTS = set(["script", "style"])
CHILDLESS_ELEMENTS = set([
    "area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
    "isindex", "link", "meta", "param"
])

def _format_attributes(attributes):
    items = []
    for key, value in attributes.iteritems():
        if value is None:
            continue
        if isinstance(value, bool):
            if value:
                value = key
            else:
                continue
        value = escape(value, True)
        items.append(u'{0}="{1}"'.format(key, value))
    return (u" " + u" ".join(items)) if items else u""

def _make_tag(tag, children, attributes, dialect="html"):
    attributes = _format_attributes(attributes)
    if tag in CHILDLESS_ELEMENTS:
        if dialect == "xhtml":
            return u"<{0}{1} />".format(tag, attributes)
        else:
            return u"<{0}{1}>".format(tag, attributes)
    children = u"".join(imap(unicode, children))
    if tag in PLAINTEXT_ELEMENTS:
        children = escape(children)
    elif tag in CDATA_ELEMENTS and dialect == "xhtml":
        children = u"/*<![CDATA[*/{0}/*]]>*/".format(children)
    return u"<{0}{1}>{2}</{0}>".format(tag, attributes, children)

class _Builder(object):
    def __init__(self, dialect):
        self.dialect = dialect

    def __getattr__(self, tag):
        def proxy(*children, **attributes):
            return _make_tag(tag, children, attributes, dialect=self.dialect)
        return proxy

    def __repr__(self):
        return "{0}({1!r})".format(self.__class__.__name__, self.dialect)

_BUILDERS = {
    "html": _Builder("html"),
    "xhtml": _Builder("xhtml")
}

class Renderable(object):
    """
    An object which is renderable to `html` or `xhtml` depending one the
    given `dialect`.
    """
    dialect = "html"

    def __init__(self, dialect=None):
        if dialect is not None:
            self.dialect = dialect

    @property
    def builder(self):
        """
        The builder used to create the html/xhtml.
        """
        return _BUILDERS[self.dialect]

    def render(self):
        """
        Returns a rendered version of this object as unicode string.
        """
        return u""

    def __unicode__(self):
        return self.render()

    def __repr__(self):
        return "{0}(dialect={1!r})".format(
            self.__class__.__name__,
            self.dialect
        )

class Label(Renderable):
    """
    Represents a label which is used to display the name of a field.

    :param text:
        A unicode string with the name of the field.

    :param field_id:
        The id of the field this label refers to.
    """
    def __init__(self, text, field_id, **kwargs):
        Renderable.__init__(self, **kwargs)
        self.text = text
        self.field_id = field_id

    def render(self):
        return self.builder.label(
            self.text,
            **{"for": self.field_id}
        )

    def __repr__(self):
        return "{0}({1!r}, {2!r}, dialect={3!r})".format(
            self.__class__.__name__, self.text, self.field_id, self.dialect
        )

class Widget(Renderable):
    """
    Represents a field as a UI-Element.

    :param field:
        A :class:`formular.fields.Field` instance.

    :param name:
        The name of the instance.
    """
    def __init__(self, field, name, **kwargs):
        Renderable.__init__(self, **kwargs)
        self.field = field
        self.name = name

    @property
    def label(self):
        """
        The label of the field as a :class:`Label` instance.
        """
        return Label(self.field.label, self.id, dialect=self.dialect)

    @property
    def value(self):
        """
        The primitive value of the field.
        """
        return self.field.primitive_value

    @property
    def id(self):
        return u"f_{0}".format(self.name.replace(u".", u"_"))

    def __repr__(self):
        return "{0}({1!r}, {2!r}, dialect={3!r})".format(
            self.__class__.__name__, self.field, self.name, self.dialect
        )

class ChildWidget(Widget):
    """
    Represents a value of field as a UI-Element.
    """
    def __init__(self, parent):
        self.parent = parent

    @property
    def dialect(self):
        return self.parent.dialect

    def __repr__(self):
        return "{0}({1!r})".format(self.__class__.__name__, self.parent)

class Input(Widget):
    """
    The base class for input widgets.
    """
    #: Specifies the type of the input widget.
    type = None

    def render(self):
        attrs = {}
        if self.type == "checkbox" and self.field.value:
            attrs["checked"] = "checked"
        else:
            attrs["value"] = self.value if self.type != "password" else None
        return self.builder.input(
            id=self.id,
            name=self.name,
            type=self.type,
            **attrs
        )

class TextInput(Input):
    """
    Represents every field which is not represented through any other widget as
    well as :class:`formular.fields.TextField` instance for single lines.
    """
    type = "text"

class PasswordInput(Input):
    """
    Represents a :class:`formular.fields.PasswordField` instance as an
    UI-Element.
    """
    type = "password"

class Checkbox(Input):
    """
    Represents a :class:`formular.fields.BooleanField` instance as an
    UI-Element.
    """
    type = "checkbox"

    @property
    def checked(self):
        """
        ``True`` if the field is checked.
        """
        return self.field.value

class Textarea(Widget):
    """
    Represents a :class:`formular.fields.TextField` instance as one or more
    lines of text in the UI.
    """
    def render(self, **attrs):
        return self.builder.textarea(self.value, name=self.name, **attrs)

class InputGroupMember(ChildWidget):
    """
    Represents a value of :class:`formular.fields.ChoiceField` instance.
    """
    value = label = None

    def __init__(self, parent, value, label):
        ChildWidget.__init__(self, parent)
        self.value = unicode(value)
        self.label = Label(label, self.id, dialect=self.dialect)

    @property
    def name(self):
        return self.parent.name

    @property
    def id(self):
        return "f_{0}_{1}".format(self.name, self.value)

    @property
    def checked(self):
        """
        ``True`` if the value for this widget is selected.
        """
        return _is_choice_selected(self.parent, self.value)

    def render(self, **attrs):
        return self.builder.input(
            id=self.id,
            type=self.type,
            name=self.name,
            value=self.value,
            checked=self.checked,
            **attrs
        )

    def __repr__(self):
        return "{0}({1!r}, {2!r}, {3!r})".format(
            self.__class__.__name__, self.parent, self.value, self.label
        )

class RadioButton(InputGroupMember):
    """
    Represents a :class:`formular.fields.ChoiceField` instance value as an
    UI-Element.
    """
    type = "radio"

class GroupCheckbox(InputGroupMember):
    """
    Represents a :class:`formular.fields.MultiChoiceField` instance value as an
    UI-Element.
    """
    type = "checkbox"

class ListWidgetMixin(Renderable):
    def as_ul(self, **attrs):
        """
        Renders the widget as an unordered list.
        """
        return self._as_list(self.builder.ul)

    def as_ol(self, **attrs):
        """
        Renders the widget as an ordered list.
        """
        return self._as_list(self.builder.ol)

    def _as_list(self, list_factory, **attrs):
        raise NotImplementedError(self.__class__.__name__ + "_as_list")

class InputGroup(Widget, ListWidgetMixin):
    """
    A base class for classes representing a `formular.fields.ChoiceField` as an
    UI-Element.
    """
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self.choices = []
        self.subwidgets = {}
        for value, label in _iter_choices(self.field.choices):
            widget = self.subwidget(self, value, label)
            self.choices.append(widget)
            self.subwidgets[value] = widget

    def _as_list(self, list_factory):
        return list_factory(*imap(self.builder.li, self.choices))

    def render(self):
        return self.as_ul()

class RadioButtonGroup(InputGroup):
    """
    Represents a :class:`formular.fields.ChoiceField` instance as an
    UI-Element.
    """
    subwidget = RadioButton

class CheckboxGroup(InputGroup):
    """
    Represents a :class:`formular.fields.MultiChoiceField` instance as an
    UI-Element.
    """
    subwidget = GroupCheckbox

class MappingWidget(Widget):
    """
    Represents a :class:`formular.field.MappingWidget` instance as an
    UI-Element and stores the widgets of the mapped fields.
    """
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self._subwidgets = {}

    def __getattr__(self, name):
        subwidget = self._subwidgets.get(name)
        if subwidget is None:
            try:
                field = self.field.mapped_fields[name]
                subwidget = field.widget(field, _make_name(self.name, name))
            except KeyError:
                raise AttributeError(name)
            self._subwidgets[name] = subwidget
        return subwidget

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError(name)

    def __iter__(self):
        for name in self.field.mapped_fields:
            yield self[name]

    def as_dl(self):
        """
        Renders the subwidgets as a definition list, where each term is the
        rendered field label and the corresponding description the rendered
        field.
        """
        return self.builder.dl(
            *(self.builder.dt(field.label.render()) + self.builder.dd(field)
              for field in self)
        )

    def as_tr(self):
        """
        Renders the subwidgets as a table row.
        """
        return self.builder.tr(
            *(self.builder.td(field.render()) for field in self)
        )

    def render(self):
        return self.as_dl()

class MultipleWidget(Widget, ListWidgetMixin):
    """
    Represents a :class:`formular.fields.Multiple` instance as an UI-Element.
    """
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self.subfield = self.field.field

    @property
    def subwidget(self):
        return self.subfield.as_widget()

    def _as_list(self, list_factory):
        rendered = []
        for i, value in enumerate(self.value):
            self.subfield.validate(value)
            self.subfield.name = _make_name(self.field.name, unicode(i))
            rendered.append(self.subwidget.render())
        self.subfield.reset()
        self.subfield.name = None
        return list_factory(*rendered)

    def render(self):
        return self.as_ul()

class FormWidget(Renderable):
    """
    Represents a :class:`formular.forms.HTMLForm` as an UI-Element.
    """
    def __init__(self, form, **kwargs):
        Renderable.__init__(self, **kwargs)
        self.form = form

    @property
    def errors(self):
        """
        A :class:`ValidationErrorWidget` instance.
        """
        return ValidationErrorWidget(self.form, dialect=self.dialect)

    def render(self, method=u"post", **attrs):
        """
        Returns the rendered form.

        :param method:
            The method used to send the form back to the server.

        .. note:: This method can be used as a
                  `jinja macro <http://jinja.pocoo.org/2/documentation/templates#call>`_
                  The caller will have to take care of the visible fields.
        """
        hidden = u"".join(
            self.builder.input(
                type="hidden",
                name=name,
                value=value
            ) for name, value in self.form.hidden_data.iteritems()
        )
        caller = attrs.pop("caller", None)
        if attrs:
            raise TypeError("Unexpected keyword argument.")
        if caller:
            body = caller()
        else:
            body = self.form._root_field.as_widget().as_dl()
        if hidden:
            # <input> fields must not be children of a <form> tag
            body += u'<div style="display: none">{0}</div>'.format(hidden)
        return self.builder.form(body, action=self.form.action, method=method)

class ValidationErrorWidget(ListWidgetMixin):
    """
    Represents the validation error of a :class:`formular.forms.Form` instance.
    """
    def __init__(self, form, dialect=None):
        ListWidgetMixin.__init__(self, dialect)
        self.form = form
        self._form_errors = None

    @property
    def errors(self):
        # As long as the form is not validated another time with other errors,
        # a cached result is returned.
        if self._form_errors == self.form.errors:
            return self._errors
        self._form_errors = self.form.errors
        self._errors = self.form.errors.unpack()
        if None not in self._errors:
            self._errors = dict(
                (self.form.fields[key].label, errors)
                for key, errors in self._errors.iteritems()
            )
        return self._errors

    def _as_list(self, list_factory, **attrs):
        if hasattr(self.errors, "itervalues"):
            errors = chain(*self.errors.itervalues())
        else:
            errors = self.errors
        return list_factory(
            *imap(self.builder.li, errors),
            **attrs
        )

    def as_dl(self, **attrs):
        """
        Renders the validation error as a definition list.

        This method may raise a :exc:`RuntimeError` if the form has top-level
        errors.
        """
        if not hasattr(self.errors, "iteritems"):
            raise RuntimeError(
                "can't render top-level errors as definition list"
            )
        return self.builder.dl(*(
            self.builder.dt(key) + self.builder.dd(value[0])
            for key, value in self.errors.iteritems()
        ))

    def render(self, **attrs):
        """
        Renders the validation error as a div with a headline. The errors
        are displayed as an unordered list if they cannot be displayed as a
        definition list.

        If the form has no validation errors this method returns an empty
        string.
        """
        if not self.errors:
            return u""
        attrs.setdefault("class", "form-errors")
        title = self.builder.h1(
            u"{0} errors occured during validation".format(len(self.errors))
        )
        try:
            errors = self.as_dl()
        except RuntimeError:
            errors = self.as_ul()
        return self.builder.div(title, errors, **attrs)

    def __repr__(self):
        return "{0}({1!r}, dialect={2!r})".format(
            self.__class__.__name__,
            self.form,
            self.dialect
        )

__all__ = [
    "TextInput", "PasswordInput", "Checkbox", "Textarea", "RadioButtonGroup",
    "CheckboxGroup", "MappingWidget", "MultipleWidget", "FormWidget",
    "ValidationErrorWidget"
]
