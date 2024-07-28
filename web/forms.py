from django import forms

class ClienteForm(forms.Form):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )   

    cedula = forms.CharField(label="CEDULA", max_length=10)
    nombre = forms.CharField(label="Nombre", max_length=200, required=True)
    apellidos = forms.CharField(label="Apellidos", max_length=200, required=True)
    email = forms.EmailField(label="Email", required=True)
    direccion = forms.CharField(label="Direccion", widget=forms.Textarea)
    telefono = forms.CharField(label="Telefono", max_length=15)
    sexo = forms.ChoiceField(label="Sexo", choices=(('M', 'Masculino'), ('F', 'Femenino')))
    fecha_nacimiento = forms.DateField(label="Fecha Nacimiento", input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d'))