from django import forms
from .models import SeguimientoSocio
from socios.models import SocioComercial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Fieldset
from crispy_forms.bootstrap import FormActions

class SeguimientoSocioForm(forms.ModelForm):
    class Meta:
        model = SeguimientoSocio
        fields = [
            'socio_potencial', 'socio_comercial', 'estado',
            'presentacion_negocio', 'fecha_presentacion',
            'documentos_enviados', 'fecha_envio_documentos',
            'contrato_enviado', 'fecha_envio_contrato',
            'contrato_firmado', 'fecha_firma_contrato',
            'capacitacion_realizada', 'fecha_capacitacion',
            'usuario_creado', 'fecha_creacion_usuario',
            'telefono', 'email', 'ciudad', 'observaciones'
        ]
        widgets = {
            'fecha_presentacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio_documentos': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio_contrato': forms.DateInput(attrs={'type': 'date'}),
            'fecha_firma_contrato': forms.DateInput(attrs={'type': 'date'}),
            'fecha_capacitacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_creacion_usuario': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si tenemos una instancia (editando), configurar fechas iniciales
        if self.instance and self.instance.pk:
            self.initial.update({
                'fecha_presentacion': self.instance.fecha_presentacion,
                'fecha_envio_documentos': self.instance.fecha_envio_documentos,
                'fecha_envio_contrato': self.instance.fecha_envio_contrato,
                'fecha_firma_contrato': self.instance.fecha_firma_contrato,
                'fecha_capacitacion': self.instance.fecha_capacitacion,
                'fecha_creacion_usuario': self.instance.fecha_creacion_usuario,
            })
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Información Básica',
                Row(
                    Column('socio_potencial', css_class='form-group col-md-8 mb-0'),
                    Column('estado', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('socio_comercial', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('telefono', css_class='form-group col-md-4 mb-0'),
                    Column('email', css_class='form-group col-md-4 mb-0'),
                    Column('ciudad', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Seguimiento del Proceso',
                Row(
                    Column('presentacion_negocio', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_presentacion', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('documentos_enviados', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_envio_documentos', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('contrato_enviado', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_envio_contrato', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('contrato_firmado', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_firma_contrato', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('capacitacion_realizada', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_capacitacion', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('usuario_creado', css_class='form-group col-md-6 mb-0'),
                    Column('fecha_creacion_usuario', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
            ),
            'observaciones',
            FormActions(
                Submit('submit', 'Guardar Seguimiento', css_class='btn btn-success'),
            )
        )
