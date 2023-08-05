# -*- coding: UTF-8 -*-
# Copyright (C) 2008 Henry Obein <henry@itaapy.com>
# Copyright (C) 2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
from copy import deepcopy

# Import from itools
from itools.core import freeze
from itools.datatypes import Enumerate
from itools.stl import stl
from itools.uri import decode_query, Reference
from context import FormError



def process_form(get_value, schema):
    values = {}
    invalid = []
    missing = []
    for name in schema:
        datatype = schema[name]
        try:
            value = get_value(name, type=datatype)
        except FormError, error:
            value = get_value(name)
            missing.extend(error.missing)
            invalid.extend(error.invalid)
        values[name] = value
    if missing or invalid:
        raise FormError(missing=missing, invalid=invalid)
    return values



class BaseView(object):

    # Access Control
    access = False

    def __init__(self, **kw):
        for key in kw:
            setattr(self, key, kw[key])


    #######################################################################
    # Query
    query_schema = {}


    def get_query_schema(self):
        return self.query_schema


    def get_query(self, context):
        get_value = context.get_query_value
        schema = self.get_query_schema()
        return process_form(get_value, schema)


    def on_query_error(self, resource, context):
        return 'The query could not be processed.'


    #######################################################################
    # Caching
    def get_mtime(self, resource):
        return None


    #######################################################################
    # Request methods
    def GET(self, resource, context):
        raise NotImplementedError


    def POST(self, resource, context):
        raise NotImplementedError


    #######################################################################
    # View's metadata
    title = None

    def get_title(self, context):
        return self.title


    #######################################################################
    # Canonical URI for search engines
    # "language" is by default because too widespreaded
    canonical_query_parameters = freeze(['language'])


    def get_canonical_uri(self, context):
        """Return the same URI stripped from redundant view name, if already
        the default, and query parameters not affecting the resource
        representation.
        Search engines will keep this sole URI when crawling different
        combinations of this view.
        """
        uri = deepcopy(context.uri)
        query = uri.query
        # Remove the view name if default
        view_name = context.view_name
        if view_name:
            resource = context.resource
            if view_name == resource.get_default_view_name():
                uri = uri.resolve2('..')
        # Remove noise from query parameters
        canonical_query_parameters = self.canonical_query_parameters
        for parameter in query.keys():
            if parameter not in canonical_query_parameters:
                del query[parameter]
        uri.query = query
        return uri



class BaseForm(BaseView):

    schema = {}


    def get_schema(self, resource, context):
        # Check for specific schema
        action = getattr(context, 'form_action', None)
        if action is not None:
            schema = getattr(self, '%s_schema' % action, None)
            if schema is not None:
                return schema

        # Default
        return self.schema


    def _get_form(self, resource, context):
        """Form checks the request form and collect inputs consider the
        schema.  This method also checks the request form and raise an
        FormError if there is something wrong (a mandatory field is missing,
        or a value is not valid) or None if everything is ok.

        Its input data is a list (fields) that defines the form variables to
          {'toto': Unicode(mandatory=True, multiple=False, default=u'toto'),
           'tata': Unicode(mandatory=True, multiple=False, default=u'tata')}
        """
        get_value = context.get_form_value
        schema = self.get_schema(resource, context)
        return process_form(get_value, schema)


    def get_value(self, resource, context, name, datatype):
        return datatype.get_default()


    def _get_action(self, resource, context):
        """Default function to retrieve the name of the action from a form
        """
        form = context.get_form()
        action = form.get('action')
        if action is None:
            context.form_action = 'action'
            return

        action = 'action_%s' % action
        # Save the query of the action into context.form_query
        if '?' in action:
            action, query = action.split('?')
            # Deserialize query using action specific schema
            schema = getattr(self, '%s_query_schema' % action, None)
            context.form_query = decode_query(query, schema)

        context.form_action = action


    def get_action_method(self, resource, context):
        return getattr(self, context.form_action, None)


    def on_form_error(self, resource, context):
        context.message = context.form_error.get_message()
        return self.GET


    def POST(self, resource, context):
        # (1) Find out which button has been pressed, if more than one
        self._get_action(resource, context)

        # (2) Automatically validate and get the form input (from the schema).
        try:
            form = self._get_form(resource, context)
        except FormError, error:
            context.form_error = error
            return self.on_form_error(resource, context)

        # (3) Action
        method = self.get_action_method(resource, context)
        if method is None:
            msg = "the '%s' method is not defined"
            raise NotImplementedError, msg % context.form_action
        goto = method(resource, context, form)

        # (4) Return
        if goto is None:
            return self.GET
        return goto



class STLView(BaseView):

    template = None


    def get_namespace(self, resource, context, query=None):
        return {}


    def get_template(self, resource, context):
        # Check there is a template defined
        if self.template is None:
            msg = "%s is missing the 'template' variable"
            raise NotImplementedError, msg % repr(self.__class__)
        # XXX A handler actually
        return resource.get_resource(self.template)


    def GET(self, resource, context):
        # Get the namespace
        namespace = self.get_namespace(resource, context)
        if isinstance(namespace, Reference):
            return namespace

        # STL
        template = self.get_template(resource, context)
        return stl(template, namespace)



class STLForm(STLView, BaseForm):

    def get_namespace(self, resource, context, query=None):
        """This utility method builds a namespace suitable to use to produce
        an HTML form. Its input data is a dictionnary that defines the form
        variables to consider:

          {'toto': Unicode(mandatory=True, multiple=False, default=u'toto'),
           'tata': Unicode(mandatory=True, multiple=False, default=u'tata')}

        Every element specifies the datatype of the field.
        The output is like:

            {<field name>: {'value': <field value>, 'class': <CSS class>}
             ...}
        """
        # Figure out whether the form has been submit or not (FIXME This
        # heuristic is not reliable)
        schema = self.get_schema(resource, context)
        submit = (context.method == 'POST')

        # Build the namespace
        namespace = {}
        for name in schema:
            datatype = schema[name]
            is_mandatory = getattr(datatype, 'mandatory', False)
            is_readonly = getattr(datatype, 'readonly', False)

            cls = []
            if is_mandatory:
                cls.append('field-is-required')
            if submit and not is_readonly:
                try:
                    value = context.get_form_value(name, type=datatype)
                except FormError:
                    cls.append('field-is-missing')
                    if issubclass(datatype, Enumerate):
                        value = datatype.get_namespace(None)
                    else:
                        value = context.get_form_value(name)
                else:
                    if issubclass(datatype, Enumerate):
                        value = datatype.get_namespace(value)
                    elif datatype.multiple:
                        # XXX Done for table multilingual fields (fragile)
                        value = value[0]
                    else:
                        value = datatype.encode(value)
            else:
                value = self.get_value(resource, context, name, datatype)
                if issubclass(datatype, Enumerate):
                    value = datatype.get_namespace(value)
                else:
                    value = datatype.encode(value)
            cls = ' '.join(cls) or None
            namespace[name] = {'name': name, 'value': value, 'class': cls}
        return namespace

