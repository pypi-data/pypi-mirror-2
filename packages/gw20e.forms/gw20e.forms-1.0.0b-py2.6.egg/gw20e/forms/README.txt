##############################################################################
#
# gw20e.forms
#
# To run this README as doctest, do:
#   python -c 'import doctest;doctest.testfile("README.txt")'
# Make sure to put the rootdir for this package on your PYTHONPATH
# if you wish to run the tests standalone.
#
##############################################################################

Contents
========
0. Intro
1. Core concepts
2. Code


0. Intro
========

This package holds an alternative to plone/zope forms. The package is
loosely based on XForms concepts (and Socrates QE). The package is an
alternative for the standard packages like plone.app.forms and
zope.forms, and aims to be slightly more understandable and useable.

The API is set up as a classic API, not using too much adapting and
lookup. This makes creating forms into something you do programmatically,
although one of the aims is to add XML support so as you can read in xml
definitions of forms.


1. Core concepts
================

The core concepts are as follows (so you can quickly decide whether
you like this approach or not):

A form is a container for/composition of three things:

1. data
2. model
3. view


1.1 Data
========

The data holds the variables you wish to collect with this form. A
variable simply has an id, and if you like a default value.  


1.2 Model
=========

The model holds all properties for a given form, like readonly-ness,
requiredness, datatyping for variables, relevance, etc. All these
properties are calculated from expressions, in this case Python
expressions, so requiredness is not just true or false, it can be
calculated based on an expression that can include other
variables. All variables from the form data are available in
expressions via the 'data' dict, so if variable 'foo' would be
required if variable 'bar' was set to 666, can be expressed like so:

 ... required="data['bar'] == 666" ...

In general, all expressions are eval-ed to something true or
false. The model offers the following properties:

* requiredness: is a variable required or not?
* relevance: is the variable relevant? Like maiden name would be irrelevant
  when gender is male. In general, the related control/widget for irrelevant 
  variables would not be shown.
* readonly: can a person change the value of a variable?
* calculate: in stead of letting a person set the value of a variable, the
  variable is calculated.
* datatype: datatype for the variable, like int, string, or more complex
  variables.

Properties are bound to variables by a bind attribute. A set of
properties can be bound to a series of variables.


1.3 View
========

The view (or FormView) is the actual visible part of the form. The
view can be rendered and holds a collection of widgets or controls,
that are bound to variables. More than one control can bind to the
same variable. Controls can be grouped in layout groups, like flow
layout or card layout (tabs).

In label and hint texts of controls you can use lexical values of
variables by using the expression ${<var name>}. This way you can refer to
values given in other variables from your labels and hints.


2. Code
=======

Ok, enough theory, let's do something for real.

A form is produced by a FormFactory: this should take care of
producing a form holding the necessary stuff.

Let's create a formfactory, to start with, but first import:

      >>> import sys
      >>> from interfaces import *
      >>> from zope.interface import implements
      >>> from formdata import FormData
      >>> from formview import FormView
      >>> from formmodel import FormModel
      >>> from data.field import Field
      >>> from model.fieldproperties import FieldProperties
      >>> from rendering.control import Input, Select, Option
      >>> from form import Form, FormValidationError
      >>> from rendering.html.renderer import HTMLRenderer

Now let us create a factory class

      >>> class FormFactory():
      ...   implements(IFormFactory)
      ...   def createForm(self):
      ...     data = FormData()
      ...     data.addField(Field("field0"))
      ...     data.addField(Field("field1", "foo"))
      ...     data.addField(Field("field2", "bar"))
      ...     data.addField(Field("field3"))
      ...     view = FormView()
      ...     view.addRenderable(Input("input0", "field0", label="First name"))
      ...     view.addRenderable(Input("input1", "field1", label="Last name"))
      ...     view.addRenderable(Select("select0", "field3", label="Select me!", options=[], with_empty=True))
      ...     model = FormModel()
      ...     model.addFieldProperties(FieldProperties("prop0", ["field0"], required="True"))
      ...     model.addFieldProperties(FieldProperties("prop1", ["field1", "field2"], relevant="data['field0']"))
      ...     return Form("test", data, model, view, None)

      >>> ff = FormFactory()
      >>> form = ff.createForm()
      >>> print len(form.data.getFields())
      4

      >>> props = form.model.getFieldProperties("field0")
      >>> props[0].id
      'prop0'

      >>> len(props)
      1

      >>> field0 = form.data.getField("field0")
      >>> field0.id
      'field0'

      >>> field0.value

