from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView
from users.form import CustomUserCreationForm
from django.conf.urls.static import static


handler404 = 'users.views.page_not_found'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('films.urls')),
    path('', include('users.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path(
        'user/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
