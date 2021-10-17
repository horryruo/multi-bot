`{{title}}` 
{% for key in data %}=>{{loop.index}}   *Title:*  [{{key.get('name')}}]({{key.get('img')}}) [{{key.get('url')}}]
{% endfor %}