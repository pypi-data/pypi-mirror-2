FormBuild
+++++++++

.. py:module :: formbuild
.. contents ::

Every application is different and so is every form. If you use a form
framework you'll quickly hit its limitations and find yourself spending a long
time working against the framework to try to make the customisations your
application needs. If you code all your forms by hand you'll find yourself
writing the same boilerplate code again and again.

FormBuild sits between these two extremes doing the most it can without getting
in your way. It integrates closely with ConversionKit for validation but does
not rely on it, instead prefering loose coupling so that you could instead 
use FormEncode, Schemaish, Flatland or your own custom validation code.

FormBuild had two main classes: ``Field`` and ``Form``. The former helps you
generate HTML for form fields from data structures representing values, options
and checked checkboxes, the latter helps you build forms with labelled fields
and fieldsets. Most of the time you will use a ``Form`` but since ``Form``
inherits from ``Field`` you can always use the lower-level ``Field`` methods
when you need to or even drop to pure HTML for very tricky cases. In this 
documentation we'll look at how to generate fields first and then look at 
constructing forms.

The idea is that you specify all values, options and checked checkboxes in your
controller code and then call methods of the ``Form`` or ``Field`` instance in
your template to choose where and how they are rendered. This way coders never
need to worry about the design of the form and designers never need to worry
about the values that will be set.

Installation
============

FormBuild is a standard setuptools package. Its latest version is always
available from http://pypi.python.org/pypi/FormBuild/ and the source repository
is available from https://hg.3aims.com/public/FormBuild.

You can install the latest version like this:

::

    pip install FormBuild

If you don't have the ``pip`` command you can use ``easy_install``:

::

    easy_install FormBuild

If you have neither ``pip`` nor ``easy_install`` you should install ``pip``. On Debian-based systems:

::

    sudo apt-get install python-pip

Or you can set up a virtual environment with ``pip`` in it:

::

    wget http://pylonsbook.com/virtualenv.py
    python virtualenv env
    . env/bin/activate
    easy_install pip
    pip install FormBuild

Getting Started
===============

Working with Fields
-------------------

In FormBuild the same ``Field`` instance is used to render many diferent
fields. You can import and set up your ``Field`` instance like this:

.. sourcecode :: pycon

    >>> from formbuild import Field
    >>> value = {u'firstname': u'James'}
    >>> field = Field(value)

