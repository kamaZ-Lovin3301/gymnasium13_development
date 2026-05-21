from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from journal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.guest_home, name='guest_home'),
    path('login/', LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('journal/', include('journal.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)