from django import forms
import models
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import StrictButton, FormActions, InlineField
import re

class FacturaGenerico(forms.ModelForm):
    class Meta:
        model = models.Factura
        fields = ["tipo", "identificador", "fecha", "titular"]
        labels = {
            'tipo': _('Tipo'),
            'fecha': _('Fecha'),
            'identificador': _('Identificador'),
            'titular': _('Titular'),
        }

    def clean_identificador(self):
        identificador = self.cleaned_data['identificador']
        if identificador:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", identificador):
                raise forms.ValidationError('el identificador de factura solo puede contener letras, numeros o -')
        return identificador

    def clean_titular(self):
        titular = self.cleaned_data['titular']
        if titular:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", titular):
                raise forms.ValidationError('La localidad solo puede contener letras y espacios')
        return titular


class RegistrarFactura(FacturaGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'Factura_add'
    helper.layout = Layout(
        Field('tipo', placeholder='Tipo'),
        Field('identificador', placeholder='Identificador'),
        Field('fecha', placeholder='Fecha',css_class='datepicker'),
        Field('titular', placeholder='Titular'),
        FormActions(
            #StrictButton('Registrar', type="submit", name="_registrar", value="_registrar", id="btn-registrar",
            #            css_class="btn btn-primary"),

            HTML("<button type='submit' id='btnReg' class='btn btn-default'>Registrar</button>")
            #HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )


