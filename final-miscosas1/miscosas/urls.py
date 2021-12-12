from django.urls import path

from . import views

urlpatterns = [
    path('loggedIn', views.loggedIn,name='loggedIn'),
    path('logout', views.logout_view, name='logOut'),
    path('profilePhoto/<str:user_name>', views.profilePhoto, name='profilePhoto'),
    path('new/', views.new_user, name='new_user'),
    path('', views.index, name='home'),
    path('alimentadores', views.alimentadores, name='alimentadores'),
    path('alimentadores/<str:alim_id>', views.alimentador_info, name='alimentador_info'),
    path('item/<str:item_id>', views.item, name='item_info'),
    path('users', views.users, name='users'),
    path('user/<str:user_id>', views.user_info, name='user_info'),
    path('new_comment/<str:item_id>', views.item_comment, name='item_comment'),
    path('info', views.info, name='info'),
]
