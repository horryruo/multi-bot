`{{stitle}}` 
{% for key in resultdata %}=>{{loop.index}}   *Id:*  [{{key.get('cid')}}]({{key.get('img')}}) [{{key.get('title')}}]({{key.get('links')}})      `{{key.get('keyword')}}`       `{{key.get('cid')}}`      *Type:* [{{key.get('subtexts')}}]({{key.get('sublinks')}})
{% endfor %}