`all magnet for {{searchid}}`
{% for key in alldata %}=>{{loop.index}}    *title:* [{{key.get('title')}}]({{key.get('url')}})    
*magnet:* `{{key.get('magnet')}}`   
*size and file:* `{{key.get('size')}}`  {{key.get('fileindex')}}
------------------------------------------------------------
{% endfor %}