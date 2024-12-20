from django import forms
from django.contrib.auth.models import User
from .models import Usuario
import re
from datetime import date


class CrearUsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    email = forms.EmailField(label="Correo Electrónico", required=True)

    class Meta:
        model = Usuario
        fields = ['rut', 'telefono', 'rol', 'fecha_contratacion']
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
        }

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

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Verificar si el nombre de usuario ya existe en la base de datos
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "El nombre de usuario ya está en uso. Por favor, elige otro.")

        # Validar que el username no contenga números
        if re.search(r'\d', username):
            raise forms.ValidationError(
                "El nombre de usuario no debe contener números.")

        return username

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Validar que el teléfono comience con 9 y tenga 9 dígitos
        if not re.match(r'^9\d{8}$', telefono):
            raise forms.ValidationError(
                "El teléfono debe comenzar con 9 y tener 9 dígitos en total.")
        return telefono

    def clean_fecha_contratacion(self):
        fecha_contratacion = self.cleaned_data.get('fecha_contratacion')
        # Validar que la fecha de contratación no sea superior a la fecha actual
        if fecha_contratacion and fecha_contratacion > date.today():
            raise forms.ValidationError(
                "La fecha de contratación no puede ser posterior a la fecha actual.")
        return fecha_contratacion

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Validar que la contraseña tenga al menos 12 caracteres
        if len(password) < 12:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 12 caracteres.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        fecha_contratacion = cleaned_data.get('fecha_contratacion')

        if rol == 'Vendedora' and not fecha_contratacion:
            raise forms.ValidationError(
                "La fecha de contratación es obligatoria para las vendedoras.")
        return cleaned_data


class ActualizarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Debes de ingresar la contraseña para actualizar'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el campo de la contraseña no sea obligatorio
        self.fields['password'].required = False

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:  # Si se proporciona una nueva contraseña
            # Usar set_password para cifrarla
            self.instance.set_password(password)
            self.password_changed = True  # Marcamos que la contraseña ha cambiado
            return password
        else:
            # Si no se ingresa una nueva contraseña, no ha cambiado
            self.password_changed = False
            return self.instance.password  # Mantener la contraseña actual


class ActualizarPerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'telefono', 'rol', 'fecha_contratacion']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # Validar que el RUT tenga el formato adecuado (8 dígitos seguidos de un guion y un dígito o letra)
        if not re.match(r'^\d{8}-[0-9A-Za-z]$', rut):
            raise forms.ValidationError(
                "El RUT debe tener 8 dígitos, un guion y un número o letra al final. Ejemplo: 12345678-1"
            )

        return rut
