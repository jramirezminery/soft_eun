# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from django.urls import path

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('callback', views.callback, name='callback'),
  path('drives', views.drives, name='drives'),
  path('drives/<id>', views.list_drives, name='listdrives'),
  path('drives-folder/<id>', views.list_drives_with_folder, name='listdriveswithfolder'),
  path('calendar', views.calendar, name='calendar'),
  path('calendar/new', views.newevent, name='newevent'),

  # LOGIN / HOMEPAGE
  path('login/level', views.level, name="level")
  
]
