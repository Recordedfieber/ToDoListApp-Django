from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import TodoTaskForm
from .models import TodoTask


# class CustomLoginView(LoginView):
#    template_name = 'login.html'
#    fields = '__all__'
#    redirect_authenticated_user = True
#    def get_success_url(self) -> str:
#        return reverse_lazy('login')

# @login_required(login_url='login')
# def dashboard(request):
#    # Get the count of incomplete tasks
#    incomplete_tasks_count = TodoTask.objects.filter(user=request.user, task_status=False).count()
#
#    return render(request, 'dashboard.html', {'count': incomplete_tasks_count})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):

        return reverse_lazy('task-list')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        # Log the user in after registration
        user = form.save()
        login(self.request, user)

        messages.success(self.request, 'Account successfully registered.')
        # Calls the parent class's form_valid method after user creation
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskListView(ListView):
    model = TodoTask
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TodoTask.objects.filter(user=self.request.user).order_by('task_priority')
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["count"] = context.get('tasks').filter(task_status=False).count()
        else:
            context["count"] = 0
        return context


@login_required(login_url=reverse_lazy('login'))  # Redirects to login page if not authenticated / temporate comment
def task_list_view(request):
    tasks = TodoTask.objects.filter(user=request.user).order_by('task_priority')
    return render(request, 'task_list.html', {'tasks': tasks})


def hello_world():
    return HttpResponse("Hello World!")


@login_required(login_url=reverse_lazy('login'))  # Redirects to login page if not authenticated
def create_task(request):
    if request.method == 'POST':
        form = TodoTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the user to the task
            form.save()
            return redirect('task-list')
    else:
        form = TodoTaskForm()
    return render(request, 'task_form.html', {'form': form})


def toggle_task_status(request, task_id):
    task = TodoTask.objects.get(pk=task_id)
    task.task_status = not task.task_status
    task.save()
    return HttpResponseRedirect(reverse('task-list'))


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoTask
    template_name = 'task_form.html'
    fields = ['task_title', 'task_priority', 'task_due_date', 'task_status']
    success_url = reverse_lazy('task-list')  # Redirect to the task list view


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoTask
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
