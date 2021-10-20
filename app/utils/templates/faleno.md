`{{title}}` 
{% for key in data %}=>{{loop.index}}   `{{key.get('work')}}`  [{{key.get('name')}}]({{key.get('img')}}) [{{key.get('url')}}]
{% endfor %}