from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.cms_new, name='cms_new'),
    path('imagen', views.imagen),
    path('loggedIn', views.loggedIn),
    path('logout', views.logout_view),
    path('<str:llave>', views.get_content, name="get_content"),
    path('modify/<str:llave>', views.cms_modify, name="cms_modify"),
]
