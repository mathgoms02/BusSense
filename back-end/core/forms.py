from django import forms
from .documents.user_document import User

# --- Formulário de Usuário (já existente) ---
class UserForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    is_visually_impaired = forms.BooleanField(label='É deficiente visual?', required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects(email=email).first():
            raise forms.ValidationError("Este email já está em uso.")
        return email

# --- NOVO: Formulário de Rota de Ônibus ---
class BusRouteForm(forms.Form):
    codigo = forms.CharField(label='Código da Rota', max_length=50)
    tarifa = forms.FloatField(label='Tarifa')