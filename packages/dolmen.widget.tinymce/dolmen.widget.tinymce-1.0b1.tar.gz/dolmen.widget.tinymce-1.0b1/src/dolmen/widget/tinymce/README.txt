=====================
dolmen.widget.tinymce
=====================

`dolmen.widget.tinymce` is a package that provides a useable and
pluggable way to render a text field as a WYSIWG editor in a
`zeam.form` Form.

Example
=======

We are going to develop here a small example, to demonstrate the use
of `dolmen.widget.tinymce`. First, we need to create a model content with
a text field::

  >>> import grokcore.component as grok
  >>> from zope.interface import Interface
  >>> from zope.schema import Text
  >>> from zope.schema.fieldproperty import FieldProperty

  >>> class ICave(Interface):
  ...   paintings = Text(title=u'Description of the cave paintings')

  >>> class Grotto(grok.Context):
  ...   paintings = FieldProperty(ICave['paintings'])

We have now a model that defines a text field. We want to edit/view
this content, using a rich editor, allowing to input rich text and to
display it as valid HTML. To do so, we define a form:

  >>> from zeam.form.ztk import Form, Fields

  >>> class EditCave(Form):
  ...    grok.name('edit')
  ...    grok.context(ICave)
  ...    ignoreContent = False
  ...    fields = Fields(ICave)

  >>> grok.testing.grok_component('edit', EditCave)
  True

At this point, if we instanciate the form, we have a normal
rendering::

  >>> from zope.publisher.browser import TestRequest

  >>> homecave = Grotto()
  >>> request = TestRequest()

  >>> form = EditCave(homecave, request)
  >>> form.updateWidgets()
 
  >>> print form.fieldWidgets.get('form.field.paintings').render() 
  <textarea id="form-field-paintings" name="form.field.paintings" class="field-text" cols="80" rows="5"></textarea>

To get the tinyMCE widget, you simply need to use the "mode" of the
field, to indicate what you want to render::

  >>> from dolmen.widget.tinymce import TINYMCE_INPUT

  >>> form = EditCave(homecave, request)
  >>> form.fields['paintings'].mode = TINYMCE_INPUT
  >>> form.updateWidgets()

  >>> print form.fieldWidgets.get('form.field.paintings').render()
  <script type="text/javascript">
          $(document).ready(function(){
          $('textarea[name="form.field.paintings"]').tinymce();
        });
        </script>
  <textarea id="form-field-paintings"
            name="form.field.paintings" class="field-text"
            cols="80" rows="5"></textarea>

The modes can be 'tinymce.input' for an input widget and
'tinymce.display' to display the value as valid html::

  >>> from dolmen.widget.tinymce import TINYMCE_DISPLAY
  >>> homecave.paintings = u"<h1>Very nice paintings</h1><p>Mammoth</p>"
  
  >>> form = EditCave(homecave, request)
  >>> form.fields['paintings'].mode = TINYMCE_DISPLAY
  >>> form.updateWidgets()

  >>> print form.fieldWidgets.get('form.field.paintings').render()
  <div id="form-field-paintings" name="form.field.paintings"
       class="field"><h1>Very nice paintings</h1><p>Mammoth</p></div>
