
tw.uploadify documentation
==========================


tw.uploadify is a tosca widget wrapper around jquery uploadify plugin
 which can be found here :

`http://www.uploadify.com/ <http://www.uploadify.com/>`_

the version released with this package is 2.1.4


using the widget
----------------

in the view controller
~~~~~~~~~~~~~~~~~~~~~~

::

    from tw.jqgrid import JqGrid
    from tw.forms import TableFieldSet

    ...

    class UploadController(BaseController):

        @expose('project.templates.upload')
        def upload(self):
            class UploadFieldset(TableFieldSet):
                label_text = "upload files"
                fields = [
                    Uploadify('upload_file', label_text='upload File',
                              script='upload',
                              fileDataName='upload_file',
                              scriptData={'_method': 'PUT'},
                              removeCompleted=False,
                              ),
                    Spacer(),
                        ]

            tmpl_context.file_form = UploadFieldset("upload")
            return dict(values=dict())

in the template::
~~~~~~~~~~~~~~~~~

    <div py:replace="tmpl_context.file_form(value=value)">Files Form</div>


options
~~~~~~~

only some options are implemented now, refer to the widgets.py source code
