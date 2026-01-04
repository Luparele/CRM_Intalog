# 🚀 Zenith CRM - Sistema de Gestão Comercial e Transportes

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![PWA](https://img.shields.io/badge/PWA-Enabled-orange)
![License](https://img.shields.io/badge/License-Proprietário-red)

Sistema completo de CRM (Customer Relationship Management) desenvolvido para gerenciamento de operações comerciais e logísticas da Intalog Logística, com foco em gestão de clientes, controle de transportes, prospecção de vendas e análise de metas.

## 📋 Índice

- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Páginas Principais](#-páginas-principais)
- [Progressive Web App (PWA)](#-progressive-web-app-pwa)
- [API REST](#-api-rest)
- [Instalação](#-instalação)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Créditos](#-créditos)

---

## 🛠 Tecnologias Utilizadas

### Linguagens e Frameworks

#### Backend
- **Python 3.12** - Linguagem principal do projeto
- **Django 5.2** - Framework web full-stack
- **Django REST Framework** - API REST para integração com sistemas externos
- **SQLite** - Banco de dados (desenvolvimento)
- **PostgreSQL** - Banco de dados (produção - recomendado)

#### Frontend
- **HTML5** - Estruturação semântica
- **CSS3** - Estilização e responsividade
- **JavaScript (ES6+)** - Interatividade e lógica client-side
- **Bootstrap 5.3** - Framework CSS responsivo
- **Bootstrap Icons** - Biblioteca de ícones

### Bibliotecas e Ferramentas

#### Python/Django
```python
# Core
django==5.2
djangorestframework==3.14.0
django-bootstrap5==23.3

# Relatórios e PDFs
xhtml2pdf==0.2.13
reportlab==4.0.7

# Data Analysis
pandas==2.1.4
openpyxl==3.1.2

# HTTP e API
requests==2.31.0

# Data/Time
python-dateutil==2.8.2
```

#### Frontend
- **HTMX 1.9.10** - Interatividade sem JavaScript complexo
- **Chart.js** - Gráficos e visualizações de dados
- **Tom Select** - Select boxes avançados com busca
- **Service Worker** - Cache offline e PWA

### Técnicas e Padrões Implementados

#### Arquitetura
- **MVT (Model-View-Template)** - Padrão do Django
- **RESTful API** - Endpoints padronizados
- **Progressive Enhancement** - Funcionalidade base + melhorias progressivas
- **Responsive Design** - Interface adaptável a todos os dispositivos
- **Component-Based Architecture** - Templates reutilizáveis

#### Performance
- **Lazy Loading** - Carregamento sob demanda
- **Pagination** - Paginação de listas grandes
- **Database Indexing** - Otimização de consultas
- **Query Optimization** - Select related e prefetch
- **Static File Compression** - Minificação de assets

#### Segurança
- **CSRF Protection** - Proteção contra Cross-Site Request Forgery
- **SQL Injection Prevention** - ORM do Django
- **XSS Protection** - Template escaping automático
- **Session Authentication** - Autenticação segura por sessão
- **Permission-Based Access** - Controle de acesso por perfil

#### UX/UI
- **HTMX Partials** - Atualizações parciais sem reload
- **Loading States** - Feedback visual de carregamento
- **Modal Dialogs** - Formulários em modais
- **Toast Notifications** - Notificações não-intrusivas
- **Infinite Scroll** - Carregamento progressivo de listas

---

## 📄 Páginas Principais

### 1. 📊 Dashboard

**Rota:** `/` (Home)

**Descrição:**  
Página principal do sistema com visão consolidada de dados em três períodos: mensal, trimestral e anual.

**Funcionalidades:**
- **Dashboard Mensal**
  - Faturamento total do mês
  - Quantidade de serviços fechados
  - Comparação com meta estabelecida
  - Dias úteis restantes no mês
  - Performance individual dos representantes (visão gestão)
  - Top 5 clientes por faturamento

- **Dashboard Trimestral**
  - Faturamento acumulado do trimestre
  - Gráfico de barras: faturamento por mês
  - Gráfico de linhas: novos clientes cadastrados
  - Gráfico pizza: distribuição por tipo de serviço

- **Dashboard Anual**
  - Visão geral do ano completo
  - Histórico de metas mensais (atingidas/não atingidas)
  - Evolução de faturamento ao longo do ano
  - Comparativo de crescimento

**Filtros Disponíveis:**
- Seleção de mês/trimestre/ano
- Filtro por representante (apenas para gestão)
- Persistência de filtros na sessão

**Tecnologias:**
- Chart.js para gráficos interativos
- HTMX para carregamento dinâmico de períodos
- Django Aggregation para cálculos

**Permissões:**
- Representantes: veem apenas seus próprios dados
- Gestão/Admin: veem dados consolidados de toda equipe

---

### 2. 📅 Agenda (Kanban de Tarefas)

**Rota:** `/agenda/`

**Descrição:**  
Sistema Kanban para gerenciamento de tarefas com três colunas de status.

**Estrutura Kanban:**
```
┌──────────────┬──────────────┬──────────────┐
│ Não Iniciada │   Iniciada   │  Finalizada  │
└──────────────┴──────────────┴──────────────┘
```

**Funcionalidades:**
- **Criação de Tarefas**
  - Título e descrição
  - Atribuição automática ao criador
  - Modal HTMX para criação rápida

- **Gestão de Status**
  - Iniciar tarefa (muda para "Iniciada")
  - Finalizar tarefa (muda para "Finalizada")
  - Registro automático de timestamps e usuário

- **Sistema de Ações**
  - Comentários em tarefas
  - Upload de arquivos anexos
  - Histórico completo de ações
  - Registro de quem fez cada ação

- **Filtros**
  - Por representante (gestão)
  - "Minhas tarefas" (criadas ou atribuídas)

- **Infinite Scroll**
  - Paginação automática nas tarefas finalizadas
  - Carregamento progressivo de 10 em 10

**Tecnologias:**
- HTMX para drag-and-drop (futuro)
- Django Signals para auditoria
- FileField para anexos

---

### 3. 🎯 Prospecção (Funil de Vendas)

**Rota:** `/prospeccao/`

**Descrição:**  
Funil de vendas completo para gestão de prospects e oportunidades comerciais.

**Estrutura do Funil:**
```
Nova → Em Negociação → [Fechado | Desistência | Perdida]
```

**Funcionalidades:**
- **Gestão de Prospects**
  - Cadastro de clientes prospectivos
  - Informações de contato completas
  - Vinculação a prospecções

- **Ciclo de Prospecção**
  - Criação de oportunidade (status: Nova)
  - Estimativas: duração, quantidade de viagens, valor médio
  - Cálculo automático de valor total estimado
  - Tipo de serviço associado

- **Fluxo de Negociação**
  - Iniciar negociação (registra data e usuário)
  - Sistema de ações e follow-ups
  - Upload de propostas e documentos
  - Cálculo automático de dias na etapa

- **Finalização**
  - Fechado: conversão em serviço
  - Desistência: cliente desistiu
  - Perdida: perdeu para concorrente

- **Dashboard de Prospecção**
  - Gráfico de funil (quantidade por etapa)
  - Performance por representante
  - Taxa de conversão
  - Tempo médio de negociação
  - Valor total em negociação

**Métricas Calculadas:**
- Taxa de conversão histórica
- Taxa de conversão mensal
- Tempo médio de negociação (em dias)
- Valor total prospectado

**Tecnologias:**
- Chart.js para visualização do funil
- Django signals para auditoria
- Cálculos automáticos com properties

---

### 4. 🚛 Transportes Realizados

**Rota:** `/servicos/`

**Descrição:**  
Controle completo de serviços de transporte realizados com visão por cliente e representante.

**Funcionalidades:**
- **Lançamento de Serviços**
  - Cliente
  - Tipo de serviço (Rodoviário, Aéreo, etc.)
  - Data do serviço
  - Quantidade de viagens
  - Valor total

- **Visualização Agrupada**
  - Por representante
  - Por cliente dentro de cada representante
  - Totalização automática

- **Filtros**
  - Mês e ano
  - Representante (apenas gestão)

- **Resumo por Representante**
  - Faturamento total
  - Meta do período
  - Percentual atingido
  - Barra de progresso visual

- **Histórico por Cliente**
  - Modal com todos os serviços do cliente no período
  - Edição inline de serviços
  - Cálculo de totais

**Validações:**
- Apenas gestão pode criar/editar serviços
- Representantes visualizam apenas seus clientes
- Registro automático do usuário que fechou

**Tecnologias:**
- Django ORM aggregation
- HTMX para modais de histórico
- Formulários dinâmicos

---

### 5. 🏢 Clientes

**Rota:** `/clientes/`

**Descrição:**  
Gestão completa de carteira de clientes ativos e prospects.

**Funcionalidades:**
- **Cadastro de Clientes**
  - CNPJ
  - Razão social
  - Endereço completo
  - Contato (nome + telefone)
  - Consulta automática de CNPJ via BrasilAPI

- **Gestão de Prospects**
  - Tabela separada para prospects
  - Campos adicionais (email)
  - Promoção de prospect para cliente ativo
  - Migração automática de dados

- **Busca e Filtros**
  - Busca por razão social ou CNPJ
  - Filtro por representante (gestão)
  - Ordenação alfabética

- **Consulta CNPJ Automática**
  - Integração com BrasilAPI
  - Retry automático (40 tentativas)
  - Preenchimento automático de razão social e endereço
  - Tratamento de rate limiting

**Permissões:**
- Representantes: veem e editam apenas seus clientes
- Gestão: vê todos os clientes
- Registro automático do cadastrador

**Tecnologias:**
- Requests para consulta de API externa
- HTMX para promoção de prospects
- Django Forms com validação customizada

---

### 6. 🎯 Metas

**Rota:** `/metas/`

**Descrição:**  
Sistema de definição e acompanhamento de metas mensais.

**Funcionalidades:**
- **Definição de Metas**
  - Meta mensal por representante
  - Valor em R$ (Decimal)
  - Dias úteis do mês
  - Ano e mês

- **Acompanhamento**
  - Comparação automática com faturamento real
  - Cálculo de percentual atingido
  - Visualização por ano

- **Filtros**
  - Seleção de ano
  - Ordenação por mês decrescente

- **Validações**
  - Unique constraint (representante + mês + ano)
  - Apenas gestão pode criar/editar
  - Representantes visualizam apenas suas metas

**Cálculos Automáticos:**
- Percentual atingido da meta
- Valor faltante para atingir
- Média diária necessária (dias úteis)

---

## 📱 Progressive Web App (PWA)

### O que é PWA?

Progressive Web App é uma tecnologia que permite que aplicações web funcionem como aplicativos nativos, oferecendo:
- **Instalação no dispositivo** (como um app real)
- **Funcionamento offline**
- **Notificações push**
- **Ícone na tela inicial**
- **Tela cheia (sem barra do navegador)**

### Implementação no Zenith CRM

#### 1. Manifest.json (`/static/manifest.json`)

Arquivo de configuração que define como o PWA aparece quando instalado:

```json
{
  "name": "Zenith CRM - Intalog Logística",
  "short_name": "Zenith CRM",
  "description": "Sistema de Gestão Comercial e Transportes",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#212529",
  "theme_color": "#212529",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

**Configurações Aplicadas:**
- `display: standalone` - Remove a barra do navegador
- `theme_color` - Cor da barra de status (mobile)
- `icons` - Ícones para tela inicial em múltiplos tamanhos
- `start_url` - Página inicial do app

#### 2. Service Worker (`/static/service-worker.js`)

Script que roda em background e gerencia cache e requisições:

```javascript
const CACHE_NAME = 'zenith-crm-v1';
const urlsToCache = [
  '/',
  '/static/css/bootstrap.min.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/icons/icon-192x192.png'
];

// Instalação - cacheia recursos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

// Fetch - serve do cache quando offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
```

**Estratégias Implementadas:**
- **Cache-First**: Arquivos estáticos (CSS, JS, imagens)
- **Network-First**: Dados dinâmicos (API)
- **Offline Fallback**: Página offline quando sem conexão

#### 3. Meta Tags no HTML

Configurações adicionais no `<head>`:

```html
<!-- PWA Meta Tags -->
<meta name="theme-color" content="#212529">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="Zenith CRM">

<!-- Ícones -->
<link rel="manifest" href="/static/manifest.json">
<link rel="apple-touch-icon" href="/static/icons/apple-touch-icon.png">
```

#### 4. Registro do Service Worker

Script no `base.html` que registra o PWA:

```javascript
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registrado:', registration.scope);
      })
      .catch((error) => {
        console.log('Falha no registro:', error);
      });
  });
}
```

### Benefícios Práticos

✅ **Acesso Offline**  
Usuários podem visualizar páginas cacheadas mesmo sem internet

✅ **Performance**  
Arquivos servidos do cache local (mais rápido que servidor)

✅ **Experiência Mobile**  
App instalável com ícone próprio, sem barra do navegador

✅ **Atualizações Automáticas**  
Service Worker atualiza cache quando há nova versão

✅ **Compatibilidade**  
Funciona em Chrome, Edge, Safari (iOS 11.3+), Firefox

### Como Instalar o PWA

#### Android (Chrome/Edge)
1. Abrir o site
2. Menu → "Adicionar à tela inicial"
3. Confirmar instalação

#### iOS (Safari)
1. Abrir o site
2. Compartilhar → "Adicionar à Tela de Início"
3. Confirmar

#### Desktop (Chrome/Edge)
1. Ícone de instalação na barra de endereço
2. Ou Menu → "Instalar Zenith CRM"

---

## 🔌 API REST

### Visão Geral

API RESTful completa para integração do Zenith CRM com sistemas externos (ERPs, Business Intelligence, aplicativos mobile, etc.).

### Tecnologia

- **Django REST Framework 3.14.0**
- **Autenticação por Sessão**
- **Serialização JSON**
- **Paginação automática (50 itens/página)**

### Arquitetura

```
app/
├── serializers.py      # Conversão Model ↔ JSON
├── api_views.py        # ViewSets (lógica da API)
├── api_urls.py         # Rotas da API
└── models.py           # Modelos de dados
```

### Endpoints Disponíveis

#### Base URL
```
http://seu-dominio.com/api/
```

#### 1. Usuários

```http
GET /api/usuarios/
GET /api/usuarios/{id}/
```

**Resposta:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin Sistema",
      "profile": {
        "setor": "ADMIN",
        "tem_acesso_gestao": true
      }
    }
  ]
}
```

