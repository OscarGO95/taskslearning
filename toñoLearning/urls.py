"""toñoLearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from taskLearning.views import Views
from toñoLearning import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createTask', Views.loadTaksGUI),
    path('getasignatura', Views.getAsignatura),
    path('getTemas', Views.getTemas),
    path('getContenidos', Views.getContenidos),
    path('uploadTask', Views.uploadTak),
    path('verifyTasks/<int:id>', Views.verifyTasks),
    path('dashboardStudent', Views.loadDash),
    path('dashboardStudent/games/<int:id>', Views.loadGame),
    path('searchTask', Views.getTask),
    path('getsizetask/<int:id>', Views.getNumberTask),
    path('getStudents', Views.getStudents),
    path('asignarjuego', Views.asignGame),
    path('indexSnake', Views.rutainutil),
    path('dashboardTeacher/<int:id>', Views.dashboardTeacher)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
