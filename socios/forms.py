from django import forms
from .models import SocioComercial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from crispy_forms.bootstrap import FormActions

class SocioComercialForm(forms.ModelForm):
    class Meta:
        model = SocioComercial
        fields = ['nombre', 'fecha_ingreso', 'ciudad_sede', 'asesor_asignado', 'documento_contrato',
                 'activo', 'telefono', 'email']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si tenemos una instancia (editando), asegurar que las fechas se muestren
        if self.instance and self.instance.pk:
            # Asegurar que el widget tenga el valor correcto
            if hasattr(self.fields['fecha_ingreso'].widget, 'attrs'):
                if self.instance.fecha_ingreso:
                    self.fields['fecha_ingreso'].widget.attrs['value'] = self.instance.fecha_ingreso.strftime('%Y-%m-%d')
            
            # También establecer el initial
            self.initial.update({
                'fecha_ingreso': self.instance.fecha_ingreso,
            })
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-8 mb-0'),
                Column('activo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_ingreso', css_class='form-group col-md-6 mb-0'),
                Column('ciudad_sede', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('asesor_asignado', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'documento_contrato',
            FormActions(
                Submit('submit', 'Guardar Socio', css_class='btn btn-success'),
            )
        )
