===================
dolmen.widget.image
===================

`dolmen.widget.image` is a thin layer above `dolmen.widget.file`
providing a widget suitable to fields implementing IImageField. It
adds, thanks to `dolmen.thumbnailer` a preview of the uploaded image
in both input and display mode.

Example
=======

We are going to develop here a small example, to demonstrate the use
of `dolmen.widget.image`. First, we instanciate our test model and add
an image field to the object::

  >>> class Mammoth(object):
  ...     pass

  >>> import dolmen.file
  >>> import grokcore.component as grok
  >>> from zope.interface import Interface, alsoProvides
  >>> from zope.schema.fieldproperty import FieldProperty

  >>> class IMammothId(Interface):
  ...   """Even mammoths need an ID card"""
  ...   picture = dolmen.file.ImageField(title=u'Luggages')

  >>> manfred = Mammoth()
  >>> manfred.picture = None
  >>> alsoProvides(manfred, IMammothId)

The picture is now set on our Mammoth. We create a form to try and
edit the picture field::

  >>> from zeam.form.ztk import Form, Fields

  >>> class EditMammoth(Form):
  ...    grok.name('edit')
  ...    grok.context(IMammothId)
  ...    ignoreContent = False
  ...    fields = Fields(IMammothId)

  >>> grok.testing.grok_component('edit', EditMammoth)
  True

We persist our Mammoth to get a located mammoth with an URL::

  >>> from zope.component.hooks import getSite
  >>> root = getSite()
  >>> root['manfred'] = manfred
  >>> manfred = root['manfred']

We can call the edit form on our persisted object::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  
  >>> request = TestRequest()

  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets()
  >>> print form.fieldWidgets.get('form.field.picture').render()
  <div id="form-field-picture">
      <input type="file" id="form-field-picture-input"
               name="form.field.picture" />
  </div>

Now, let's try with a fake value::
     
  >>> manfred.picture = "some fake image"
  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets() 

  >>> print form.fieldWidgets.get('form.field.picture').render()
  <div id="form-field-picture">
    <div>
      <div class="widget-image-preview">
        <img src="http://127.0.0.1/manfred/++thumbnail++picture.preview"
             title="Download" />
      </div>
      <p class="file-info">
        <a class="filename"
           href="http://127.0.0.1/manfred/++download++picture">Download</a>
      </p>
    </div>
    <div>
      <input type="radio" value="keep" checked="checked"
             class="noborder" name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=true"
             id="form-field-picture-action" />
      <label for="form-field-picture-action">Keep existing file</label>
      <br />
      <input type="radio" value="delete" class="noborder"
             name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=true"
             id="form-field-picture-delete" />
      <label for="form-field-picture-delete">Delete existing file</label>
      <br />
      <input type="radio" value="replace" class="noborder"
             name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=false"
             id="form-field-picture-replace" />
          <label for="form-field-picture-replace">Replace with new file</label>
    </div>
    <div>
      <input type="file" id="form-field-picture-input"
             name="form.field.picture" />
      <script type="text/javascript">document.getElementById('form-field-picture-input').disabled=true;</script>
    </div>
  </div>


With non persistent objects (which don't resolve to an URL), no
preview is displayed. If we can't resolve to an URL, we can't serve
the thumbnail or download the data::

  >>> judith = Mammoth()
  >>> judith.picture = "Fake image data"
  >>> alsoProvides(judith, IMammothId)

  >>> form = getMultiAdapter((judith, request), name='edit')
  >>> form.updateWidgets() 
  >>> print form.fieldWidgets.get('form.field.picture').render()
  <div id="form-field-picture">
    <div>
      <input type="radio" value="keep" checked="checked"
             class="noborder" name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=true"
             id="form-field-picture-action" />
      <label for="form-field-picture-action">Keep existing file</label>
      <br />
      <input type="radio" value="delete" class="noborder"
             name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=true"
             id="form-field-picture-delete" />
      <label for="form-field-picture-delete">Delete existing file</label>
      <br />
      <input type="radio" value="replace" class="noborder"
             name="form.field.picture.action"
             onclick="document.getElementById('form-field-picture-input').disabled=false"
             id="form-field-picture-replace" />
          <label for="form-field-picture-replace">Replace with new file</label>
    </div>
    <div>
      <input type="file" id="form-field-picture-input"
             name="form.field.picture" />
      <script type="text/javascript">document.getElementById('form-field-picture-input').disabled=true;</script>
    </div>
  </div>
