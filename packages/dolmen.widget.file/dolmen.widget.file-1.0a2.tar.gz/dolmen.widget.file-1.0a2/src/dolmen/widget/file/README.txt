==================
dolmen.widget.file
==================

`dolmen.widget.file` is a package that walks hand-in-hand with
`dolmen.file`. It provides a useable and pluggable way to render the
`dolmen.file.FileField` in a `zeam.form` Form.

Example
=======

We are going to develop here a small example, to demonstrate the use
of `dolmen.widget.file`. First, we need to create a model content with
a file field::

  >>> import dolmen.file
  >>> import grokcore.component as grok
  >>> from zope.interface import Interface
  >>> from zope.schema.fieldproperty import FieldProperty


  >>> class ITravelMount(Interface):
  ...   luggage = dolmen.file.FileField(title=u'Luggages')


  >>> class Mammoth(grok.Context):
  ...   grok.implements(ITravelMount)
  ...   luggage = FieldProperty(ITravelMount['luggage'])


We now have a travel mammoth on which we can add a luggage. Now, we
need a form to edit the animal::

  >>> from zeam.form.ztk import Form, Fields

  >>> class EditMammoth(Form):
  ...    grok.name('edit')
  ...    grok.context(ITravelMount)
  ...    ignoreContent = False
  ...    fields = Fields(ITravelMount)

  >>> grok.testing.grok_component('edit', EditMammoth)
  True

Let's instanciate a Mammoth and try to call the form on it::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> manfred = Mammoth()
  >>> request = TestRequest()

  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets()
 
  >>> print form.fieldWidgets.get('form.field.luggage').render() 
  <div id="form-field-luggage">
      <input type="file" id="form-field-luggage-input"
             name="form.field.luggage" />
  </div>



Now, let's try with a value::
     
  >>> manfred.luggage = "A nice data"
  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets()
  >>> print form.fieldWidgets.get('form.field.luggage').render()
  <div id="form-field-luggage">
    <div>
      <input type="radio" value="keep" checked="checked"
             class="noborder" name="form.field.luggage.action"
             onclick="document.getElementById('form-field-luggage-input').disabled=true"
             id="form-field-luggage-action" />
      <label for="form-field-luggage-action">Keep existing file</label>
      <br />
      <input type="radio" value="delete" class="noborder"
             name="form.field.luggage.action"
             onclick="document.getElementById('form-field-luggage-input').disabled=true"
             id="form-field-luggage-delete" />
      <label for="form-field-luggage-delete">Delete existing file</label>
      <br />
      <input type="radio" value="replace" class="noborder"
             name="form.field.luggage.action"
             onclick="document.getElementById('form-field-luggage-input').disabled=false"
             id="form-field-luggage-replace" />
          <label for="form-field-luggage-replace">Replace with new file</label>
      </div>
    <div>
      <input type="file" id="form-field-luggage-input"
             name="form.field.luggage" />
      <script type="text/javascript">document.getElementById('form-field-luggage-input').disabled=true;</script>
    </div>
  </div>
