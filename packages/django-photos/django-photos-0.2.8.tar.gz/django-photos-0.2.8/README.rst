Installation
------------

Install *django-photos* via `pip` from the repository::

	pip install -e hg+http://bitbucket.org/feuervogel/django-photos#egg=django-photos
	
or from *pypi*::

	pip install django-photos

It comes with `django`, `pil`, `easy_thumbnails` and `django-taggit`. 
	
Add all apps to your INSTALLED_APPS in your `settings.py`::

	INSTALLED_APPS = (
		# ...,
		'photos',
		'taggit',
		'easy_thumbnails',        
		# ...,
	)
	
Run `python manage.py syncdb` to sync the database::

	python manage.py syncdb
	
Take care that MEDIA_ROOT and MEDIA_URL are set and the files are served.

Finally add `photos.urls` to your *urls.py*::

	urlpatterns = patterns('',
		# ...,
		(r'^photos/', 'photos.urls'),
		# ...,
	)
	
For more information read the (not yet available) docs.