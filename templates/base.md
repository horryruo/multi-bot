`{{ciddata.get('title')}}`
[fanart]({{ciddata.get('fanart_img')}})
*Cid:* `{{ciddata.get('cid')}}`
*Distribute:* {{ciddata.get('distribute')}}
*Release:* {{ciddata.get('release')}}
*Time:* {{ciddata.get('time')}}
*Performer(s):*  {% for key in ciddata_performers %}
[{{ciddata_performers.get(key)}}](https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress/id={{key}}/) `{{key}}`  {% endfor %}
*Director:* [{{ciddata['director']}}](https://www.dmm.co.jp/digital/videoa/-/list/=/article=director/id={{ciddata.get('directorid')}}/) `{{ciddata.get('directorid')}}`
*Series:* [{{ciddata.get('series')}}](https://www.dmm.co.jp/digital/videoa/-/list/=/article=series/id={{ciddata.get('seriesid')}}/) `{{ciddata.get('seriesid')}}`
*Maker:* [{{ciddata.get('maker')}} ](https://www.dmm.co.jp/digital/videoa/-/list/=/article=maker/id={{ciddata.get('makerid')}}/)  `{{ciddata.get('makerid')}}`
*Label:* [{{ciddata.get('label')}} ](https://www.dmm.co.jp/digital/videoa/-/list/=/article=label/id={{ciddata.get('labelid')}}/)  `{{ciddata.get('labelid')}}`
*Keyword:*  {% for key in ciddata_keyword %}
[{{ciddata_keyword.get(key)}}](https://www.dmm.co.jp/digital/videoa/-/list/=/article=keyword/id={{key}}/) `{{key}}`  {% endfor %}
*Score:* {% for key in ciddata.get('score') %}`{{key}}.`{% endfor %}stars
*ProductNumber:* `{{ciddata.get('cid')}}`
[点击查看更多官方信息](https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={{ciddata.get('cid')}})

