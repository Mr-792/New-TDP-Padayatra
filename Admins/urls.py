from django.urls import path
from . import views

urlpatterns=[
    path('',views.sign_in_form,name='signin'),
    path('get_padayatra_registrate',views.get_padayatra_registrate),
    path('dashboard/',views.get_dashboard_stats),
    path('ac',views.AssembliesData.as_view()),
    path('pc',views.DistrictData.as_view()),
    path('admin-signin/',views.admin_sign_api),
    path('ac/<str:district>',views.AcViewSet.as_view({'get':'list'})),
    path('pd/',views.PadayatraScheduleViewSet.as_view({'get':'list',"post":'create'})),






    path('<str:username>/dashboard/',views.admin_dashboard,name='dashboard'),    
    path('<str:username>/posts/',views.view_posts),
    path('<str:username>/post-post/',views.upload_post),
    path('<str:username>/create-post/',views.create_post),
    path('<str:username>/stories/',views.view_stories),
    path('<str:username>/create-story/',views.create_story),
    path('<str:username>/banners/',views.view_banners),
    path('<str:username>/create-banner/',views.create_banner),
    path('<str:username>/padayatra-list/',views.view_padayatra_list,name="padayatra-list"),
    path('<str:username>/schedule-padayatra/',views.schedule_padayatra,name="create-padayatra-form"),
    path('<str:username>/edit-padayatra/<int:id>/',views.edit_padayatra),
    # path('edit/<int:id>/',views.edit),
    path('<str:username>/users/',views.users),
    path('logout/',views.admin_logout),
]