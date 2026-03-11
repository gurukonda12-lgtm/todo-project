from django.contrib import admin
from todo.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'completed', 'date_created')
    list_filter = ('priority', 'completed', 'date_created')
    search_fields = ('title', 'user__username')