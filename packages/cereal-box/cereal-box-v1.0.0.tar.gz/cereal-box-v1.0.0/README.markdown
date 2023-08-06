# cereal-box

## Description
cereal-box is a serialization library that exposes defined functions through a custom Django template tag and a JSON API.

## Examples
#### models.py

	from django.db import models

	class Cereal(models.Model): # Nevermind the naming snafu
		name        = models.CharField(max_length=20)
		sugar_level = models.PositiveIntegerField()
		def __unicode__(self): return self.name

	import cereal
	cereal.register(Cereal, [cereal.functions.filter()])

#### Python

	>>> import cereal
	>>> cereal.call('cereal', 'filter', sugar_level=9)
	[{'sugar_level': 9, 'id': 1, 'name': u'Lucky Charms'}]

#### Template tag

	{% load cereal_tags %}
	{% cereal cereal.filter sugar_level=9 as cereals %}
	<ul>
		{% for c in cereals %}
		<li>{{c.name}}</li>
		{% endfor %}
	</ul>



#### Curl

	curl http://127.0.0.1:8000/api/cereal/filter?sugar_level=9
	[{"sugar_level": 9, "id": 1, "name": "Lucky Charms"}]
