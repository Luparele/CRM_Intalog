from django import forms
from django.contrib.auth.models import User
from .models import Profile, Cliente, ClienteProspect, Servico, Meta, Tarefa, AcaoTarefa, Prospeccao, AcaoProspeccao
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal
import calendar
from datetime import date


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        help_texts = {
            'username': None,
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('telefone', 'setor', 'status')
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class ClienteForm(forms.ModelForm):
    """ Formulário para Clientes ATIVOS (Com serviços) """
    class Meta:
        model = Cliente
        fields = ['cadastrado_por', 'cnpj', 'razao_social', 'endereco', 'nome_contato', 'telefone_contato']
        
        widgets = {
            'cadastrado_por': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'cadastrado_por': 'Representante Responsável (Dono da Carteira)',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['cadastrado_por'].queryset = User.objects.filter(
            is_active=True, 
            profile__setor='REPRESENTANTE'
        ).order_by('username')
        
        if self.user:
            # --- ALTERAÇÃO: Permissão para escolher dono agora é do COMERCIAL e ADMIN ---
            pode_escolher_dono = (
                self.user.is_staff or 
                self.user.profile.tem_acesso_gestao # Inclui COMERCIAL e ADMIN
            )
            
            if not pode_escolher_dono:
                del self.fields['cadastrado_por']
            else:
                self.fields['cadastrado_por'].required = True


class ClienteProspectForm(forms.ModelForm):
    class Meta:
        model = ClienteProspect
        fields = ['cnpj', 'razao_social', 'nome_contato', 'telefone_contato', 'email_contato']
        widgets = {
            'cnpj': forms.TextInput(attrs={'hx-get': '/app/api/consultar-cnpj/', 'hx-trigger': 'blur', 'hx-target': '#id_razao_social', 'hx-swap': 'outerHTML', 'placeholder': '00.000.000/0000-00'}),
            'email_contato': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
        }

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['cliente', 'tipo_servico', 'data_servico', 'quantidade', 'valor']
        widgets = {
            'data_servico': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'tipo_servico': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # --- ALTERAÇÃO: COMERCIAL e ADMIN veem todos os clientes ---
            if user.is_staff or user.profile.tem_acesso_gestao:
                self.fields['cliente'].queryset = Cliente.objects.all().order_by('razao_social')
            else:
                self.fields['cliente'].queryset = Cliente.objects.filter(cadastrado_por=user).order_by('razao_social')

class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['cliente', 'mes', 'ano', 'dias_uteis', 'valor']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.order_by('razao_social')
        self.fields['cliente'].label = "Cliente"

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if hasattr(user, 'profile') and user.profile.status == 'INATIVO':
            raise forms.ValidationError(
                "Usuário INATIVO! Por favor, entre em contato com o administrador para solicitar a reativação.",
                code='inactive_profile'
            )

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class AcaoTarefaForm(forms.ModelForm):
    class Meta:
        model = AcaoTarefa
        fields = ['descricao', 'arquivo']
        labels = {
            'descricao': "Ação a ser Tomada:",
            'arquivo': "Anexar Arquivo (Opcional):"
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva a ação realizada ou o próximo passo...'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control form-control-sm'})
        }

class ProspectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.razao_social} ({obj.cnpj or 'S/ CNPJ'})"

class ProspeccaoForm(forms.ModelForm):
    cliente = ProspectChoiceField(
        queryset=ClienteProspect.objects.none(),
        label="Prospect"
    )

    class Meta:
        model = Prospeccao
        fields = [
            'cliente', 'tipo_servico', 'duracao_meses', 
            'viagens_aproximadas', 'valor_medio_viagem'
        ]
        widgets = {
            'tipo_servico': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        prospects_queryset = ClienteProspect.objects.order_by('razao_social')

        if user:
            # --- ALTERAÇÃO: COMERCIAL e ADMIN veem todos prospects ---
            if user.is_staff or user.profile.tem_acesso_gestao:
                self.fields['cliente'].queryset = prospects_queryset
            else:
                self.fields['cliente'].queryset = prospects_queryset.filter(cadastrado_por=user)

    def clean(self):
        cleaned_data = super().clean()
        viagens = cleaned_data.get('viagens_aproximadas')
        valor_medio = cleaned_data.get('valor_medio_viagem')

        if viagens and valor_medio:
            cleaned_data['valor_total'] = Decimal(viagens) * valor_medio
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.valor_total = self.cleaned_data.get('valor_total', 0)
        if commit:
            instance.save()
        return instance

class AcaoProspeccaoForm(forms.ModelForm):
    class Meta:
        model = AcaoProspeccao
        fields = ['descricao', 'arquivo']
        labels = {
            'descricao': "Ação a ser Tomada:",
            'arquivo': "Anexar Arquivo (Opcional):"
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva a ação realizada ou o próximo passo...'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control form-control-sm'})
        }

class ProspeccaoEditForm(forms.ModelForm):
    class Meta:
        model = Prospeccao
        fields = [
            'tipo_servico', 'duracao_meses', 
            'viagens_aproximadas', 'valor_medio_viagem'
        ]
        widgets = {
            'tipo_servico': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        viagens = cleaned_data.get('viagens_aproximadas')
        valor_medio = cleaned_data.get('valor_medio_viagem')

        if viagens and valor_medio:
            cleaned_data['valor_total'] = Decimal(viagens) * valor_medio
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.valor_total = self.cleaned_data.get('valor_total', instance.valor_total)
        if commit:
            instance.save()
        return instance
