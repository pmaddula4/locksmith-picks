from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('defvpos/', views.defvpos, name="defvpos"),
    path('hotandcold/', views.hotandcold, name="hotandcold"),
    path('l10/', views.l10, name="l10"),
    path('mailinglist/', views.mailinglist, name="mailinglist"),
]