#### 2. Clientes

```http
GET    /api/clientes/
POST   /api/clientes/
GET    /api/clientes/{id}/
PUT    /api/clientes/{id}/
DELETE /api/clientes/{id}/
```

**Query Parameters:**
- `search` - Buscar por razão social ou CNPJ
- `ordering` - Ordenar por campo

**POST Request:**
```json
{
  "cnpj": "12345678000190",
  "razao_social": "Empresa Exemplo LTDA",
  "endereco": "Rua Exemplo, 123",
  "nome_contato": "João Silva",
  "telefone_contato": "(11) 98765-4321"
}
```

#### 3. Serviços

```http
GET  /api/servicos/
POST /api/servicos/
GET  /api/servicos/{id}/
```

**Query Parameters:**
- `ano` - Filtrar por ano (ex: 2024)
- `mes` - Filtrar por mês (ex: 12)
- `cliente` - Filtrar por ID do cliente

**POST Request:**
```json
{
  "cliente": 1,
  "tipo_servico": 1,
  "data_servico": "2025-01-10",
  "quantidade": 5,
  "valor": "7500.00"
}
```

#### 4. Dashboard

```http
GET /api/dashboard/mensal/?mes=12&ano=2024
```

**Resposta:**
```json
{
  "mes": 12,
  "ano": 2024,
  "faturamento_total": "3615000.00",
  "quantidade_servicos": 125,
  "meta_valor": "5000000.00",
  "percentual_meta": 72.3,
  "dias_restantes": 0
}
```

### Autenticação

A API utiliza **autenticação por sessão**. É necessário fazer login através da interface web antes de usar a API.

**Exemplo Python:**
```python
import requests

# Criar sessão
session = requests.Session()

# Fazer login
session.post('http://dominio.com/login/', data={
    'username': 'usuario',
    'password': 'senha'
})

# Usar API
response = session.get('http://dominio.com/api/clientes/')
clientes = response.json()
```

### Códigos de Status

| Código | Significado |
|--------|-------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Não autenticado |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Não encontrado |
| 500 | Internal Server Error |

### Documentação Interativa

Acesse `/api-docs/` no navegador para documentação completa e interativa (apenas administradores).

### Permissões

- **Representantes:** Acesso apenas aos próprios dados
- **Gestão/Admin:** Acesso total a todos os dados

### Casos de Uso

1. **Integração com Power BI**
   - Consumir endpoint `/api/dashboard/mensal/`
   - Gerar relatórios automáticos

2. **App Mobile Personalizado**
   - CRUD completo de clientes
   - Consulta de metas e performance

3. **Sincronização com ERP**
   - Envio automático de serviços fechados
   - Atualização de clientes

4. **Webhooks**
   - Notificações em tempo real
   - Integração com Slack/Teams

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/Luparele/zenith-crm.git
cd zenith-crm
```

2. **Crie ambiente virtual:**
```bash
python -m venv venv
```

3. **Ative o ambiente:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale dependências:**
```bash
pip install -r requirements.txt
pip install djangorestframework --break-system-packages  # Para API
```

5. **Configure o banco de dados:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie superusuário:**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor:**
```bash
python manage.py runserver
```

8. **Acesse o sistema:**
```
http://127.0.0.1:8000/
```

### Configurações de Produção

Para ambiente de produção, edite `CRM_Comercial/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

# Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zenith_crm',
        'USER': 'postgres',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📂 Estrutura do Projeto

```
zenith-crm/
├── app/                          # Aplicação principal
│   ├── migrations/               # Migrações do banco
│   ├── templates/                # Templates HTML
│   │   └── app/
│   │       ├── partials/         # Componentes reutilizáveis
│   │       ├── dashboard_*.html  # Dashboards
│   │       ├── cliente_*.html    # Páginas de clientes
│   │       ├── servico_*.html    # Páginas de serviços
│   │       ├── agenda.html       # Kanban de tarefas
│   │       ├── prospeccao.html   # Funil de vendas
│   │       └── api_documentation.html
│   ├── models.py                 # Modelos de dados
│   ├── views.py                  # Views tradicionais
│   ├── api_views.py              # ViewSets da API
│   ├── serializers.py            # Serializers da API
│   ├── forms.py                  # Formulários Django
│   ├── urls.py                   # Rotas da aplicação
│   └── api_urls.py               # Rotas da API
│
├── CRM_Comercial/                # Configurações do projeto
│   ├── settings.py               # Configurações Django
│   ├── urls.py                   # URLs principais
│   └── wsgi.py                   # Interface WSGI
│
├── static/                       # Arquivos estáticos
│   ├── icons/                    # Ícones PWA
│   ├── app/css/                  # CSS customizado
│   ├── manifest.json             # Manifesto PWA
│   └── service-worker.js         # Service Worker
│
├── templates/                    # Templates globais
│   ├── base.html                 # Template base
│   └── registration/             # Templates de autenticação
│
├── uploads/                      # Arquivos enviados
├── db.sqlite3                    # Banco de dados (dev)
├── manage.py                     # CLI do Django
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

---

## 🎨 Design e UX

### Paleta de Cores

- **Primary:** `#212529` (Dark Gray)
- **Success:** `#28a745` (Green)
- **Warning:** `#ffc107` (Yellow)
- **Danger:** `#dc3545` (Red)
- **Info:** `#17a2b8` (Cyan)

