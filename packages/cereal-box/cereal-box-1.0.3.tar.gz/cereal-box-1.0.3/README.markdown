# cereal-box

## Description
cereal-box is a serialization library that exposes defined functions through a custom Django template tag and a JSON API.

## Installation

In your settings, add 'cereal' to INSTALLED_APPS.

In your urls.py, add

    import cereal
    urlpatterns += (patterns('', (r'^api/', include(cereal.urls)))
    
## Settings

When using the standard ceral api the ip addresses and the number of requests 
from those ip addresses will be kept in the cache.  If the number of requests
for a specific ip address exceeds the number or requests per the timeout
then the user will receive a 503 error response, Service Unavailable.  

The available settings to change this behavior are:

    CEREAL_REQUESTS_TIMEOUT, default = 1 (seconds)
    CEREAL_REQUESTS_PER_TIMEOUT, default = 15 (number requests)

It is highly recommended that you use something fast like Redis or Memcache if you
use the timeout view.  Otherwise you'll be using the Django cache which defaults
to your registered database.

If using the cache and the ip address timeout is not desired, simply write your 
own url:

    ('^api/(?P<model>\w+)/(?P<function>\w+)', cereal.views.json_api)   

## Registering a function

There are a couple of different ways you can do this.

    import cereal
    cereal.register(MyModel, [myfunction1, myfunction2])
    cereal.register('my_arbitrary_scope', [myfunction3, myfunction4])
    cereal.register(MyModel, myfunction5)
    cereal.register('my_arbitrary_scope', myfunction6)
    
Model names will be lower cased.  So, MyModel and 'mymodel' are equivalent first arguments.
    
Or you can use the decorator:
    @cereal.register_for('my_scope') #You could also use a model name here
    def my_function(....)
    ...
    
### Function details

Functions take the arguments (scope, **kwargs) where kwargs is all of the arguments passed to cereal.
TODO: eventually we'd like the request (and other info?) to be passed in here somehow.

Functions are expected to return a jsonize-able python object.  Typically you would use .values() to
go from a queryset to a dictionary, although for a less efficient way of getting a similar thing for polymorphic
relations, you can use cereal.smart_values(queryset, *keys).

### Custom serializers

cereal.register takes a third argument, a custom serializer.  This is called by the default filter*()
methods and also can be called manually on a queryset in your registered function with cerial.ize(queryset).
Note that the serializer is tied to a *model* not to a function. TODO: change this behavior?

## Calling a function

You can do this in python, with a template tag, or via a JSON API call.

### Python

    import cereal
    cereal.call('my_scope', 'my_function', arg1=value1, arg2=value2)
    
### Template Tag

    {% load cereal_tags %}
    {% cereal my_scope.my_function arg1=value1 arg2=value2 as cereals %}
    
Now 'cereal' will contain whatever python value was returned.

### JSON API

This uses regular old request parameters.  POSTing also works.

    curl http://path.to.my.site/api/my_scope/my_function?arg1=value1&arg2=value2

The result is a jsonified version of the returned python values.


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
