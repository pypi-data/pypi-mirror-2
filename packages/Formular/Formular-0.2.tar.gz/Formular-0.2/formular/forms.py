#!/usr/bin/env python
# coding: utf-8
"""
    formular.forms
    ~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from collections import defaultdict

from formular.fields import Field, Mapping
from formular.datastructures import OrderedDict, missing
from formular.i18n import get_translations
from formular._csrf import _get_csrf_token, _remove_csrf_token
from formular.widgets import FormWidget
from formular.exceptions import ValidationError

def _iter_lists(d):
    if hasattr(d, "iterlists"):
        return d.iterlists()
    rv = defaultdict(list)
    for key, value in d.iteritems():
        if isinstance(value, (tuple, list)):
            rv[key].extend(value)
        else:
            rv[key].append(value)
    return rv.iteritems()

def _split_key(key):
    for part in key.split("."):
        if part.isdigit():
            yield int(part)
        else:
            yield part

def _decode_dict(d):
    list_marker = object()
    value_marker = object()

    def enter_container(container, key):
        return container.setdefault(key, {list_marker: False})

    def convert(container):
        if value_marker in container:
            values = container.pop(value_marker)
            if container.pop(list_marker):
                values.extend(convert(x[1]) for x in sorted(container.items()))
                return values
            if len(values) == 1:
                return values[0]
            return values
        elif container.pop(list_marker):
            return [convert(x[1]) for x in sorted(container.items())]
        return dict((k, convert(v)) for k, v in container.iteritems())

    result = {list_marker: False}
    for key, values in _iter_lists(d):
        parts = list(_split_key(key))
        container = result
        for part in parts:
            last_container = container
            container = enter_container(container, part)
            last_container[list_marker] = isinstance(part, int)
        container[value_marker] = values
    return convert(result)

class FormMeta(type):
    def __call__(self, *args, **kwargs):
        fields = []
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue
            attribute = getattr(self, attribute_name)
            if isinstance(attribute, Field):
                fields.append((attribute_name, attribute))
        fields.sort(key=lambda x: x[1].position_hint)
        self.unbound_fields = OrderedDict(fields)
        return type.__call__(self, *args, **kwargs)

class Form(object):
    """
    The base class for forms. Fields can be assigned declarativly, on a created
    class or on an instance::

        class LoginForm(Form):
            username = TextField(label=u"Username", required=True)
            password = PasswordField(label=u"Password", required=True)
            repeat_password = password.copy(label=u"Repeat password",
                                            equals="password")
            permanent = BooleanField(label=u"Keep me logged in")

    Fields can be accessed as an attribute or dict-like using
    ``LoginForm()["username"]``.

    Sometimes you may want to validate a field in a way which only makes sense
    in the context of the form type you are defining. In order to do that
    you define a method with the name `validate_FIELD_NAME`. Such a method gets
    the value of the field `FIELD_NAME` as an argument.

    If you want to validate the form itself you can define a `validate_context`
    method which get's called upon validation.

    :param initial_data:
        If you want to use different default values for the fields you can pass
        a dictionary, using this parameter.

    :param locale:
        For localization provide a locale string, currently supported are:
            - en
            - de

    .. versionadded:: 0.2
       `validate_*` methods.
    """
    __metaclass__ = FormMeta

    def __init__(self, initial_data=missing, locale="en"):
        def wrap_validator(validator):
            def wrapper(form, value):
                return validator(value)
            return wrapper
        self._root_field = Mapping(OrderedDict(), default=initial_data)
        self._root_field.bind(self)
        for name, field in self.unbound_fields.iteritems():
            field = field.copy()
            validator = getattr(self, "validate_" + name, None)
            if validator:
                field.validators["context"] = wrap_validator(validator)
            field.bind(self, name)
            self._root_field.mapped_fields[name] = field
            setattr(self, name, field)
        root_validator = getattr(self, "validate_context", None)
        if root_validator:
            self._root_field.validators["context"] = lambda f, v: root_validator()
        self.translations = get_translations(locale)
        self.hidden_data = {}

    @property
    def fields(self):
        """
        The fields of this form.

        .. note:: Adding fields directly to this dictionary won't bind them.
                  Use ``Form().new_field = Field()`` instead.
        """
        return self._root_field.mapped_fields

    @property
    def data(self):
        """
        The validated or default data.
        """
        return self._root_field.value

    @property
    def initial_data(self):
        """
        The initial form data.
        """
        return self._root_field.default

    @property
    def errors(self):
        """
        A :exc:`formular.exceptions.MultipleValidationErrors` instance with the
        errors which occured during validation or a
        :exc:`formular.exceptions.ValidationError` if an error occurred at form
        level.
        """
        return self._root_field.errors

    @property
    def is_valid(self):
        """
        ``True`` if the :attr:`data` is valid.
        """
        return self._root_field.is_valid

    def reset(self):
        """
        Resets the form to the initial data.
        """
        self._root_field.reset()

    def validate(self, form_data):
        """
        Validates the form against the given `form_data`.
        """
        self.reset()
        return self._root_field.validate(_decode_dict(form_data))

    @classmethod
    def as_mapping(cls):
        """
        Returns the form as a :class:`formular.fields.Mapping`.
        """
        return cls()._root_field.copy()

    def __getattr__(self, name):
        try:
            return self.fields[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if isinstance(value, Field) and name != "_root_field":
            value.bind(self, name)
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        is_field = False
        if name in self.fields:
            del self.fields[name]
            is_field = True
        try:
            object.__delattr__(self, name)
        except AttributeError:
            # If the deleted attribute was a field which was not set as an
            # attribute, e.g. added via ``form.fields["foo"] = Field()``,
            # an :exc:`AttributeError` can occur.
            # In every other case we want the :exc:`AttributeError` raised.
            if not is_field:
                raise

    def __repr__(self):
        return "{0}(locale={1!r}, **kwargs)".format(
            self.__class__.__name__,
            self.translations.locale
        )

class HTMLForm(Form):
    """
    Represents the logic for an HTML form.

    :param session:
        An object with a dict-like interface in which session related data can
        be stored.

    :param action:
        The path under which the form can be reached.

    :param remote_addr:
        The `REMOTE_ADDR` from the wsgi environment. This is required for the
        reCAPTCHA support.

        .. versionadded:: 0.2
    """
    #: If ``True`` this form will be protected against cross-site request
    #: forgery, as long as it is protectable.
    csrf_protection_enabled = True

    #: The public reCAPTCHA api key.
    #:
    #: .. versionadded:: 0.2
    recaptcha_public_key = None

    #: The private reCAPTCHA api key.
    #:
    #: .. versionadded:: 0.2
    recaptcha_private_key = None

    def __init__(self, session=None, action=u"", remote_addr=None, **kwargs):
        Form.__init__(self, **kwargs)
        self.session = session
        self.action = action
        self.remote_addr = remote_addr

    @property
    def hidden_data(self):
        if self.is_csrf_protected:
            self._hidden_data["_csrf_token"] = self.csrf_token
        else:
            self._hidden_data.pop("_csrf_token", None)
        return self._hidden_data

    @hidden_data.setter
    def hidden_data(self, new_hidden_data):
        self._hidden_data = new_hidden_data

    @property
    def is_csrf_protectable(self):
        """
        ``True`` if :attr:`session` is not ``None`` and :attr:`action` is
        specified.
        """
        return self.action and self.session is not None

    @property
    def is_csrf_protected(self):
        """
        ``True`` if the field is protected against csrf.
        """
        return self.is_csrf_protectable and self.csrf_protection_enabled

    @property
    def csrf_token(self):
        """
        The csrf token for this form. If necessary this property should set the
        token on the session.
        """
        if not self.is_csrf_protectable:
            raise AttributeError(
                "CSRF token requires the form the be protectable"
            )
        return _get_csrf_token(self.session, self.action)

    def validate(self, form_data, without_csrf_protection=False):
        """
        Validates the given `form_data`.

        :param without_csrf_protection:
            Pass ``True`` if you want to turn of the csrf protection for a
            validation e.g. if you want to validate form data you got via an
            JSON/XML API of your application.

        .. versionchanged:: 0.2
           `form_data` values are now converted to unicode if necessary.
        """
        self.reset()
        raw_form_data = form_data
        form_data = {}
        for key, value in raw_form_data.iteritems():
            if isinstance(value, unicode):
                form_data[key] = value
            else:
                form_data[key] = value.decode("iso-8859-1")
        form_data = _decode_dict(form_data)
        if self.is_csrf_protected and not without_csrf_protection:
            csrf_token = form_data.get("_csrf_token")
            if csrf_token != self.csrf_token:
                self._root_field.errors = ValidationError(
                    self.translations.gettext(
                        u"Form submitted multiple times or session expired. "
                        u"Please try again."
                    )
                )
            _remove_csrf_token(self.session, self.action)
            if not self.is_valid:
                return False
        return Form.validate(self, form_data)

    def as_widget(self):
        """
        Returns the :class:`HTMLForm` as a
        :class:`formular.widgets.FormWidget`.
        """
        return FormWidget(self)

    def __repr__(self):
        return "{0}(session={1!r}, action={2!r}, **kwargs)".format(
            self.__class__.__name__,
            self.session,
            self.action
        )

class ConfigurationForm(Form):
    #: If your configuration format requires sections(like ini), you can
    #: specify a main section, instead of using a
    #: :class:`formular.fields.Mapping` instance for every section.
    #: This does only affect assignment of fields on the class, not on the
    #: instance.
    main_section = None

    #: If :attr:`main_section` is set to ``True`` every field which is not a
    #: mapping is dropped.
    drop_main_fields = True

    def __init__(self, *args, **kwargs):
        if self.drop_main_fields and self.main_section is not None:
            main_fields = OrderedDict()
            unbound_fields = OrderedDict()
            for name, field in self.unbound_fields.iteritems():
                if hasattr(field, "mapped_fields"):
                    unbound_fields[name] = field
                else:
                    main_fields[name] = field
            unbound_fields[self.main_section] = Mapping(main_fields)
            self.unbound_fields = unbound_fields
        Form.__init__(self, *args, **kwargs)

__all__ = ["Form", "HTMLForm", "ConfigurationForm"]
