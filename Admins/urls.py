
from django.contrib import admin
from django.urls import path
from Admins.views import PadayatraScheduleAPI,DashboardAPI,PadayatraSearchAPI,admin_sign_in,YoutubeURLsAPI
from Admins.views import *
from .import views
urlpatterns = [
    path('',views.sign_in_form,name='signin'),
    path('admin-signin/',admin_sign_in.as_view({'post':'sign_in'})),
    path('<str:username>/dashboard/',views.admin_dashboard,name='dashboard'),    
    path('<str:username>/posts/',views.view_posts),
    path('<str:username>/create-post/',views.create_post),
    path('<str:username>/stories/',views.view_stories),
    path('<str:username>/create-story/',views.create_story),
    path('<str:username>/banners/',views.view_banners),
    path('<str:username>/create-banner/',views.create_banner),
    path('<str:username>/padayatra-list/',views.view_padayatra_list,name="padayatra-list"),
    path('<str:username>/schedule-padayatra/',views.schedule_padayatra,name="create-padayatra-form"),
    path('<str:username>/edit-padayatra/<int:id>/',views.edit_padayatra),
    path('<str:username>/posts/edit-post/<int:id>/',views.edit_post),
    path('<str:username>/banners/edit-banner/<int:id>/',views.edit_banner),
    path('<str:username>/stories/edit-story/<int:id>/',views.edit_story),
    path('<str:username>/users/',views.users),
    path('<str:username>/logout/',views.admin_logout),
    path("<str:username>/connect-with-NL/",views.connect_with_nl),
    path('<str:username>/viewpoll/',views.view_poll),
    path('<str:username>/createpoll/',views.createpoll),
    path('<str:username>/live/',views.live),
    path("<str:username>/connect-with-NL/",views.connect_with_nl),
    path('<str:username>/viewpoll/<int:id>/',views.view_poll),
    path('<str:username>/createpoll/',views.createpoll),
    path('verified/',views.verified),
    path('<str:username>/editpoll/<int:id>/',views.edit_poll),
    
    path('create-padayatra', PadayatraScheduleAPI.as_view({'post':'create'})),
    path('get-padayatra/<int:pk>', PadayatraScheduleAPI.as_view({'get':'retrieve'})),
    path('update-padayatra',PadayatraScheduleAPI.as_view({'put':'update'})),
    path('delete-padayatra/<int:pk>',PadayatraScheduleAPI.as_view({'delete':'destroy'})),

    path('all-padayatra-districts',PadayatraSearchAPI.as_view({'get':'all_districts'})),
    path('all-districts-web',PadayatraSearchAPI.as_view({'get':'all_districts_web'})),
    path('all-padayatra-mobile',PadayatraSearchAPI.as_view({'get':'all_padayatra_mobile'})),

    path('padayatra-by-district/<str:district>',PadayatraSearchAPI.as_view({'get':'search_district'})),
    path('padayatra-by-assembly/<str:assembly>',PadayatraSearchAPI.as_view({'get':'search_assembly'})),
    
    path('dashboard',DashboardAPI.as_view({'get':'dashboard'})),
    path('push-notification',DashboardAPI.as_view({'post':'push_notification'})),

    path('create-youtubeURLs', YoutubeURLsAPI.as_view({'post':'create'})),
    path('get-youtubeURLs', YoutubeURLsAPI.as_view({'get':'retrieve'})),
    path('update-youtubeURLs',YoutubeURLsAPI.as_view({'put':'update'})),
    path('delete-youtubeURLs/<int:pk>',YoutubeURLsAPI.as_view({'delete':'destroy'})),
    
    path('<str:username>/sendnotification/',views.sendNotification),

    ]
