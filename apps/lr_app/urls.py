from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^register$', views.log_register, name="register"),
	url(r'^login$', views.log_register, name="login"),
	url(r'^logout$', views.logout, name="logout"),
]