### Princípios de Design

1. **Mobile First** - Interface otimizada para mobile
2. **Consistência** - Padrões visuais uniformes
3. **Feedback Visual** - Loading states e confirmações
4. **Acessibilidade** - Contraste adequado e navegação por teclado
5. **Performance** - Carregamento rápido e responsivo

---

## 📊 Métricas e KPIs

O sistema calcula automaticamente:

- **Taxa de conversão** de prospects
- **Ticket médio** por cliente
- **Faturamento** por período
- **Percentual de meta** atingido
- **Tempo médio** de negociação
- **Performance** individual e coletiva
- **Dias úteis** restantes no mês
- **Projeção** de faturamento

---

## 🔐 Segurança

### Implementações

- ✅ CSRF Protection
- ✅ SQL Injection Prevention (ORM)
- ✅ XSS Protection (Template escaping)
- ✅ Session Authentication
- ✅ Permission-based Access Control
- ✅ Password Hashing (PBKDF2)
- ✅ HTTPS Ready (configurar em produção)

### Recomendações

1. Usar HTTPS em produção
2. Configurar SECRET_KEY único
3. Habilitar rate limiting na API
4. Configurar CORS adequadamente
5. Fazer backup regular do banco
6. Monitorar logs de acesso

---

## 🧪 Testes

