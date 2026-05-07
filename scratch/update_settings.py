import os

path = 'CRM_Comercial/settings.py'
with open(path, 'rb') as f:
    content = f.read().decode('utf-8', 'ignore')

search = "'django.contrib.messages.context_processors.messages',"
replace = search + "\n                'app.context_processors.webpush_settings',"

if search in content:
    new_content = content.replace(search, replace)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Search string not found")
