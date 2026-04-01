from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from journal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('journal/', include('journal.urls')),
]