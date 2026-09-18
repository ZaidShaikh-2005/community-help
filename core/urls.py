from django.urls import path
from . import views


urlpatterns = [

    path('', views.login_view, name='login'),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'add-family/',
        views.add_family,
        name='add_family'
    ),

    path(
        'family-list/',
        views.family_list,
        name='family_list'
    ),

    path(
        'family/<int:family_id>/',
        views.family_detail,
        name='family_detail'
    ),

    path(
        'add-member/',
        views.add_member,
        name='add_member'
    ),

    path(
        'member-list/',
        views.member_list,
        name='member_list'
    ),

    path(
        'member/<int:member_id>/',
        views.member_detail,
        name='member_detail'
    ),

    path(
        'member/<int:member_id>/edit/',
        views.edit_member,
        name='edit_member'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
]