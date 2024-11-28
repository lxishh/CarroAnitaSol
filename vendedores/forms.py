from django import forms
from django.contrib.auth.models import User
from .models import Usuario

class CrearUsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    email = forms.EmailField(label="Correo Electrónico", required=True)

    class Meta:
        model = Usuario
        fields = ['telefono', 'rol', 'fecha_contratacion', 'ingresos_totales']

    def save(self, commit=True):
        # Crear el usuario de Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Crear el perfil asociado
        usuario = super().save(commit=False)
        usuario.usuario = user

        if commit:
            usuario.save()
        return usuario
        
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        fecha_contratacion = cleaned_data.get('fecha_contratacion')

        if rol == 'Vendedora' and not fecha_contratacion:
            raise forms.ValidationError("La fecha de contratación es obligatoria para las vendedoras.")
        return cleaned_data