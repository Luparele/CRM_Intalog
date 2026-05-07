import os

file_path = r'c:\Users\Segurança\Documents\CRM Intalog\templates\app\partials\_detalhe_tarefa_agendada_modal.html'

new_content = """<div class="modal-header">
    <h5 class="modal-title">{{ tarefa.titulo }}</h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
</div>
<div class="modal-body">
    <div class="mb-3">
        <label class="fw-bold">Status:</label>
        <span
            class="badge {% if tarefa.status == 'REALIZADA' %}bg-success{% elif tarefa.status == 'NAO_REALIZADA' %}bg-danger{% else %}bg-secondary{% endif %}">
            {{ tarefa.get_status_display }}
        </span>
    </div>

    <div class="mb-3">
        <label class="fw-bold">Descrição:</label>
        <p class="text-muted">{{ tarefa.descricao|linebreaks|default:"Sem descrição." }}</p>
    </div>

    <div class="row text-muted small">
        <div class="col-6">
            <strong>Data Agenda:</strong> {{ tarefa.data_agendamento|date:"d/m/Y" }}
        </div>
        <div class="col-6">
            <strong>Atribuído a:</strong> {{ tarefa.get_responsavel_nome }}
        </div>
        <div class="col-6 mt-2">
            <strong>Criado por:</strong> {{ tarefa.criado_por.get_full_name|default:tarefa.criado_por.username }} <small class="text-muted">em {{ tarefa.data_criacao|date:"d/m/Y H:i" }}</small>
        </div>
        <div class="col-6 mt-2">
            <strong>Visualizada em:</strong> {{ tarefa.visualizada_em|date:"d/m/Y H:i"|default:"-" }}
        </div>
        {% if tarefa.finalizado_por %}
        <div class="col-6 mt-2">
            <strong>Finalizado por:</strong> {{ tarefa.get_finalizador_nome }} <small class="text-muted">em {{ tarefa.data_finalizacao|date:"d/m/Y H:i" }}</small>
        </div>
        {% endif %}
    </div>
</div>
<div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
</div>
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"File overwritten successfully: {file_path}")
print("New content preview:")
print(new_content)
