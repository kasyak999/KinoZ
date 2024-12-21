from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView
from films.views import PersonalAccount, EmailUpdateView
from films.form import CustomUserCreationForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('films.urls')),
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
    path('user/<str:username>', PersonalAccount.as_view(), name='user'),
    path('user/email/', EmailUpdateView.as_view(), name='email_update'),
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
