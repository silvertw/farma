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
        fields = ["tipo", "nroFactura", "fecha", "cuit"]
        labels = {
            'tipo': _('Tipo'),
            'fecha': _('Fecha'),
            'nroFactura': _('nroFactura'),
            'cuit': _('cuit'),
        }


    def clean_nroFactura(self):
        nroFactura = self.cleaned_data['nroFactura']
        if nroFactura:
            if not re.match(r"^[a-zA-Z\d-]+((\s[a-zA-Z\d-]+)+)?$", nroFactura):
                raise forms.ValidationError('El numero puede contener letras numeros y -')
        return nroFactura


    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuit):
            raise forms.ValidationError('CUIT invalido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit

class RegistrarFactura(FacturaGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'Factura_add'
    helper.layout = Layout(
        Field('tipo',placeholder='Tipo'),
        Field('nroFactura', placeholder='nroFactura'),
        Field('fecha', placeholder='Fecha',css_class='datepicker'),
        Field('cuit', placeholder='cuit'),
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


class RangoFechasForm(forms.Form):
    desde = forms.DateField(label='Fecha Desde', required=False, widget=forms.TextInput(attrs={'class':'datepicker'}))
    hasta = forms.DateField(label='Fecha Hasta', widget=forms.TextInput(attrs={'class':'datepicker'}), required=False)