The ``value`` passed to the ``Field`` object is a dictionary where the keys are
the names of the fields you will render and the values are the values of those
fields. In this case we have one field with a name ``u'firstname'`` and a value
``u'James'``. But in most examples your ``value`` dictionary will have a key
value pair for each field you want to render. Both the field names and their
corresponding values *must* be Unicode (or more specifically, derived from
Python's builtin ``unicode`` type).

The above code would usually go in your controller, then in your template you
will decide the type of field to use to display the ``firstname`` by calling
one of the methods of the ``field`` instance. Let's start by rendering it as a
text field:

.. sourcecode :: pycon

    >>> print field.text('firstname')
    <input type="text" name="firstname" value="James" />

The ``text()`` method looks up the value of the ``firstname`` field and returns
the HTML for an input field of type text. Notice that the value ``James`` has
been set.

Here's how the field looks when it is rendered as a text field:

.. raw :: html

    <input type="text" name="firstname" value="James" />

Because the construction of the values is separate from the rendering of the
field, the designer working with your template can easily choose to have the
``firstname`` field displayed by a different type of field. Let's see the same
field rendered in a variety of different ways.

First as a textarea:

.. sourcecode :: pycon

    >>> print field.textarea('firstname')
    <textarea name="firstname">James</textarea>

Here's how the field looks when it is rendered as a textarea field:

.. raw :: html

    <textarea name="firstname">James</textarea>

Now let's render it as a hidden field:

.. sourcecode :: pycon

    >>> print field.hidden('firstname')
    <input type="hidden" name="firstname" value="James" />

You'll see later when we look at working with forms rather than fields that you
can also set hidden fields in the ``action_bar()`` method.

Finally here is the firstname value rendered as a password field:

.. sourcecode :: pycon

    >>> print field.password('firstname')
    <input type="password" name="firstname" value="James" />

Here it is as HTML:

.. raw :: html

    <input type="password" name="firstname" value="James" />

It is often considered bad practice to re-populate password fields so the
``password()`` method also takes a ``populate`` argument which can be set in
the template to emsure the password is not populated, even if a value was set
when the ``field`` object was created. It is used like this:

.. sourcecode :: pycon

    >>> print field.password('firstname', populate=False)
    <input type="password" name="firstname" value="" />

Here it is as HTML without the password populated:

.. raw :: html

    <input type="password" name="firstname" value="" />

In real examples you will want to use the ``field`` object to render lot's of
fields, not just to render a single one. Here's a more typical example:

.. sourcecode :: pycon

    >>> from formbuild import Field
    >>> value = {
    ...     u'firstname': u'James',
    ...     u'lastname': u'James',
    ...     u'email': u'james@example.com',
    ...     u'profile': u'I like climbing, sailing, running and scuba diving',
    ... }
    >>> field = Field(value)

Then in your template:

.. sourcecode :: pycon

    >>> print "Firstname: ", field.text(u'firstname'), '\n', \
    ...       "Surname: ", field.text(u'surname'), '\n' \
    ...       "Email: ", field.text(u'email'), '\n' \
    ...       "Profile: ", field.textarea(u'profile')
    Firstname:  <input type="text" name="firstname" value="James" /> 
    Surname:  <input type="text" name="surname" /> 
    Email:  <input type="text" name="email" value="james@example.com" /> 
    Profile:  <textarea name="profile">I like climbing, sailing, running and scuba diving</textarea>


Custom Attributes
-----------------

Quite frequently you may find yourself wanting to set extra attributes on a field. All fields take a
``attribute`` argument which is a dictionary of extra HTML attributes you
would like added to a field. For example it is common to set an ``id`` or a
``class`` attribute. Here's an example of how to use the ``attributes`` argument:

.. sourcecode :: pycon

    >>> from formbuild import Field, OrderedDict
    >>> field = Field({u'firstname': u'James'})
    >>> print field.textarea('firstname', attributes=OrderedDict([(u'id', u'form_firstname'), (u'class', u'fields')]))
    <textarea id="form_firstname" class="fields" name="firstname">James</textarea>

The keys of the dictionary passed as the ``attributes`` parameter should be
Unicode and the values should either be Unicode, integers or long.

One useful HTML tip is that you can set multiple classes on the same element by
having their names separated by a space. You can use the same tip when
specifying attributes:

.. sourcecode :: pycon

    >>> print field.textarea('firstname', attributes={u'class': u'one two'})
    <textarea class="one two" name="firstname">James</textarea>

The order of attributes is not preserved when you use a normal Python
dictionary like this.  If you need the order to be preserved you will need to
use an ``OrderedDict``.  On Pythom 2.7 and above this is just
``collections.OrderedDict``, on earlier versions FormBuild provides its own
implementation:

.. sourcecode :: pycon

    >>> from formbuild import OrderedDict
    >>> print field.textarea('firstname', attributes=OrderedDict([(u'id', u'form_firstname'), (u'class', u'fields')]))
    <textarea id="form_firstname" class="fields" name="firstname">James</textarea>

.. caution::

    Depending on your preferences you might prefer to create dictionaries like this:
    
    :: 
    
        field.textarea('firstname', attribute=dict(id=form_firstname', class='fields'))

    This would work for some attribute names but note that ``class`` is a reserved word in
    Python so this would give an error. Also, in older versions of Python the keys of this
    dictionary would be not be treated as unicode values, so this would also give an error.

.. tip ::

   It used to also be common to add attributes for JavaScript events such as
   ``onchange`` or ``onblur`` to forms but best practice is now to set an ID on
   the field element and attach event handlers to the form unobtrusively using the
   ID. See XXX for more information.

Cross-Site Scripting (XSS) Attacks and MarkupSafe
-------------------------------------------------

There are two ways the ``Field`` class can treat the values you pass it:

* As a raw string which needs escaping eg ``James & David's Party``.
* As properly escaped HTML ready to be copied straight into the appropriate 
  part of an HTML field e.g. ``James &amp; David&#39;s Party``

It is important to get the escaping of values correct, otherwise a visitor to
your site could accidentally add HTML values to a string they enter and when
their string is displayed in the form it could break your HTML. Worse, if a
malicous user visited your site and spent some time carefully crafting an
appropirate HTML string, they could actually change the HTML in your page to
behave differently, perhaps taking users to a different page or stealing
information. This is known as a cross-site scripting attack or an XSS attack so
it is important FormBuild handles values it recieves safely.

FormBuild decides whether or not your string value needs escaping by looking at
its *type*. If it is a ``unicode`` type, FormBuild will escape it for you. If
it is built with a special object called ``Markup``, FormBuild will assume it
is already escaped. The ``Markup`` object comes from ``markupsafe`` and is
rapidly becoming the standard in Python for marking escaped HTML.

Here's an example representing a form for an event:

.. sourcecode :: pycon

    >>> from markupsafe import Markup
    >>> from formbuild import Field
    >>> field = Field({
    ...     u'title': Markup(u"James &amp; David&#39;s Party"),
    ...     u'place': u"The King's Arms",
    ... })

Notice that the title contains escaped HTML and has been marked as escaped by
making it a ``Markup`` object but that the place hasn't.

Let's see how FormBuild treats the different objects:

.. sourcecode :: pycon

    >>> print field.text(u'title')
    <input type="text" name="title" value="James &amp; David&#39;s Party" />
    >>> print field.text(u'place')
    <input type="text" name="place" value="The King&#39;s Arms" />

As you can see, the place had its ``'`` character escaped but the title didn't
have any of the ``&`` characters escaped because FormBuild knew it was a Markup
object that was already escpaed.

.. caution ::

   If you are not thinking what you are doing it is very easy to accidentally
   wrap un-escaped HTML in a ``Markup`` object. Particularly if a value is coming
   from say a database and isn't written explicitly in your code. If you do this
   FormBuild will assume you have already properly escaped the HTML and not escape
   it again. This could then re-introduce a XSS attack vector into your form so
   never wrap anything in a ``Markup`` object unless you are 100% sure the value
   didn't originate from user input anywhere.

   Here's an example of what happens if you forget this:

   .. sourcecode :: pycon
   
       >>> title_from_database = u"James & David's Party"
       >>> field = Field(
       ...     {u'title': Markup(title_from_database)}, # CAUTION: Don't do this!
       ... )
       >>> print field.text(u'title')
       <input type="text" name="title" value="James & David's Party" />

   Notice that the value is unescaped (the ``&`` and ``'`` have not been
   changed), so a malicious user could once again add HTML and JavaScript to
   your page to do evil things.

The strings returned by the FormBuild methods are ``Markup`` instances
themselves since they are already properly escaped. This is only useful if your
templating language is aware of how to treat ``Markup`` objects. If it isn't
look what happens:

.. sourcecode :: pycon

    >>> field = Field({
    ...     u'title': u"James & David's Party",
    ... })
    >>> print u'<form>' + field.text(u'title') + u'</form>'
    &lt;form&gt;<input type="text" name="title" value="James &amp; David&#39;s Party" />&lt;/form&gt;

Because ``field.text(u'title')`` returned a ``Markup`` object, the unicode
strings either side representing HTML were accidentally escaped before the
string was printed. This clearly isn't what you intended.

If this happens with your templating language, you will
need to convert the ``Markup`` object back to a normal ``unicode`` type before
concatentating other strings with it:

.. sourcecode :: pycon

    >>> print u'<form>' + unicode(field.text(u'title')) + u'</form>'
    <form><input type="text" name="title" value="James &amp; David&#39;s Party" /></form>


Luckily most modern templating languages like Mako and Jinja2 support the
``Markup`` object so this step isn't needed. XXX Is this true?

You can also use ``Markup`` for attributes since the same escaping problems
occur. Here's an example where both of the attribute values need escaping but
one is specified with ``Markup`` and the other isn't:

.. sourcecode :: pycon

    >>> from formbuild import Field
    >>> field = Field({u'firstname': u'James'})
    >>> print field.textarea('firstname', attributes=OrderedDict([(u'one', Markup('1 &amp; 2')), (u'two', u'1 & 2')]))
    <textarea one="1 &amp; 2" two="1 &amp; 2" name="firstname">James</textarea>

Once again, the Markup attribute value isn't changed whereas the unicode one is
escaped.

HTML vs XHTML
-------------

By default FormBuild generates XHTML-compatible markup. This means it closes
fields that use a single markup element with ``/>`` rather than ``>``. You can
change this behaviour by passing the ``Field`` class a different ``html``
argument. Your choices are:

* ``formbuild.XHTMLBuilder``
* ``formbuild.HTMLBuilder``

You can also write your own builder if you prefer.

Here's an example where we use the ``HTMLBuilder`` instead of the default
``XHTMLBuilder``:

.. sourcecode :: pycon

    >>> from formbuild import Field, HTMLBuilder
    >>> field = Field(
    ...     {
    ...         u'title': Markup(u"James &amp; David&#39;s Party"),
    ...         u'place': u"The King's Arms",
    ...     },
    ...     builder=HTMLBuilder(),
    ... )
    >>> print field.text(u'title')
    <input type="text" name="title" value="James &amp; David&#39;s Party">

Notice this time that the input field is closed with ``>`` rather than ``/>``
since we are using the HTML builder.

XXX Thte ``TableForm`` class currently doesn't use the builder.

Validating Sets of Fields
-------------------------

Before we look at other field types, let's see how to validate form submissions
for simple forms. Rather than looking at the way each framework deals with
getting data from a POST submission into a format you can use, I'll assume
you've already done the work to convert it to a dictionary of Unicode values,
ready to use. See the separate FormConvert module for examples of how to do
this for Python's ``cgi.FieldStorage`` and the Pylons/Pyramid/TurboGears
``webob.Request``.

Let's imagine you wanted a form for the even above. You might render an empty version like this:

.. sourcecode :: pycon

    >>> from formbuild import Field, HTMLBuilder
    >>> field = Field()
    >>> print Markup(u'<form action="." method="post">\nTitle: %s\nPlace: %s\n<input name="submit" value="Submit" type="submit" />\n</form>')%(
    ...     field.text(u'title'),
    ...     field.text(u'place'),
    ... )
    <form action="." method="post">
    Title: <input type="text" name="title" />
    Place: <input type="text" name="place" />
    <input name="submit" value="Submit" type="submit" />
    </form>


Once the form is submitted and converted you will end up with a dictionary like this:

.. sourcecode :: pycon

    >>> post = {u'title': u"James and David's Party", u'place': u'London', u'submit': u'Submit'}

Let's see how to validate it and convert it with ConversionKit:

.. sourcecode :: pycon

    >>> from conversionkit import Conversion, toDict
    >>> from stringconvert import unicodeToUnicode
    >>> 
    >>> form_to_event = toDict(
    ...     converters = dict(
    ...         title=unicodeToUnicode(),
    ...         place=unicodeToUnicode(),
    ...     )
    ... )
    >>>
    >>> conversion = Conversion(post).perform(form_to_event)
    >>> if conversion.successful:
    ...     print "Success:", conversion.result
    ... else:
    ...     print "Error summary:", conversion.error
    Success: {u'place': u'London', u'title': u"James and David's Party"}

By default ``toDict`` removes keys from the post dictionary which do not have
corresponding converters specified. This means the submit button is stripped
from the conversion result without being validated. This is usually what you
want. There are occasions when a missing field is a problem though. For
example, if a value for the ``place`` field wasn't submitted because the field
wasn't present in the form, that would indicate there had been a problem. We
can validate this using the ``missing_errors`` key to ``toDict`` like this:

.. sourcecode :: pycon

    >>> form_to_event = toDict(
    ...     converters = dict(
    ...         title=unicodeToUnicode(),
    ...         place=unicodeToUnicode(),
    ...     ), 
    ...     missing_errors = dict(
    ...         place=u'No place field was submitted'
    ...     ),
    ... )

Individual converters are only run if there is a value for them. In this case
if the place field was present in the form, but the user hadn't completed it, a
value of ``u''`` would be present in the post dict for the ``place`` key. This
value would then be present in the results unvalidated.

To specify that empty values are not allowed you must set an error or a
default. Let's make the default place ``London`` but require that the ``title``
is not empty:

.. sourcecode :: pycon

    >>> form_to_event = toDict(
    ...     converters = dict(
    ...         title=unicodeToUnicode(),
    ...         place=unicodeToUnicode(),
    ...     ), 
    ...     missing_errors = dict(
    ...         title=u'No title field was submitted',
    ...         place=u'No place field was submitted',
    ...     ),
    ...     empty_errors = dict(
    ...         title=u'Please enter a title',
    ...     ),
    ...     empty_defaults = dict(
    ...         place=u'London',
    ...     ),
    ... )

Many validation and conversion libraries treat missing and empty conditions in
the same way. ConversionKit treats them each explicitly although you can use
the combined ``missing_or_empty_error`` and ``missing_or_empty_default``
options if you are feeling lazy.

If you have quite a complex form, with a variety of different errors and
defaults for each field, it can be easier to specify the errors and defaults
with the converter for the field. You can do so like this:

.. sourcecode :: pycon

    >>> from conversionkit import Field
    >>> form_to_event = toDict(
    ...     converters = dict(
    ...         title=Field(
    ...             unicodeToUnicode(),
    ...             missing_error = u'No title field was submitted',
    ...             empty_error = u'Please enter a title',
    ...         ),
    ...         place=Field(
    ...             unicodeToUnicode(),
    ...             missing_error = u'No place field was submitted',
    ...             empty_default = u'London',
    ...         ), 
    ...     ),
    ... )

If an error had occurred you can also have obtained more detailed errors like this:

.. sourcecode :: pycon

    >>> invalid_post = {u'place': u'London', u'submit': u'Submit'}
    >>> conversion = Conversion(invalid_post).perform(form_to_event)
    >>> print "Error summary:", conversion.error
    Error summary: The 'title' field is invalid
    >>> from nestedrecord import encode_error
    >>> print "All errors:", encode_error(conversion)
    All errors: {u'title': u'No title field was submitted'}

See the ConversionKit documentation for full information about how
ConversionKit works, see FormConvert for a set of converters that are useful
for working in the context of HTML form submissions.

You'll learn more about how to cope with errors when we look at the ``Form``
object rather than just looking at fields.

Commonly Used Fields
====================

Input fields and textareas
--------------------------

You've already seen the input fields and textareas in examples so far. Here is
their API documentation:

.. autoclass:: Field
   :members: text, password, hidden, textarea

Single Radio buttons and Checkboxes
-----------------------------------

.. autoclass:: Field
   :members: radio, checkbox

Image and Submit Buttons
------------------------

There are two types of field in FormBuild that are not really designed to have
dynamic data values set in the controller. These are image and a submit button.
In a normal use case the value of the field will be chosen by the designer when
they create the form. ``image_button()`` and ``submit()`` fields therefore take
a ``value`` argument so that you can set the value as you create the field in
the template. They *do not* get populated from a ``value`` dictionary passed to
``Field`` the way other fields do. Here are their specifications:

.. autoclass:: Field
   :members: image_button, submit

.. tip :: 

   When you are using a ``TableForm`` you can specify a set of image or submit
   buttons in the ``action_bar()`` method.

Static Field
------------

Sometimes it is useful to have a field that appears to be read-only.

.. autoclass:: Field
   :members: static

Date Field
-----------

Date fields are a little more complicated than ordinary fields in that you
usually want to add a JavaScript date picker to them to ensure that a user can
easily choose the correct date. As usual FormBuild doesn't provide any JavaScript
integration, instead I'll show you how you can integrate whatever JavaScript
you want yourself.

For this example we'll use jQuery UI. Google host the libraries we need so 
we'll link to Google's versions directly.

First in the head of the page, or right at the foot of the body, add this to import the JavaScript and CSS you'll need:

.. sourcecode :: html

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.5/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="http://jqueryui.com/themes/base/jquery.ui.all.css">

.. raw :: html

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.5/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="http://jqueryui.com/themes/base/jquery.ui.all.css">

(You can actually insert it in the body where you render the field if you
prefer but this isn't considered such good practice.)

Then add the JavaScript for your field:

.. sourcecode :: html

    <script>
        $(function() {
            $("#date_in").datepicker({dateFormat: 'yy-mm-dd'});
        });
    </script>

.. raw :: html

    <script>
        $(function() {
            $("#date_in").datepicker({dateFormat: 'yy-mm-dd'});
        });
    </script>

This tells jQuery to look for a field with the ID ``date_in`` and add a jQuery
UI date picker to it. Notice that I've chosen a non-standard date format to
demonstrate that both jQuery UI and conversionkit can cope with a range of date
formats.

Let's make a text field that can be used for that purpose. To do so we'll need
to specify a size and maxlength of 8 characters and ensure the ID of the field
is set to ``date_in``. We'll do this with the ``attributes`` argument:

.. sourcecode :: html

    >>> from formbuild import Field
    >>> field = Field({u'date_in': u'11-01-13'})
    >>> print field.text('date_in', attributes={u'id': u'date_in', u'size': 8, u'maxlength': 8})
    <input maxlength="8" id="date_in" size="8" type="text" name="date_in" value="11-01-13" />

Here's a working example:

.. raw :: html

    <input name="date_in" value="11-01-13" maxlength="8" type="text" id="date_in" size="8" />

To validate a date field you can use ``stringconvert.unicodeToDate`` like this
as one of the converters in ``toDict()``:

.. sourcecode :: pycon

    >>> from stringconvert import unicodeToDate
    >>> converter = toDict(
    ...     converters = dict(
    ...         date_in = unicodeToDate(u'%y-%m-%d'),
    ...     )
    ... )

Here's an example:

.. sourcecode :: pycon

    >>> Conversion({u'date_in': u'11-01-13', u'submit': u'Submit'}).perform(converter).result
    {u'date_in': datetime.date(2011, 1, 13)}

Single Value Autocomplete Field
-------------------------------

When you want the user to select one value from many possible choices you can
use an autocomplete field. In this example we'll use jQuery UI again because it
has a fairly flexible implementation.

Once again you'll need to add the CSS and JavaScript you'll need:

.. sourcecode :: html

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.5/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="http://jqueryui.com/themes/base/jquery.ui.all.css">

Then you can add the JavaScript to turn an ordinary text field into an
autocomplete field. Replace ``/url/where/jquery/can/lookup/input`` with the URL
jQuery can make its calls to.

.. sourcecode :: html

    <script>
        $(function() {
            $("#site").autocomplete({
                source: "/url/where/jquery/can/lookup/input",
                minLength: 2,
            });
        });
    </script>

.. raw :: html

    <script>
        $(function() {
            $("#site").autocomplete({
                source: "/url/where/jquery/can/lookup/input",
                minLength: 2,
            });
        });
    </script>

Now let's create the HTML for the field. We've chosen a size of 50 because its
often helpful for autocomplete fields to be quite long:

.. sourcecode :: html

    >>> from formbuild import Field
    >>> field = Field({u'site': u''})
    >>> print field.text('site', attributes={u'id': u'site', u'size': 50})
    <input id="site" size="50" type="text" name="site" value="" />

.. raw :: html

    <input id="site" size="50" type="text" name="site" value="" />

Finally you'll need to code the action that returns the autocomplete data from
jQuery. The way you would do this depends on your framework, here's some
pseudo-code which should give you an idea of what you would neeed to write:

.. sourcecode :: python

    def autocomplete():
        term = query.getfirst('term')
        rows = database.query(
            '''
            SELECT 
                name 
            FROM site
            WHERE name ilike(%s)
            ORDER BY name DESC
            ''',
            ('%'+term+'%',),
            format='list',
        )
        response.add_header(name='Content-type', value='application/javascript; charset=utf-8')
        return json.dumps([row[0] for row in rows])

To validate 



.. tip ::

   See also the ``dropdown()`` method and the ``checkbox_group()`` method which
   provide other ways of dealing with the types of data structres an autocomplete
   field can be used with.

SQL-backed Single Autocomplete Field
------------------------------------

The single and multi-valued autocomplete fields so far 

Multi Value Autocomplete Field
------------------------------

You can also use very similar code to the single value autocomplete field to
create a multi-value autocomplete field. All that changes is the JavaScript.


Working with Forms
==================

So far we've concentrated on how to render fields. In most real-world applications you will also want a way to:

* Add a label next to each field
* Show any error messages associated with a user entering an invalid value into a form
* group related sets of fields together

These tasks are all achived with a ``Form`` instance. A ``Form`` instance
derives from ``Field`` and has all the same methods. This means that all the
examples you've seen so far using ``Field`` would also have worked with a
``Form`` instance.

The ``Form`` constructor takes two extra arguments compared with ``Fields``,
they are:


Field within Forms
-------------------

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

Introducing Fieldets
---------------------

Displaying Errors
-----------------

Cross Site Request Forgery (CSRF) Attacks
-----------------------------------------

Customising Layouts
-------------------

Start by creating your own form class from ``StandardForm``:

.. sourcecode :: pycon

    >>> from formbuild import Form
    >>> 
    >>> class StandardForm(Form):
    ...    pass
    >>>
    >>> form = StandardForm()

All your forms can now be built with ``StandardForm`` which means that if you
ever need to customise the look and feel or behaviour of all your forms, you
can do so in one place by customising your project's ``StandardForm`` class.


Table Layouts
-------------

In the application code create a ``form`` instance for each form you want to
create, using your ``StandardForm`` as a basis, setting up the four required
variables:

.. sourcecode :: pycon
  
    >>> from formbuild import TableForm
    >>> form = TableForm(
    ...     value = {
    ...         'firstname': u'James', 
    ...         'surname': u'', 
    ...     },
    ...     error = {
    ...         'surname': u'Please enter a surname',
    ...     },
    ...     option = {
    ...         'salutation': [
    ...             dict(id=u'0', label=u'--Please select--'),
    ...             dict(id=u'1', label=u'Mr'),
    ...             dict(id=u'2', label=u'Mrs'),
    ...             dict(id=u'3', label=u'Ms'),
    ...             dict(id=u'4', label=u'Dr'),
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


A Typical Workflow
------------------



Advanced FormBuild
==================

File Field
-----------

Set the enctype to multipart, method to post.

Nested list Of Records Model (NORM)
-----------------------------------

Select Dropdowns and Radio Button Groups
----------------------------------------

In the same way that ``Field`` can treat values as either being strings that
need escaping or HTML values, it can also treat the option IDs and labels as
being strings that need escaping or HTML values.

.. autoclass:: Field
   :members: dropdown, radio_group

Select Combo and Checkbox Group Fields
--------------------------------------

.. autoclass:: Field
   :members: combo, checkbox_group

Repeating Fields
----------------

Examples and Tests
==================

FormBuild comes with a simple test suite and a simple example. To run the
example or tests you'll need to download and extract the source distribution of
FormBuild from one of the locations specified in `Installation`_. 

You can run the tests like this:

::

    cd /path/to/FormBuild/tests
    python doc.py

If you see no output, the tests have passed.

You can run the example like this:

::

    cd /path/to/FormBuild/example
    python census.py

This will output various information from the program. An example of the output
can be found in ``/path/to/FormBuild/example/census_expected_output.txt``.

History
=======

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


