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
        model = models.FacturaDeProveedor
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
        Field('tipo',placeholder='Tipo'),
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


class formaDePagoGenerico(forms.ModelForm):
    class Meta:
        model = models.formaDePago
        fields = ["formaPago"]
        labels = {
            'formaPago': _('Forma de Pago'),
        }

class formaDePago(formaDePagoGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'formaDePago_add'
    helper.layout = Layout(
        Field('formaPago',placeholder='Forma de Pago'),

        FormActions(
            StrictButton('Guardar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar",
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )

#=======================================================================================================================

class PagoGenerico(forms.ModelForm):
    class Meta:
        model = models.Pago
        fields = ["importe","observaciones","fecha","formaDePago"]
        labels = {
            'importe': _('Importe'),
            'fecha': _('Fecha'),
            'observaciones':_('Observaciones'),
            'formaDePago': _('FormaDePago'),
        }

class Pago(PagoGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'formaDePago_add'
    helper.layout = Layout(
        Field('importe',placeholder='Importe'),
        Field('fecha', placeholder='Fecha',css_class='datepicker'),
        Field('observaciones', placeholder='Observaciones'),
        Field('formaDePago', placeholder='Forma de Pago'),
        FormActions(
            #StrictButton('Registrar', type="submit", name="_registrar", value="_registrar", id="btn-registrar",
            #            css_class="btn btn-primary"),
            #HTML("<button type='submit' id='btnReg' class='btn btn-default'>Pagar</button>")
            #HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )












