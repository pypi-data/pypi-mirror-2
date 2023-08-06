++++++++++++++++++
FormBuild 3 Manual
++++++++++++++++++

History
+++++++

FormBuild has seen three major releases, each incompatible with its
predecessor:

FormBuild 1

    A sophisticated and complex package for doing all sorts of clever things
    with forms. In reality though very few of them proved useful. Essentially
    FormBuild 1 was over-engineered.

FormBuild 2

    FormBuild 2 was a vastly simplified API focusing on the core use cases and
    with automatic variable escaping built in to help prevent XSS attacks. It
    re-used functionality from the WebHelpers package and was designed to work
    with FormEncode. The basic behaviour of FormBuild 2 was documented in `The
    Definitive Guide to Pylons <http://pylonsbook.com/>`_ but no offical
    documentation was ever released.

FormBuild 3 

    FormBuild 3 is another ground-up re-write, removing the dependency on
    WebHelpers, avoiding the use of ``literal()`` objects and only
    implementing the core features of FormBuild 2, unifying and improving the
    API.

    FormBuild 3 was written alongside FormConvert, a new package designed
    specifically to handle server-side validation and to complement FormBuild,
    avoiding the requirement to use FormEncode. 

    FormBuild 3 and FormConvert provide a carefully-designed and compelling
    form construction and validation framework but do not depend on each other
    and work perfectly well independently. 

Introduction
++++++++++++

FormBuild does one thing: It helps you build forms in HTML, populating field
values, setting options and displaying error messages. It explicitly avoids
any sort of validation and can work with any framework specifically because it
has no reliance on the way the framework operates. It also avoids any
integration with a database schema. 

Here are some alternatives:

* If you want forms generated automatically from SQLAlchemy schema try
  `FormAlchemy <http://code.google.com/p/formalchemy/>`_. 
* If you want combined validators and fields, try
  `ToscaWidgets <http://toscawidgets.org/>`_.
* If you just want some helpers to generate the HTML for you try
  `WebHelpers <http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/>`_.

The reason I personally use FormBuild over these alternatives is that I like
the fact that form generation is totally de-coupled from validation and yet
still allows you to build sophisticated, clean forms which are easy to
integrate with validation code.

.. note ::

   For a validation library which works well with FormBuild I'm personally
   using FormConvert. It isn't released yet but in the meantime you can use
   `FormEncode <http://formconvert.org>`_ or roll your own validation.

The innovation of FormBuild is model the way HMTL forms *behave* rather than
the way they are constructed. All the various combinations of HTML fields can
be modeled as either:

* single value fields which have a *name* and take a single *value* single
* value fields from options which have a *name* and take a single 
  *value* which must be one of the *options*
* multi value fields have have a *name*, a series of possilbe *options* 
  and zero or more *selected values*
* checkboxes which have *name* and take a *single value* but which can be
  *checked* or *unchecked* affecting whether the field is submitted or not

.. note ::

    A group of single value fields with the same name do not necessarily
    behave like a multi value field because the available *options* might not
    be restricted in the same way. The exception to this is a group of
    checkboxes which when used together do behave exactly like a multi value
    field such as an HTML ``<select>`` field with multiple values enabled.
    FormBuild therefore has a special field type called ``checkbox_group`` for
    treating a group of checkboxes as a single multi value field. In the same
    way, a group of radio buttons with the same name behaves similarly to a
    single value field from options (except that it is possible to select no
    value at all with a radiogroup) so FormBuild provides a ``radio_group``
    field.

FormBuild also separates form design from implementation. You can build a form
in a templating language but the values, options, error messages and which
check boxes are ticked are all confgured in your application. FormBuild
doesn't deal with validation which is dealt with by a separate package called
FormConvert. It also doesn't deal with multi-page workflows which is instead
dealt with by the Wizard package. By treating valdidation and workflow
separately from form construction and population you are also free to use
alternative tools such as FormEncode or roll your own approaches to deal with
more complex cases.

Tutorial
++++++++

Creating forms in Python can be tedious. FormBuild can help, particularly if
you want all the forms in a site to have a consistent style.

Start by creating your own form class from ``StandardForm``:

.. sourcecode :: pycon

    >>> from formbuild import Form
    >>> 
    >>> class StandardForm(Form):
    ...    pass

All your forms can now be built with ``StandardForm`` which means that if you
ever need to customise the look and feel or behaviour of all your forms, you
can do so in one place by customising your project's ``StandardForm`` class.

In FormBuild there are four important variables:

``value``

    A dictionary where each key is a field name and each value is the value it
    takes.

``error``

    A dictionary where each key is a field name and each value is a string
    representing an error associated with the current value of a field.

``option``

    Certain field types such as checkbox groups are made up of various
    different options of which the user picks one. Often the available options
    are determined at run-time based on other factors so the ``options``
    variable is used to specify the available options for a particular
    instance of a form for the types of fields which take options.

``checked``

    Radio and checkbox fields only submit their name and value if they are
    checked. The ``checked`` variable is a dictionary where the keys are is
    the names of fields which can be checked and and values are ``True`` or
    ``False`` depending on whether or not the field should be checked.

In the application code create a ``form`` instance for each form you want to
create, using your ``StandardForm`` as a basis, setting up the four required
variables:

.. sourcecode :: pycon
  
    >>> form = StandardForm(
    ...     value = {
    ...         'firstname': u'James', 
    ...         'surname': u'', 
    ...         'hobbies': [u'1', u'4'],
    ...     },
    ...     error = {
    ...         'surname': u'Please enter a surname',
    ...         'hobbies': u'Please choose from the available options, there is no option 4.',
    ...     },
    ...     option = {
    ...         'hobbies': [
    ...             (u'1', u'Programming'),
    ...             (u'2', u'Swimming'),
    ...             (u'3', u'Reading Fiction Books'),
    ...         ],
    ...         'salutation': [
    ...             (u'0', u'--Please select--'),
    ...             (u'1', u'Mr'),
    ...             (u'2', u'Mrs'),
    ...             (u'3', u'Ms'),
    ...             (u'4', u'Dr'),
    ...         ]
    ...     },
    ...     checked = {
    ...         'agree': False
    ...     }
    ... )

How you generate the values, errors and options is down to your application.
FormConvert can help in the conversion of values from HTTP post data to the
values you need and back again.

Notice that all the valus are Unicode strings. The options are a list of
``(value, label)`` pairs and although the values here are consecutive numbers
represented as strings, you could use and values you like.

Now the ``form`` instance exists you can use it to build a form. Usually this
would be done in a template but the example here uses plain Python. Whilst you
can build the HTML structure yourself and add indivudual fields, here we are
using FormBuild's built-in layout tools:

.. sourcecode :: pycon

    >>> lines = [
    ...     form.start_with_layout(
    ...         '/form/submit.py', 
    ...         table_class='form',
    ...     ),
    ...     form.row('<h2>Personal Details</h2>'),
    ...     form.field(
    ...         label="Salutation",
    ...         type='dropdown',
    ...         name='salutation',
    ...     ),
    ...     form.field(
    ...         label="Firstname",
    ...         type='text', 
    ...         name='firstname',
    ...         required=True,
    ...     ),
    ...     form.field(
    ...         label="Surname",
    ...         type='text', 
    ...         name='surname',
    ...         required=True,
    ...     ),
    ...     form.row('<h2>Hobbies</h2>'),
    ...     form.field(
    ...         label="Hobbies",
    ...         type='checkbox_group', 
    ...         name='hobbies',
    ...         args=dict(align="vert"),
    ...     ),
    ...     form.action_bar(
    ...         form.submit(name='action', value='Submit'),
    ...     ),
    ...     form.end_with_layout(),
    ... ]

Here the ``required=True`` option adds an asterix to the label to show the
user that the field is required, it has nothing to do with validation, it only
affects the interface.

To make the form look prettier you'll probably want to add some CSS styles.
This is a good example:

.. sourcecode :: pycon

    >>> styles = """\
    ...     table.form td.label label {
    ...         font-weight: bold;
    ...         padding-right: 5px;
    ...     }
    ...     table.form .error, table.form span.required {
    ...         font-weight: bold;
    ...         color: #f00;
    ...     }
    ...     table.form span.small {
    ...         font-size: 85%;
    ...         line-height: 77%;
    ...     }
    ...     table.form td.label {
    ...         white-space: no-wrap;
    ...         width: 170px;
    ...     }
    ...     table.form td {
    ...         padding-bottom: 0px;
    ...         margin: 0px;
    ...     }
    ...     table.form td.field_desc {
    ...         padding-bottom: 8px;
    ...     }"""

We are using ``table.form`` in the styles because we specified
``table_class='form'`` in ``form.start_with_layout()``.

You can then put it all together like this:

.. sourcecode :: pycon

    >>> page = [
    ...     '<html>',
    ...     '<head><title>Test Form</title>',
    ...     '<style type="text/css">',
    ...     styles,
    ...     '</style>',
    ...     '</head>',
    ...     '<body><h1>Test Form</h1>',
    ...     '\n'.join(lines),
    ...     '</body>',
    ...     '</html>',
    ... ]
    >>> print '\n'.join(page)
    <html>
    <head><title>Test Form</title>
    <style type="text/css">
        table.form td.label label {
            font-weight: bold;
            padding-right: 5px;
        }
        table.form .error, table.form span.required {
            font-weight: bold;
            color: #f00;
        }
        table.form span.small {
            font-size: 85%;
            line-height: 77%;
        }
        table.form td.label {
            white-space: no-wrap;
            width: 170px;
        }
        table.form td {
            padding-bottom: 0px;
            margin: 0px;
        }
        table.form td.field_desc {
            padding-bottom: 8px;
        }
    </style>
    </head>
    <body><h1>Test Form</h1>
    <form action="/form/submit.py" method="post"><table class="form">
    <tr><td colspan="3"><h2>Personal Details</h2></td></tr>
    <tr class="field">
      <td class="label" valign="top" height="10">
        <span style="visibility: hidden">*</span><label for="salutation">Salutation:</label>
      </td>
      <td class="field" valign="top">
        <select name="salutation">
    <option value="0">--Please select--</option>
    <option value="1">Mr</option>
    <option value="2">Mrs</option>
    <option value="3">Ms</option>
    <option value="4">Dr</option>
    </select>
      </td>
      <td rowspan="2" valign="top"></td>
    </tr>
    <tr class="field">
      <td class="label" valign="top" height="10">
        <span class="required">*</span><label for="firstname">Firstname:</label>
      </td>
      <td class="field" valign="top">
        <input type="text" name="firstname" value="James" />
      </td>
      <td rowspan="2" valign="top"></td>
    </tr>
    <tr class="field">
      <td class="label" valign="top" height="10">
        <span class="required">*</span><label for="surname">Surname:</label>
      </td>
      <td class="field" valign="top">
        <div class="error">Please enter a surname</div>
    <input type="text" name="surname" value="" />
      </td>
      <td rowspan="2" valign="top"></td>
    </tr>
    <tr><td colspan="3"><h2>Hobbies</h2></td></tr>
    <tr class="field">
      <td class="label" valign="top" height="10">
        <span style="visibility: hidden">*</span><label for="hobbies">Hobbies:</label>
      </td>
      <td class="field" valign="top">
        <div class="error">Please choose from the available options, there is no option 4.</div>
    <input type="checkbox" name="hobbies" value="1" checked="checked" /> Programming<br />
    <input type="checkbox" name="hobbies" value="2" /> Swimming<br />
    <input type="checkbox" name="hobbies" value="3" /> Reading Fiction Books<br />
      </td>
      <td rowspan="2" valign="top"></td>
    </tr>
    <tr>
      <td></td>
      <td colspan="2">
        <input type="submit" name="action" value="Submit" />
      </td>
    </tr>
    </table></form>
    </body>
    </html>

Here's how it looks when it is rendered:

.. image :: form1.png

That's it, you've created a reasonably sophisticated form and populated it
with values and error messages.

XXX Using fields directly

XXX Adding in the checkbox to the example.

Layout API
==========

To support common requirements for layouts the FormBuild ``Form`` class has a
``field()`` method which is used like this:

.. sourcecode :: pycon

    ${form.start_with_layout(action="/some/action")}
    ${form.field(
        label='Email',
        field=dict(type='text', name='email', default=''),
        required=True
    )}
    ${form.end_with_layout()}

The ``start_with_layout()`` and ``end_with_layout()`` methods add the
``<form>`` tags as usual but also add the code needed to start and end the HTML
structures generated by the calls to ``field()``. 

There are also ``start_layout()`` and ``end_layout()`` methods which you can
use if you want to separate the generation of the form tags from the generation
of the HTML required for the layout.

The ``field()`` method takes a number of extra arguments to customise variables
such as whether the field is marked as required, the help text to display after
it and any words to appear under the label or the field itself.

Notice that when working with a ``field()`` the arguments which you would
normally pass to the induvidual form method as passed as a dictionary via the
``field`` argument. The ``field()`` method will handle calling the appropriate
method to generate the HTML for the field. As a result of this alternative
calling method you also need to pass the field type as one of the dictionary
arguments. 

Another consequence of calling ``field()`` rather than the form's individual
field methods is that you don't need to specify an error message. Because the
name of the field is passed as one of the values of the dictionary passed via
the ``field`` arguments, the ``field()`` hepler can lookup any error message
and display it accordingly. The same also applies to the field's value. The
``field()`` method can look it up from the arguments used to create the
``form`` object and pass the correct value when it constructs the field from
the field arguments. It is still useful to be able to pass a default value for
a field so the ``field()`` method can also correctly handle a ``default`` key
in the ``field`` argument, using the default if no value is set, otherwise
using the value instead. 

.. note ::

    The old FormBuild used a series of functions for starting and stopping
    various components but in practice the flexibility was not needed. It was
    easier to simply implement an alternative ``field()`` function supporting
    the different layout required. This is the approach you should follow in
    FormBuild 2.

Custom Field Types
==================

It is sometimes useful to be able to create a custom field type. A common
requirement is that a dropdown be populated with possible values from a
database. We might want to implement a custom type of dropdown field which is
capable of performing a database lookup. 

An implementation might look like this:

.. sourcecode :: pycon

    class CustomForm(Form):

        def database_dropdown(table, cursor, **attrs):
            cursor.execute('SELECT value, label FROM %s', table)
	    attrs['options'] = cursor.fecthall()
	    return self.dropdown(**attrs)

The field could then be used like this in the template:

.. sourcecode :: pycon

    form.database_dropdown(table='Color', cursor=cursor, name='color')

In order for this implementation to work the database ``cursor`` object would
have to be availble in the template. It would be much easier if the cursor
could be set when the form was constructed via some sort of state variable.
This is exactly what happens. ``Form`` classes take a ``state`` argument in
addition to their ``values`` and ``errors`` arguments. The ``state`` argument
can contain any state information your induvidual form generation methods might
require. As such it is very similar to the ``state`` argument you might use
with a FormEncode validator. 

Here's how you might construct the ``CustomForm``::

    form = CustomForm(
        values={'email': 'someone@example.com'},
        errors={'email':'example.com is not a valid domain name'}.
        state={'cursor': cursor}
    )

The ``database_dropdown()`` method can then look like this::

    def database_dropdown(table, **attrs):
        self.state['cursor'].execute('SELECT value, label FROM %s', table)
        attrs['options'] = self.state['cursor'].fecthall()
        return self.dropdown(**attrs)

Which means the template code can just concentrate on the arguments which
affect how the field is displayed::

    form.database_dropdown(table='Color', name='color')

The ``state`` argument could also be used to pass a database connection,
reference to a memcahced store, SQLAlchemy session or simply configuration
information.

Pylons/TurboGears/WebHelpers Integration
++++++++++++++++++++++++++++++++++++++++

If you are using Pylons you will want any HTML strings built by FormBuild to
be treated as ``literal()`` objects. To achieve this you can define your own
``LiteralForm`` class as follows:

.. sourcecode :: pycon

    >>> from formbuild import Form
    >>> from webhelpers.html import literal
    >>> 
    >>> class LiteralForm(Form):
    ...     def __getattribute__(self, name):
    ...         if name in [ 
    ...             'value', 
    ...             'option', 
    ...             'error', 
    ...             'checked', 
    ...             'bag', 
    ...             'table_class', 
    ...             'end',
    ...         ]:
    ...             return Form.__getattribute__(self, name) 
    ...         def make_literal(*k, **p):
    ...             return literal(getattr(Form, name)(self, *k, **p))
    ...         return make_literal

This class behaves exactly the same way as the ``Form`` class except that it
returns ``literal()`` objects instead of Unicode strings. 

Here's an example:

.. sourcecode :: pycon

    >>> form = LiteralForm(
    ...     value={'fruit[0].id': '1', 'fruit[1].id': '3'}, 
    ...     option={
    ...         'fruit[*].id': [
    ...             ('1', 'Bananas'), 
    ...             ('2>', 'Apples <>'),
    ...             ('3', 'Pears'),
    ...         ]}
    ... )
    >>> print form.checkbox_group('fruit', sub_name='id')
    <input type="checkbox" name="fruit[0].id" value="1" checked="checked" /> Bananas
    <input type="checkbox" name="fruit[1].id" value="2&gt;" /> Apples &lt;&gt;
    <input type="checkbox" name="fruit[2].id" value="3" checked="checked" /> Pears
    >>> print form.checkbox_group('fruit', sub_name='id', align='vert')
    <input type="checkbox" name="fruit[0].id" value="1" checked="checked" /> Bananas<br />
    <input type="checkbox" name="fruit[1].id" value="2&gt;" /> Apples &lt;&gt;<br />
    <input type="checkbox" name="fruit[2].id" value="3" checked="checked" /> Pears<br />
    >>> result = form.checkbox_group('fruit', sub_name='id', align='table', cols=2)
    >>> print result
    <table border="0" width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td><input type="checkbox" name="fruit[0].id" value="1" checked="checked" /> Bananas</td>
          <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
          <td><input type="checkbox" name="fruit[1].id" value="2&gt;" /> Apples &lt;&gt;</td>
          <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
        </tr>
        <tr>
          <td><input type="checkbox" name="fruit[2].id" value="3" checked="checked" /> Pears</td>
          <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
          <td></td>
          <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
        </tr>
    </table>
    >>> isinstance(
    ...     result,
    ...     literal,
    ... )
    True

ToDo
++++

* Find a way to maintain attribute order, perhaps with `odict <http://www.voidspace.org.uk/python/odict.html>`_
* Document ``sub_name`` here as well as in the FormConvert documentation
* Link to http://www.w3schools.com/TAGS/tag_form.asp

