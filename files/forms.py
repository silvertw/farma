from django import forms
from files import models as filemodels
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import StrictButton, FormActions, InlineField
import re

class UploadFormGenerico(forms.ModelForm):
    class Meta:
        model = filemodels.Document
        fields = ["filename", "docfile"]
        labels = {
            'filename': _('Nombre del Archivo'),
            'docfile': _('Archivo de Ventas'),
        }


class UploadForm(forms.Form):
    docfile = forms.FileField(label='Archivo de Ventas')
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'File_add'
    helper.layout = Layout(
        Field('docfile', placeholder='Archivo'),

        FormActions(
            #StrictButton('Registrar', type="submit", name="_registrar", value="_registrar", id="btn-registrar",
            #            css_class="btn btn-primary"),

            HTML("<button type='submit' id='btnReg' class='btn btn-default'>Registrar</button>")
            #HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )
