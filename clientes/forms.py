from django import forms
from .models import Cliente, CupoCredito
from socios.models import SocioComercial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from crispy_forms.bootstrap import FormActions

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula', 'fecha_compra', 'valor_compra', 'socio_comercial', 
                 'telefono', 'email', 'ciudad', 'observaciones']
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-0'),
                Column('cedula', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_compra', css_class='form-group col-md-6 mb-0'),
                Column('valor_compra', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('socio_comercial', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ciudad', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            'observaciones',
            FormActions(
                Submit('submit', 'Guardar Cliente', css_class='btn btn-success'),
            )
        )
        
        # Filtrar solo socios activos
        self.fields['socio_comercial'].queryset = SocioComercial.objects.filter(activo=True)

class CupoCreditoForm(forms.ModelForm):
    class Meta:
        model = CupoCredito
        fields = ['nombre', 'ciudad', 'valor_aprobado', 'telefono', 'email', 
                 'fecha_aprobacion', 'observaciones']
        widgets = {
            'fecha_aprobacion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-0'),
                Column('ciudad', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('valor_aprobado', css_class='form-group col-md-6 mb-0'),
                Column('fecha_aprobacion', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observaciones',
            FormActions(
                Submit('submit', 'Guardar Cupo', css_class='btn btn-success'),
            )
        )
