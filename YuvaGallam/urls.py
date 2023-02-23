"""YuvaGallam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from Admins import views

urlpatterns = [
    # path('/', Returnpage.as_view({'get':'retrieve'})),

    # path('admin/', admin.site.urls),
    # path('',views.sign_in_form,name='signin'),
    # path('admin-signin/',views.admin_login),
    # path('admin_dashboard/',views.admin_dashboard,name='dashboard'),    
    # path('posts/',views.view_posts),
    # path('post-post/',views.upload_post),
    # path('create-post/',views.create_post),
    # path('stories/',views.view_stories),
    # path('create-story/',views.create_story),
    # path('banners/',views.view_banners),
    # path('create-banner/',views.create_banner),
    # path('padayatra-list/',views.view_padayatra_list,name="padayatra-list"),
    # path('schedule-padayatra/',views.schedule_padayatra,name="create-padayatra-form"),
    # path('schedule/',views.schedule),
    # path('edit-padayatra/<int:id>/',views.edit_padayatra),
    # path('edit/<int:id>/',views.edit),
    # path('users/',views.users),
    # path('logout/',views.admin_logout),
    path('',include('Admins.urls')),

    path('feed/',include('Feed.urls')),
    path('users/',include('Users.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
