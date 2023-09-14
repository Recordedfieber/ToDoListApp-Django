from django.urls import path, reverse_lazy

from . import views
from .views import TaskListView, TaskUpdateView, TaskDeleteView, hello_world, create_task, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),
    path('register/', RegisterPage.as_view(), name="register"),
    path('', TaskListView.as_view(), name='task-list'),
    path('task/new/', create_task, name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/hello/', hello_world, name='helloworld'),
    path('task/<int:task_id>/toggle-status/', views.toggle_task_status, name='toggle-task-status'),
]
