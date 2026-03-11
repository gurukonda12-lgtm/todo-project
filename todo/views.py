from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Todo.objects.filter(user=user)
        return Todo.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ===================== User Views =====================
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# ===================== Todo Views =====================
@login_required(login_url='login')
def home(request):
    todos = Todo.objects.filter(user=request.user).order_by('-date_created')

    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        Todo.objects.create(user=request.user, title=title, priority=priority, due_date=due_date)
        return redirect('home')

    return render(request, 'todo.html', {'todos': todos})

@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('home')

@login_required(login_url='login')
def toggle_complete(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('home')


@login_required(login_url='login')
def edit_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)

    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.priority = request.POST.get('priority')
        todo.due_date = request.POST.get('due_date')
        todo.save()
        return redirect('home')

    return render(request, 'edit_todo.html', {'todo': todo})

# ===================== REST API =====================
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)