### Executar Testes
```bash
python manage.py test
```

### Cobertura de Testes
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📈 Roadmap Futuro

### Fase 2
- [ ] Notificações em tempo real (WebSockets)
- [ ] Chat interno entre representantes
- [ ] Automação de email marketing
- [ ] Integração com WhatsApp Business API
- [ ] Relatórios customizáveis com filtros avançados

### Fase 3
- [ ] Machine Learning para previsão de vendas
- [ ] Dashboard executivo com BI avançado
- [ ] App mobile nativo (React Native)
- [ ] Integração com Google Maps (rotas)
- [ ] Sistema de gamificação

---

## 🐛 Troubleshooting

### Problema: Pylance mostra erros de import
**Solução:** Recarregar janela do VS Code (`Ctrl+Shift+P` → Reload Window)

### Problema: API retorna 401
**Solução:** Fazer login antes de usar a API (autenticação por sessão)

### Problema: PWA não instala
**Solução:** Verificar se está usando HTTPS (obrigatório para PWA)

### Problema: Gráficos não aparecem
**Solução:** Verificar se Chart.js foi carregado corretamente

---

## 📞 Suporte

Para dúvidas, sugestões ou relato de bugs:
- **Email:** eduardo.luparele@example.com
- **GitHub Issues:** [https://github.com/Luparele/zenith-crm/issues](https://github.com/Luparele)

---

## 📜 Licença

Este projeto é **proprietário** e de uso exclusivo da **Intalog Logística**.  
Todos os direitos reservados © 2024-2026

---

## 👨‍💻 Créditos

### Desenvolvimento e Propriedade Intelectual

**EDUARDO LUPARELE COELHO**

- 🔗 GitHub: [https://github.com/Luparele](https://github.com/Luparele)
- 💼 LinkedIn: [Eduardo Luparele Coelho](https://www.linkedin.com/in/eduardo-luparele-coelho-492851296/)
- 📧 Email: eduardo.luparele@gmail.com

### Reconhecimentos

Desenvolvido para **Intalog Logística** com o objetivo de otimizar processos comerciais e logísticos através de tecnologia moderna e eficiente.

**Tecnologias Open Source utilizadas:**
- Django e Django REST Framework
- Bootstrap e Bootstrap Icons
- Chart.js
- HTMX
- Tom Select

---

<div align="center">

**Zenith CRM** - *O ponto mais alto do sucesso comercial* 🚀

Desenvolvido com ❤️ por Eduardo Luparele Coelho

</div>
