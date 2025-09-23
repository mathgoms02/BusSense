from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from ..forms import UserForm, BusRouteForm
from ..documents.user_document import User
from ..documents.bus_route_document import BusRoute

MODEL_MAP = {
    'user': {'form': UserForm, 'document': User, 'title': 'Usuário'},
    'busroute': {'form': BusRouteForm, 'document': BusRoute, 'title': 'Rota de Ônibus'},
}

def select_form_view(request):
    return render(request, 'core/select_form.html')

class DynamicFormView(View):
    def get(self, request, model_name, *args, **kwargs):
        config = MODEL_MAP.get(model_name)
        if not config:
            raise Http404("Modelo não encontrado")

        form = config['form']()
        context = {
            'form': form,
            'model_title': config['title']
        }
        return render(request, 'core/dynamic_form.html', context)

    def post(self, request, model_name, *args, **kwargs):
        config = MODEL_MAP.get(model_name)
        if not config:
            raise Http404("Modelo não encontrado")
        
        form = config['form'](request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            # Lógica de salvamento explícita e segura
            if model_name == 'user':
                instance = User(
                    name=cleaned_data['name'],
                    last_name=cleaned_data['last_name'],
                    email=cleaned_data['email'],
                    is_visually_impaired=cleaned_data['is_visually_impaired']
                )
                instance.set_password(cleaned_data['password'])
            
            elif model_name == 'busroute':
                instance = BusRoute(
                    codigo=cleaned_data['codigo'],
                    tarifa=cleaned_data['tarifa']
                )
            
            instance.save()
            return redirect('select_form')

        context = {
            'form': form,
            'model_title': config['title']
        }
        return render(request, 'core/dynamic_form.html', context)