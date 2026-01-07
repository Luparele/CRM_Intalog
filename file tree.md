# File Tree: CRM Intalog

**Generated:** 1/7/2026, 12:06:21 PM
**Root Path:** `c:\Users\Segurança\Documents\CRM Intalog`

```
├── CRM_Comercial
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app
│   ├── management
│   │   ├── commands
│   │   │   ├── __init__.py
│   │   │   ├── cleardata.py
│   │   │   ├── populate_db.py
│   │   │   └── populate_prospeccoes.py
│   │   └── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_cliente_filial.py
│   │   ├── 0003_alter_profile_setor.py
│   │   ├── 0004_remove_prospeccao_tipo_proposta_and_more.py
│   │   ├── 0005_recreate_meta_with_cliente.py
│   │   └── __init__.py
│   ├── static
│   │   └── app
│   │       └── css
│   │           └── print.css
│   ├── __init__.py
│   ├── admin.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── backup
│   ├── _cliente_form_modal.html
│   ├── _servico_historico_modal.html
│   ├── _tarefas_finalizadas_paginadas.html
│   ├── agenda.html
│   └── views.py
├── static
│   ├── icons
│   │   ├── apple-touch-icon.png
│   │   ├── favicon.ico
│   │   ├── icon-128x128.png
│   │   ├── icon-144x144.png
│   │   ├── icon-152x152.png
│   │   ├── icon-192x192.png
│   │   ├── icon-384x384.png
│   │   ├── icon-512x512.png
│   │   ├── icon-72x72.png
│   │   └── icon-96x96.png
│   ├── manifest.json
│   └── service-worker.js
├── static_root
│   ├── admin
│   │   ├── css
│   │   │   ├── vendor
│   │   │   │   └── select2
│   │   │   │       ├── LICENSE-SELECT2.md
│   │   │   │       └── select2.css
│   │   │   ├── autocomplete.css
│   │   │   ├── base.css
│   │   │   ├── changelists.css
│   │   │   ├── dark_mode.css
│   │   │   ├── dashboard.css
│   │   │   ├── forms.css
│   │   │   ├── login.css
│   │   │   ├── nav_sidebar.css
│   │   │   ├── responsive.css
│   │   │   ├── responsive_rtl.css
│   │   │   ├── rtl.css
│   │   │   ├── unusable_password_field.css
│   │   │   └── widgets.css
│   │   ├── img
│   │   │   ├── gis
│   │   │   │   ├── move_vertex_off.svg
│   │   │   │   └── move_vertex_on.svg
│   │   │   ├── LICENSE
│   │   │   ├── README.txt
│   │   │   ├── calendar-icons.svg
│   │   │   ├── icon-addlink.svg
│   │   │   ├── icon-alert.svg
│   │   │   ├── icon-calendar.svg
│   │   │   ├── icon-changelink.svg
│   │   │   ├── icon-clock.svg
│   │   │   ├── icon-deletelink.svg
│   │   │   ├── icon-hidelink.svg
│   │   │   ├── icon-no.svg
│   │   │   ├── icon-unknown-alt.svg
│   │   │   ├── icon-unknown.svg
│   │   │   ├── icon-viewlink.svg
│   │   │   ├── icon-yes.svg
│   │   │   ├── inline-delete.svg
│   │   │   ├── search.svg
│   │   │   ├── selector-icons.svg
│   │   │   ├── sorting-icons.svg
│   │   │   ├── tooltag-add.svg
│   │   │   └── tooltag-arrowright.svg
│   │   └── js
│   │       ├── admin
│   │       │   ├── DateTimeShortcuts.js
│   │       │   └── RelatedObjectLookups.js
│   │       ├── vendor
│   │       │   ├── jquery
│   │       │   │   ├── LICENSE.txt
│   │       │   │   └── jquery.js
│   │       │   ├── select2
│   │       │   │   ├── i18n
│   │       │   │   │   ├── af.js
│   │       │   │   │   ├── ar.js
│   │       │   │   │   ├── az.js
│   │       │   │   │   ├── bg.js
│   │       │   │   │   ├── bn.js
│   │       │   │   │   ├── bs.js
│   │       │   │   │   ├── ca.js
│   │       │   │   │   ├── cs.js
│   │       │   │   │   ├── da.js
│   │       │   │   │   ├── de.js
│   │       │   │   │   ├── dsb.js
│   │       │   │   │   ├── el.js
│   │       │   │   │   ├── en.js
│   │       │   │   │   ├── es.js
│   │       │   │   │   ├── et.js
│   │       │   │   │   ├── eu.js
│   │       │   │   │   ├── fa.js
│   │       │   │   │   ├── fi.js
│   │       │   │   │   ├── fr.js
│   │       │   │   │   ├── gl.js
│   │       │   │   │   ├── he.js
│   │       │   │   │   ├── hi.js
│   │       │   │   │   ├── hr.js
│   │       │   │   │   ├── hsb.js
│   │       │   │   │   ├── hu.js
│   │       │   │   │   ├── hy.js
│   │       │   │   │   ├── id.js
│   │       │   │   │   ├── is.js
│   │       │   │   │   ├── it.js
│   │       │   │   │   ├── ja.js
│   │       │   │   │   ├── ka.js
│   │       │   │   │   ├── km.js
│   │       │   │   │   ├── ko.js
│   │       │   │   │   ├── lt.js
│   │       │   │   │   ├── lv.js
│   │       │   │   │   ├── mk.js
│   │       │   │   │   ├── ms.js
│   │       │   │   │   ├── nb.js
│   │       │   │   │   ├── ne.js
│   │       │   │   │   ├── nl.js
│   │       │   │   │   ├── pl.js
│   │       │   │   │   ├── ps.js
│   │       │   │   │   ├── pt-BR.js
│   │       │   │   │   ├── pt.js
│   │       │   │   │   ├── ro.js
│   │       │   │   │   ├── ru.js
│   │       │   │   │   ├── sk.js
│   │       │   │   │   ├── sl.js
│   │       │   │   │   ├── sq.js
│   │       │   │   │   ├── sr-Cyrl.js
│   │       │   │   │   ├── sr.js
│   │       │   │   │   ├── sv.js
│   │       │   │   │   ├── th.js
│   │       │   │   │   ├── tk.js
│   │       │   │   │   ├── tr.js
│   │       │   │   │   ├── uk.js
│   │       │   │   │   ├── vi.js
│   │       │   │   │   ├── zh-CN.js
│   │       │   │   │   └── zh-TW.js
│   │       │   │   ├── LICENSE.md
│   │       │   │   └── select2.full.js
│   │       │   └── xregexp
│   │       │       ├── LICENSE.txt
│   │       │       └── xregexp.js
│   │       ├── SelectBox.js
│   │       ├── SelectFilter2.js
│   │       ├── actions.js
│   │       ├── autocomplete.js
│   │       ├── calendar.js
│   │       ├── cancel.js
│   │       ├── change_form.js
│   │       ├── core.js
│   │       ├── filters.js
│   │       ├── inlines.js
│   │       ├── jquery.init.js
│   │       ├── nav_sidebar.js
│   │       ├── popup_response.js
│   │       ├── prepopulate.js
│   │       ├── prepopulate_init.js
│   │       ├── theme.js
│   │       ├── unusable_password_field.js
│   │       └── urlify.js
│   ├── app
│   │   └── css
│   │       └── print.css
│   ├── icons
│   │   ├── apple-touch-icon.png
│   │   ├── favicon.ico
│   │   ├── icon-128x128.png
│   │   ├── icon-144x144.png
│   │   ├── icon-152x152.png
│   │   ├── icon-192x192.png
│   │   ├── icon-384x384.png
│   │   ├── icon-512x512.png
│   │   ├── icon-72x72.png
│   │   └── icon-96x96.png
│   ├── manifest.json
│   └── service-worker.js
├── templates
│   ├── app
│   │   ├── partials
│   │   │   ├── _acoes_list.html
│   │   │   ├── _acoes_prospeccao_list.html
│   │   │   ├── _agenda_header.html
│   │   │   ├── _cliente_form_modal.html
│   │   │   ├── _cliente_promocao_modal.html
│   │   │   ├── _dashboard_anual.html
│   │   │   ├── _dashboard_anual_CORRIGIDO.html
│   │   │   ├── _dashboard_filters.html
│   │   │   ├── _dashboard_mensal.html
│   │   │   ├── _dashboard_prospeccao_content.html
│   │   │   ├── _dashboard_top_clientes.html
│   │   │   ├── _dashboard_trimestral.html
│   │   │   ├── _detalhe_prospeccao_modal.html
│   │   │   ├── _detalhe_representante_modal.html
│   │   │   ├── _detalhe_tarefa_modal.html
│   │   │   ├── _navbar.html
│   │   │   ├── _prospeccao_card.html
│   │   │   ├── _prospeccao_edit_form_modal.html
│   │   │   ├── _prospeccao_form_modal.html
│   │   │   ├── _relatorio_pdf_clientes.html
│   │   │   ├── _relatorio_pdf_faturamento.html
│   │   │   ├── _relatorio_pdf_historico.html
│   │   │   ├── _relatorio_resultados.html
│   │   │   ├── _servico_form_modal.html
│   │   │   ├── _servico_historico_modal.html
│   │   │   ├── _tarefa_card.html
│   │   │   ├── _tarefa_form_modal.html
│   │   │   └── _tarefas_finalizadas_paginadas.html
│   │   ├── agenda.html
│   │   ├── api_documentation.html
│   │   ├── cliente_confirm_delete.html
│   │   ├── cliente_detail.html
│   │   ├── cliente_form.html
│   │   ├── cliente_list.html
│   │   ├── dashboard_admin.html
│   │   ├── dashboard_prospeccao.html
│   │   ├── dashboard_representante.html
│   │   ├── direitos.html
│   │   ├── home.html
│   │   ├── meta_confirm_delete.html
│   │   ├── meta_form.html
│   │   ├── meta_list.html
│   │   ├── prospeccao.html
│   │   ├── relatorios.html
│   │   ├── representante_form.html
│   │   ├── representante_list.html
│   │   ├── servico_confirm_delete.html
│   │   ├── servico_form.html
│   │   └── servico_list.html
│   ├── partials
│   │   └── _dashboard_filters.html
│   ├── registration
│   │   ├── login.html
│   │   ├── password_change_done.html
│   │   └── password_change_form.html
│   └── base.html
├── .gitignore
├── .pylintrc
├── LICENSE
├── README.md
├── dados do projeto.txt
├── manage.py
├── pyrightconfig.json
└── requirements.txt
```

---
*Generated by FileTree Pro Extension*