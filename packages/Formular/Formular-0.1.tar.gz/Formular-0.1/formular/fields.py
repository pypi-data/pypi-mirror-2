#!/usr/bin/env python
# coding: utf-8
"""
    formular.fields
    ~~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from itertools import count
from decimal import Decimal
from datetime import date, time

try:
    from babel.dates import format_time, parse_time, format_date, parse_date
    HAS_BABEL = True
except ImportError:
    HAS_BABEL = False
    format_time = parse_time = None

from formular import validators
from formular.datastructures import missing, OrderedDict
from formular.exceptions import ValidationError, MultipleValidationErrors
from formular._utils import (_get_cls_args, _value_matches_choice,
                             _iter_choices, _to_list, _make_name)
from formular.widgets import (TextInput, PasswordInput, Checkbox, Textarea,
                              RadioButtonGroup, CheckboxGroup, MappingWidget,
                              MultipleWidget)

def _(message):
    """
    Dummy gettext function used to mark a string as translateable for
    xgettext.
    """
    return message

class FieldMeta(type):
    _dict_names = ["validator_factories", "error_messages"]

    def __call__(self, *args, **kwargs):
        dicts = dict((dict_name, {}) for dict_name in self._dict_names)
        for base in self.mro():
            for dict_name, d in dicts.iteritems():
                d.update(getattr(base, dict_name, {}))
        for dict_name, d in dicts.iteritems():
            if hasattr(self, dict_name):
                d.update(getattr(self, dict_name))
            setattr(self, dict_name, d)
        return type.__call__(self, *args, **kwargs)

#: Returns a unique, increasing position hint.
next_position_hint = count().next

class Field(object):
    """
    The base class of any field.

    :param name:
        The name the field is should have. If you are assigning this field to a
        form, passing this name is unnecessary. Should the given name and the
        assigned differ, the assigned is used.

    :param label:
        The name for the field which is shown to the user.

    :param default:
        A default value.

    :param error_messages:
        A dictionary which updates the error messages provided by the class.

    Validators are passed as keyword arguments. The name of the validator is
    passed as key with the initial value as value.

    Available validators for this field are:
        - :func:`formular.validators.required`
        - :func:`formular.validators.requires`
        - :func:`formular.validators.equals`

    Validators and error messages are inherited by subclasses.
    """
    __metaclass__ = FieldMeta

    #: A dictionary of validators used by this field. Keys are the names which
    #: should be used as keyword arguments in the constructor. Values are
    #: validator factories as returned by
    #: :func:`formular.validators.as_validator`.
    validator_factories = {
        "required": validators.required,
        "requires": validators.requires,
        "equals": validators.equals
    }

    #: Maps the validator names to the corresponding error messages.
    error_messages = {
        "invalid": _(u"The value is invalid."),
        "required": _(u"This field is required."),
        "requires": _(u"Requires {{form.fields[{initial_value}].label}}."),
        "equals": _(u"Does not equal {{form.fields[{initial_value}].label}}.")
    }

    #: The default value for this field type. Default values may be mutable so
    #: so you should never modify them.
    default = missing

    #: The widget type used to render this field.
    widget = TextInput

    @classmethod
    def register_as_validator(cls, obj):
        """
        Decorator to add a validator.

        :param obj: Either a name or a callable object with a ``__name__``
                    attribute.

        This method can be used like this::

            @Field.register_as_validator
            def required(form, is_required, value):
                return bool(value) if is_required else True

        However you might not wanna have a `required` - or whatever the name is
        - function lying around somewhere, so you can just
        define the name explicitly::

            @Field.register_as_validator("required")
            def a_name_i_like_a_lot_more(form, is_required, value):
                return bool(value) if is_required else True

        .. note:: If you register a validator on a field class, this validator
                  will be registered on every subclass of this field.
        """
        def decorate(func, name=obj):
            cls.validator_factories[name] = validators.as_validator(func)
            return func
        if not isinstance(obj, basestring):
            return decorate(obj, name=obj.__name__)
        return decorate

    def __init__(self, name=None, label=None, default=missing,
                 error_messages=None, **validators):
        self.label = label
        if default is not missing:
            self.default = default
        self.error_messages = self.error_messages.copy()
        if error_messages:
            self.error_messages.update(error_messages)
        self.validators = {}
        for name, initial_value in validators.iteritems():
            try:
                validator_factory = self.validator_factories[name]
            except KeyError:
                raise ValueError(
                    "{0} has no {1} validator.".format(
                        self.__class__.__name__,
                        name
                    )
                )
            else:
                self.validators[name] = validator_factory(initial_value)

        self.name = name
        self.form = None
        self.position_hint = next_position_hint()
        self.errors = ValidationError()

    @property
    def value(self):
        """
        The parsed value or the default value.
        """
        return getattr(self, "_value", self.default)

    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self):
        del self._value

    @property
    def primitive_value(self):
        return self.to_primitive(self.value)

    @property
    def is_valid(self):
        """
        ``True`` if there are no errors.
        """
        return not self.errors

    @property
    def is_bound(self):
        return self.form is not None

    def copy(self, *args, **kwargs):
        """
        Returns a copy of the field, arguments passed to the constructor can be
        overridden by passing them.

        .. note:: Copies are always unbound, even if the copied field is bound.
        """
        init_argnames, init_kwargnames = _get_cls_args(self.__class__)
        if not args:
            args = [getattr(self, argname) for argname in init_argnames]
        for kwargname in init_kwargnames:
            if kwargname not in kwargs:
                kwargs[kwargname] = getattr(self, kwargname)
        for name, validator in self.validators.iteritems():
            kwargs[name] = validator.initial_value
        return self.__class__(*args, **kwargs)

    def bind(self, form, name=None):
        """
        Binds the field to the `form` and assigns a name if given.
        """
        self.form = form
        if name is not None:
            self.name = name

    def unbind(self, with_name=False):
        """
        Unbinds the field from the `form` and the name if `with_name` is
        ``True``.
        """
        self.form = None
        if with_name:
            self.name = None

    def convert(self, value):
        """
        Converts the given `value` to unicode.

        This method gets a unicode representation of the value this method
        should return. The given `value` should be a result of
        :meth:`to_primitive` but it can be anything.
        
        Therefore, if a conversion is not possible and the value is invalid, a
        :exc:`ValueError` may be raised. If that happens the "invalid" error
        message is added to :attr:`errors`.
        """
        return unicode(value)

    def to_primitive(self, value):
        """
        Converts the given `value` to unicode.

        A subclass may want to override this method if the unicode
        representation of `value` is not sufficient enough to get the `value`
        back.

        However this method has to return a unicode string and must not fail.
        """
        return unicode(value)

    def _format_error_message(self, error_message, validator_args):
        error_message = self.form.translations.gettext(error_message)
        last_error_message = error_message
        error_message = error_message.format(**validator_args)
        while last_error_message != error_message:
            last_error_message = error_message
            error_message = error_message.format(**validator_args)
        return error_message

    def validate(self, value):
        """
        Parses and validates `value`. If the validation fails with one or more
        errors this method returns ``False`` otherwise ``True``.

        The parsed value can be accessed through the `value` attribute, the
        errors are stored as a :class:`formular.exceptions.ValidationError`
        through the `errors` attribute.
        """
        if not self.is_bound:
            raise RuntimeError("Fields must be bound to be validated.")
        self.reset()
        errors = []
        try:
            self.value = self.convert(value)
        except ValueError:
            errors.append(self.error_messages["invalid"])
            self.errors = ValidationError(*errors)
            return self.is_valid
        for name, validator in self.validators.iteritems():
            if not validator(self.form, self.value):
                errors.append(self._format_error_message(
                    self.error_messages[name], validator.last_args)
                )
        self.errors = ValidationError(*errors)
        return self.is_valid

    def reset(self):
        """
        Resets the field after validation.
        """
        try:
            del self._value
        except AttributeError:
            pass
        self.errors = ValidationError()

    def as_widget(self, widget_type=None, dialect="html"):
        """
        Returns a `widget_type` instance for this field. If no `widget_type` is
        given, :attr:`widget` is used instead.

        :param dialect:
            The dialect used to render this widget. Supported are ``"html"``
            and ``"xhtml"``.
        """
        widget_type = widget_type or self.widget
        if not self.is_bound:
            raise RuntimeError("Widgets can only be created for bound fields.")
        return widget_type(self, self.name, dialect=dialect)

    def _base_repr(self):
        rv = ""
        if self.label is not None:
            rv += "label={0!r}".format(self.label)
        if self.default != self.__class__.default:
            rv += ", default={0!r}".format(self.default)
        if self.error_messages != self.__class__.error_messages:
            rv += ", error_messages={0!r}".format(self.error_messages)
        rv += ", " + ", ".join(
            "{0}={1!r}".format(name, validator.initial_value)
            for name, validator in self.validators.iteritems()
        )
        return rv.lstrip(", ")

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._base_repr())

class Mapping(Field):
    """
    Represents multiple different fields::

        >>> field = Mapping({"name": TextField(), "age": IntegerField()})
        >>> field.validate({"name": u"John Doe", "age": u"42"})

    :param mapped_fields:
        A dictionary or a list of pairs, with names as keys and fields as their
        values.
    """
    widget = MappingWidget

    def __init__(self, mapped_fields, **kwargs):
        Field.__init__(self, **kwargs)
        if not hasattr(mapped_fields, "iteritems"):
            mapped_fields = OrderedDict(mapped_fields)
        for name, field in mapped_fields.iteritems():
            field.name = name
        self.mapped_fields = mapped_fields
        self.errors = MultipleValidationErrors()

    @property
    def default(self):
        return getattr(self, "_default",
            OrderedDict(
                (field.name, field.default)
                for field in self.mapped_fields.itervalues()
            )
        )

    @default.setter
    def default(self, new_default):
        self._default = new_default

    def copy(self, *args, **kwargs):
        if args:
            mapped_fields = args[0]
        else:
            mapped_fields = OrderedDict(
                (field.name, field.copy())
                for field in self.mapped_fields.itervalues()
            )
        return Field.copy(self, mapped_fields, **kwargs)

    def bind(self, form, name=None):
        Field.bind(self, form, name)
        for field in self.mapped_fields.itervalues():
            field.bind(form, _make_name(name, field.name))

    def unbind(self, with_name=False):
        Field.unbind(self, with_name)
        for field in self.mapped_fields.itervalues():
            field.unbind()

    def convert(self, value):
        rv = OrderedDict()
        for name, field in self.mapped_fields.iteritems():
            rv[name] = field.convert(
                value.get(name, field.to_primitive(field.default))
            )
        return rv

    def to_primitive(self, value):
        rv = OrderedDict()
        for name, field in self.mapped_fields.iteritems():
            rv[name] = field.primitive_value
        return rv

    def validate(self, value):
        # If the fields were added after binding they may or may not be
        # correctly bound. So we have to ensure they are.
        if hasattr(self, "form"):
            self.bind(self.form)
        errors = OrderedDict()
        self.value = OrderedDict()
        for field_name, field in self.mapped_fields.iteritems():
            primitive_value = value.get(
                field_name,
                field.to_primitive(field.default)
            )
            if not field.validate(primitive_value):
                errors[field_name] = field.errors
            self.value[field_name] = field.value
        self.errors = MultipleValidationErrors(errors)
        return self.is_valid

    def __repr__(self):
        return "{0}({1!r}, {2})".format(
            self.__class__.__name__, self.mapped_fields, self._base_repr()
        )

class SizedField(Field):
    """
    Represents a field, which value has a length.

    Available validators for this field are:
        - :func:`formular.validators.min_length`
        - :func:`formular.validators.max_length`
    """
    validator_factories = {
        "min_length": validators.min_length,
        "max_length": validators.max_length
    }

    error_messages = {
        "min_length": _(u"Must be at least {initial_value} long."),
        "max_length": _(u"Must be shorter then {initial_value}.")
    }

class TextField(SizedField):
    """
    Represents a field which holds text.
    """
    error_messages = {
        "min_length": _(u"Must be at least {initial_value} characters long."),
        "max_length": _(u"Must be shorter then {initial_value} characters.")
    }

class PasswordField(TextField):
    """
    Represents a field which holds a password.
    """
    widget = PasswordInput

class ComparableField(Field):
    """
    Represents a field with a comparable value.

    Available validators for this field are:
        - :func:`formular.validators.min_value`
        - :func:`formular.validators.max_value`
    """
    validator_factories = {
        "min_value": validators.min_value,
        "max_value": validators.max_value
    }

    error_messages = {
        "min_value": _(u"Must be greater then {initial_value}."),
        "max_value": _(u"Must be lesser then {initial_value}.")
    }

class NumberField(ComparableField):
    """
    Represents a field which holds a number of a given type.

    :param number_type:
        The constructor of the number type this field should hold. If the value
        is ``None`` the value `number_type` attribute of the class is used
        instead.
    """
    number_type = int
    error_messages = {
        "invalid": _(u"A number is required.")
    }

    def __init__(self, number_type=None, **kwargs):
        ComparableField.__init__(self, **kwargs)
        if number_type is not None:
            self.number_type = number_type

    def convert(self, value):
        return self.number_type(value)

class IntegerField(NumberField):
    """
    Represents a field which holds an integer.
    """
    error_messages = {
        "invalid": _(u"An integer is required.")
    }

class FloatField(NumberField):
    """
    Represents a field which holds a float.
    """
    number_type = float

    error_messages = {
        "invalid": _(u"A float is required.")
    }

class DecimalField(NumberField):
    """
    Represents a field which holds a decimal.
    """
    number_type = Decimal

    error_messages = {
        "invalid": _(u"A decimal is required.")
    }

class BooleanField(Field):
    """
    Represents a field which holds a boolean value.
    """
    error_messages = {
        "invalid": _(u'The value must be either "True" or "False".')
    }

    default = False

    widget = Checkbox

    def convert(self, value):
        if value == u"True":
            return True
        elif value == u"False":
            return False
        raise ValueError()

class ChoiceField(Field):
    """
    Represents a field which allows the user to choose between different
    values.

    :param choices:
        A list of values or a list of pairs. If a list of pairs is passed each
        pair should be a tuple of a value and a label which should be used
        instead of the value to be displayed to the user.

        The choices can always be changed later using the :attr:`choices`
        attribute.
    """
    error_messages = {
        "invalid": _(u"The choice is invalid.")
    }

    widget = RadioButtonGroup

    def __init__(self, choices=None, **kwargs):
        Field.__init__(self, **kwargs)
        self.choices = choices or []

    def convert(self, value):
        for choice, _ in _iter_choices(self.choices):
            if _value_matches_choice(value, choice):
                return choice
        raise ValueError()

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.choices, self._base_repr()
        )

class MultiChoiceField(ChoiceField, SizedField):
    """
    Represents a field which allows the user to make multiple choices between
    different values.
    """
    error_messages = {
        "invalid": _(u"One or more choices are invalid.")
    }

    default = []

    widget = CheckboxGroup

    def convert(self, value):
        known_choices = {}
        for choice, _ in _iter_choices(self.choices):
            known_choices[choice] = choice
            known_choices[unicode(choice)] = choice
        result = []
        for value in _to_list(value):
            for version in value, unicode(value):
                if version in known_choices:
                    result.append(known_choices[version])
                    break
            else:
                raise ValueError()
        return result

    def to_primitive(self, choices):
        return [ChoiceField.to_primitive(self, choice) for choice in choices]

class Multiple(SizedField):
    """
    Represents multiple values of the same field.

    >>> field = Multiple(IntegerField())
    >>> field.validate([u"1", u"2", u"3"])
    True
    >>> field.value
    [1, 2, 3]
    """
    error_messages = {
        "min_length": _(u"Requires at least {initial_value} values."),
        "max_length": _(u"Requires at most {initial_value} values.")
    }

    default = []

    widget = MultipleWidget

    def __init__(self, field, **kwargs):
        Field.__init__(self, **kwargs)
        self.field = field

    def bind(self, form, name=None):
        SizedField.bind(self, form, name)
        self.field.bind(form)

    def unbind(self, with_name=False):
        SizedField.unbind(self, with_name)
        self.field.unbind()

    def convert(self, values):
        return map(self.field.convert, values)

    def to_primitive(self, values):
        return map(self.field.to_primitive, values)

    def validate(self, values):
        self.reset()
        errors = OrderedDict()
        try:
            self.value = self.convert(values)
        except ValueError:
            self.errors = ValidationError(self.error_messages["invalid"])
            return self.is_valid
        for i, value in enumerate(self.value):
            if not self.field.validate(value):
                errors[unicode(i)] = self.field.errors
            self.value[i] = self.field.value
        self.field.reset()
        self.errors = MultipleValidationErrors(errors)
        return self.is_valid

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.field, self._base_repr()
        )

class Seperated(Multiple):
    """
    Represents multiple values seperated by a string.

    :param seperator:
        The string the values are seperated with.

    :param strip_values:
        If ``True`` each primitive value is stripped before converting it.

    :param primitive_prefix:
        A prefix which will be added to the `seperator` to create a primitive
        in :meth:`to_primitive`.

        This is useful in combination with `strip_values`::

            >>> f = Seperated(seperator=u",", strip_values=True,
                              seperator_prefix=u" ")
            >>> # a user can pass a primitive value like this for validation...
            >>> f.validate(u"foo, bar,baz")
            >>> # and the value is...
            >>> f.value
            [u"foo", u"bar", u"baz"]
            >>> # however the generated primitive looks like this...
            >>> f.to_primitive(f.value)
            u"foo, bar, baz"
            >>> # which looks a lot nicer then the primitive we got at
            >>> # validation
    """
    widget = TextInput

    def __init__(self, field=None, seperator=u",", strip_values=True,
                 seperator_prefix=u" ", **kwargs):
        Multiple.__init__(self, field or TextField(), **kwargs)
        self.seperator = seperator
        self.strip_values = strip_values
        self.seperator_prefix = seperator_prefix

    def convert(self, string):
        return [
            self.field.convert(p.strip() if self.strip_values else p)
            for p in string.split(self.seperator)
        ]

    def to_primitive(self, values):
        return (self.seperator + self.seperator_prefix).join(
            self.field.to_primitive(value) for value in values
        )

    def __repr__(self):
        return ("{0}(field={1}, seperator={2!r}, strip_values={3}, "
                "seperator_prefix={4!r}, {5})").format(
            self.__class__.__name__,
            self.field,
            self.seperator,
            self.strip_values,
            self.seperator_prefix,
            self._base_repr()
        )

if HAS_BABEL:
    class TimeField(ComparableField):
        """
        Represents a :class:`datetime.time` instance.

        :param format:
            One of ``"full"``, ``"long"`` or ``"medium"``.
        """
        error_messages = {
            "invalid": _("Invalid time.")
        }

        def __init__(self, format="medium", **kwargs):
            ComparableField.__init__(self, **kwargs)
            self.format = format

        def to_primitive(self, value):
            if not isinstance(value, time):
                return u""
            return format_time(value, format=self.format,
                locale=self.form.translations.locale
            )

        def convert(self, value):
            try:
                result = parse_time(
                    value,
                    locale=self.form.translations.locale
                )
            except IndexError:
                raise ValueError()
            # FIXME: This should be done upstream in babel.
            if "pm" in value.lower() and result.hour != 12:
                result = result.replace(hour=result.hour + 12)
            return result

    class DateField(ComparableField):
        """
        Represents a :class:`datetime.date` instance.

        :param format:
            `"short"`` or a custom date/time pattern.
        """
        error_messages = {
            "invalid": _(u"Invalid date.")
        }

        def __init__(self, format="short", **kwargs):
            ComparableField.__init__(self, **kwargs)
            self.format = format

        def to_primitive(self, value):
            if not isinstance(value, date):
                return u""
            return format_date(value, format=self.format,
                locale=self.form.translations.locale
            )

        def convert(self, value):
            try:
                return parse_date(value, locale=self.form.translations.locale)
            except IndexError:
                raise ValueError()

__all__ = [
    "Field", "Mapping", "SizedField", "TextField", "PasswordField",
    "ComparableField", "NumberField", "IntegerField", "FloatField",
    "ComplexField", "DecimalField", "BooleanField", "ChoiceField",
    "MultiChoiceField", "Multiple", "Seperated"
]

if HAS_BABEL:
    __all__.extend(["TimeField", "DateField"])
