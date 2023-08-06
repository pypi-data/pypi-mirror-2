Contents
========
1. General use
2. XML implementation

1. General use
--------------

The pyramid package provides a simple means of using gw20e.forms for pyramid
apps. The package provides a specific 'file' field for pyramid, to enable
extracting filename and contents from a file in a POST/GET request, and a base
view.

Would you wish to use gw20e.forms, then:

 * add gw20e.forms to the eggs dependencies of your app (duh...)

 * for the view that you wish to show the actual form, override
   gw20e.forms.pyramid.pyramidformview. Let's do some imports
   first. Please note that it is more convenient to use the XML
   implementation, as shown later on. Also, if you insist on using the
   Pythonic implementation, it is better to make a factory create the
   form, so you can just call the factory from your view. Anyway,
   let's go for the not-so-smart way:

      >>> from gw20e.forms.form import Form
      >>> from gw20e.forms.formdata import FormData
      >>> from gw20e.forms.formmodel import FormModel
      >>> from gw20e.forms.formview import FormView
      >>> from gw20e.forms.submission.attrstorage import AttrStorage
      >>> from gw20e.forms.data.field import Field
      >>> from gw20e.forms.rendering.control import Input
      >>> from gw20e.forms.pyramid.formview import formview as pyramidformview
      
   Phew, that was a load of imports. Now do the actual view
   class. It's a pretty simple form, but you should get the picture.

      >>> class yourformview(pyramidformview):
      ...   def __init__(self, context, request):
      ...     data = FormData()
      ...     data.addField(Field("foo", "some default value"))
      ...     data.addField(Field("bar"))
      ...     model = FormModel() 
      ...     view = FormView()
      ...     # We'll leave the poperties out for now, check the main
      ...     # README for details
      ...     view.addRenderable(Input("input0", "foo", "Input foo"))
      ...     view.addRenderable(Input("input1", "bar", "Input bar here"))
      ...     submission = AttrStorage(attr_name="_data")
      ...     form = Form("test", data, model, view, submission)
      ...     pyramidformview.__init__(self, context, request, form)

   Now, a view for pyramid just takes a context, and a request, so let's 
   create the view instance:

      >>> class Context:
      ...  """ nothing needed here, but we'll store the data in here """
      >>> class Request:
      ...   def __init__(self, params={}):
      ...     self.params = params
      >>> ctx = Context()
      >>> req = Request()
      >>> view = yourformview(ctx, req)

   Ok, we're ready for some action now. Let's try to render the form.

      >>> print view.renderform()
      <form class="gw20e-form" method="post" action="" enctype="multipart/form-data">
      <input type="hidden" name="formprocess" value="1"/>
      <div class="alert"></div>
      <div id="input0" class="control input relevant">
      <label for="input-input0">Input foo</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input0" type="text" name="input0" value="some default value" size="20"/>
      </div>
      <div id="input1" class="control input relevant">
      <label for="input-input1">Input bar here</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input1" type="text" name="input1" value="" size="20"/>
      </div>
      </form>
      <BLANKLINE>

   Nice. Now let's give the request some content, and let the view handle the
   submission. This should result in the context having the form data stored
   in the _data attribute. formprocess is the marker used by gw20e.forms
   to assume that the form is posted.

      >>> req = Request({'formprocess': 1, 'input0': 6, 'input1': 'whatever'})
      >>> view = yourformview(ctx, req)
      >>> view()
      {'status': 'stored', 'errors': {}}
      >>> ctx._data.getField('foo').value
      6
      >>> ctx._data.getField('bar').value
      'whatever'


2. XML implementation
---------------------

   Using the XML implementation makes life even easier.


     from gw20e.forms.pyramid.formview import xmlformview as pyramidformview
     from gw20e.forms.xml.formfile import FormFile

     class yourformview(pyramidformview):
     
       def __init__(self, context, request):
           pyramidformview.__init__(self, context, request, FormFile("forms/yourform.xml"))

   where you have a directory 'forms' containing the XML definition
   called yourform.xml. Check the gw20e.forms.xml module for details
   on XML definitions.


 * Create a template (form.pt for example) that calls the render
   method of the view:

   <p tal:content="structure python:view.renderform()"></p>


 * Wire the stuff into zcml (assuming you use that)
   
   <view
     context=".models.YourModel"
     view=".views.yourformview"
     renderer="templates/form.pt"
     name="yourform"
     />
