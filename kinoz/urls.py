from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
# Добавьте новые строчки с импортами классов.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from films.views import personal_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('films.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path(
        'user/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('films:index'),
        ),
        name='registration',
    ),
    path('user/<str:username>', personal_account.as_view(), name='user')
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
