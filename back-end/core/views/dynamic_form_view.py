# back-end/core/views/dynamic_form_view.py

from django.shortcuts import render, redirect
from django.views import View
# Importe TODOS os documents que você quer no formulário
from core.documents import City, BusRoute, Cid 
from core.utils import get_next_sequence_value

# Mapeia os nomes dos documentos para suas classes e campos
# Esta é a versão final, alinhada com seus models
DOCUMENT_CONFIG = {
    'city': {
        'class': City,
        'fields': ['name'],
        'id_field_name': 'id', # CORREÇÃO: Usando 'id' como no seu Document
        'id_sequence_name': 'city'
    },
    'bus_route': {
        'class': BusRoute,
        'fields': ['route_short_name', 'route_name_start', 'route_name_end', 'route_type'],
        'id_field_name': 'id', # CORREÇÃO: Usando 'id' como no seu Document
        'id_sequence_name': 'bus_route'
    },
    'cid': {
        'class': Cid,
        'fields': ['cod', 'diagnostic'],
        'id_field_name': 'cid_id', # CORRETO: 'Cid' usa 'cid_id'
        'id_sequence_name': 'cid'
    }
    # Adicione outras configurações de documento aqui
}

class DynamicFormView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'document_types': DOCUMENT_CONFIG.keys()
        }
        return render(request, 'core/dynamic_form.html', context)

    def post(self, request, *args, **kwargs):
        doc_type = request.POST.get('document_type')
        config = DOCUMENT_CONFIG.get(doc_type)

        if not config:
            return redirect('dynamic_form') 

        next_id = get_next_sequence_value(config['id_sequence_name'])
        
        # Esta lógica agora funciona para todos os casos
        data = {
            config['id_field_name']: next_id 
        }

        for field in config['fields']:
            data[field] = request.POST.get(field)
        
        document_class = config['class']
        new_document = document_class(**data)
        new_document.save()

        return redirect('dynamic_form')