In the meanwhile, field1 and field2 should be irrelevant, given that field0
has no value

      >>> form.model.isRelevant("field1", form.data)
      False
      >>> form.model.isRelevant("field2", form.data)
      False

      >>> try:
      ...   form.validate()
      ... except FormValidationError:
      ...   print sys.exc_info()[1].errors['field0']
      ['required']

      >>> form.data.getField("field0").value = "pipo"
      >>> form.validate()
      True

      >>> field0.value
      'pipo'

By now, field1 and field2 should also be relevant

      >>> form.model.isRelevant("field1", form.data)
      True
      >>> form.model.isRelevant("field2", form.data)
      True

Now for some display parts. An irrelevant control should not have a class
'relevant', otherwise it should have it...

      >>> form.data.getField('field0').value = None
      >>> field = form.view.getRenderable('input1')
      >>> renderer = HTMLRenderer()
      >>> renderer.render(form, field, sys.stdout)
      <div id="input1" class="control input ">
      <label for="input-input1">Last name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input1" type="text" name="input1" value="foo" size="20"/>
      </div>

      >>> form.data.getField('field0').value = 'pipo'
      >>> field = form.view.getRenderable('input1')
      >>> renderer = HTMLRenderer()
      >>> renderer.render(form, field, sys.stdout)
      <div id="input1" class="control input relevant">
      <label for="input-input1">Last name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input1" type="text" name="input1" value="foo" size="20"/>
      </div>

      >>> field = form.view.getRenderable('input0')
      >>> renderer.render(form, field, sys.stdout)
      <div id="input0" class="control input relevant required">
      <label for="input-input0">First name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input0" type="text" name="input0" value="pipo" size="20"/>
      </div>
      
How 'bout those extra classes...

      >>> renderer.render(form, field, sys.stdout, extra_classes="card")
      <div id="input0" class="control input card relevant required">
      <label for="input-input0">First name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input0" type="text" name="input0" value="pipo" size="20"/>
      </div>

      >>> select = form.view.getRenderable('select0')
      >>> renderer.render(form, select, sys.stdout)
      <div id="select0" class="control select relevant">
      <label for="input-select0">Select me!</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <select id="input-select0" name="select0"  size="1">
      <option value="" >Maak een keuze</option>
      </select>
      </div>

Well, this is all very simple, and it is quite likely that you would
wish for something a bit more usefull. All parts of the form are there
to be extended. Take for instance the FormView. A developer (or end
user) should be able to:

 * create a full HTML form;
 * use a generated HTML form (this is wat the base implementation does);
 * create a PDF form.

The factory is also an important part of the form process. A factory
can be imagined to be one of the following:

 * produced from a Schema (content type);
 * produced from an XML definition, for example an XForms instance from
   OpenOffice.

Forms in general should be:

 * submitable to a range of handlers, like email, database storage,
   content type storage;
 * easy to validate 'live;
 * enable multi-page.

More detailed tests:

We'd like to check whether lookup of a control by bind works, so as to
be able to process values into lexical values. This is especially
interesting when using selects: we'd expect to see the label not the
value in lexical space.

      >>> data = FormData()
      >>> data.addField(Field("f0", "opt0"))
      >>> view = FormView()
      >>> opts = [Option("opt0", "Option 0"), Option("opt1", "Option 1")]
      >>> view.addRenderable(Select("sel0", "f0", "Select 0", options=opts))
      >>> ctl = view.getRenderableByBind("f0")
      >>> ctl.lexVal("opt0")
      'Option 0'


Can we use variable substitution in labels and hints? Yes, we can!

      >>> data = FormData()
      >>> data.addField(Field("f0", "Pipo"))
      >>> data.addField(Field("f1"))
      >>> view = FormView()
      >>> view.addRenderable(Input("in0", "f0", label="First name"))
      >>> view.addRenderable(Input("in1", "f1", label="Last name for ${f0}"))
      >>> model = FormModel()
      >>> form = Form("test", data, model, view, None)
      >>> renderer = HTMLRenderer()
      >>> field = form.view.getRenderable('in1')
      >>> renderer.render(form, field, sys.stdout)
      <div id="in1" class="control input relevant">
      <label for="input-in1">Last name for Pipo</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-in1" type="text" name="in1" value="" size="20"/>
      </div>

Let's delve into input processing a bit...
A simple input should just return it's own value

  >>> data = {'pipo': 'lala'}
  >>> ctl = Input("pipo", "f0", "Some input")
  >>> ctl.processInput(data)
  'lala'
