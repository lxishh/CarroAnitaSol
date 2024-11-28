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
    
class ActualizarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Deja en blanco si no deseas cambiar la contraseña'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el campo de la contraseña no sea obligatorio
        self.fields['password'].required = False

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password:  # Si se proporciona una nueva contraseña
            self.instance.set_password(password)  # Usar set_password para cifrarla
            self.password_changed = True  # Marcamos que la contraseña ha cambiado
            print(f"Contraseña cambiada: {password}")  # Imprime en la consola la nueva contraseña (o solo un mensaje)
            return password
        else:
            self.password_changed = False  # Si no se ingresa una nueva contraseña, no ha cambiado
            return self.instance.password  # Mantener la contraseña actual




class ActualizarPerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['telefono', 'rol', 'fecha_contratacion', 'ingresos_totales']
