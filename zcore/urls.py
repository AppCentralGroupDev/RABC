"""zcore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home, name="home"),
    path('add-new-group', views.add_new_group, name="add_new_group"),
    path("assign_user/<int:user_id>", views.assign_user, name="assign_user"),
    path("add_user_group/<str:group_name>/<int:user_id>", views.add_user_group, name="add_user_group"),
    path("remove_user_group/<str:group_name>/<int:user_id>", views.remove_user_group, name="remove_user_group"),
    path('add-model', views.add_model, name="add_model"),
    path('approve-user-account/<int:user_id>', views.approve_user_account, name="approve_user_account"),
    path('customer', views.customer_page, name="customer"),
    # path('page1/', views.page1, name="page1"),
    # path('page2/', views.page2, name="page2"),
    path('pages/<str:page_name>', views.pages, name="pages"),
    # path('manager/', views.manager_page, name="manager"),
    # path('admin-page/', views.admin_page, name="admin_page"),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
