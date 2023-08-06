
tw.uploadify documentation
==========================


tw.uploadify is a tosca widget wrapper around jquery uploadify plugin
 which can be found here :

`http://www.uploadify.com/ <http://www.uploadify.com/>`_

the version released with this package is 2.1.4


using the widget
----------------

in the widget lib
~~~~~~~~~~~~~~~~~

::

    from tw.forms import TableFieldSet
    from tw.uploadify import Uploadify

    class UploadFieldset(TableFieldSet):
        label_text = "upload files"
        fields = [
            Uploadify('upload_file', label_text='upload File',
                      script='upload',
                      fileDataName='upload_file',
                      scriptData={'_method': 'PUT'},
                      removeCompleted=False,
                      ),
                ]

    upload_fieldset = UploadFieldset("upload_fieldset")



in the view controller
~~~~~~~~~~~~~~~~~~~~~~

::

    from widgetlib import upload_fieldset

    ...

    class UploadController(BaseController):

        @expose('project.templates.upload')
        params = { 'child_args' : {
                      'upload_file': dict(script="foobarbaz"),
                    }
                  }
        tmpl_context.file_form = upload_fieldset
        return dict(params=params)


in the template
~~~~~~~~~~~~~~~

::

    <div py:replace="tmpl_context.file_form(**params)">Files Form</div>


options
~~~~~~~

only some options are implemented now, please refer to the widgets.py source code
