from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Project


class ProjectListView(ListView):
    model = Project


class ProjectCreateView(CreateView):
    model = Project
    # 화면에서 입력받을 칸만 적는다. created_at은 자동으로 채워진다.
    fields = ['name', 'description', 'stack']
    success_url = reverse_lazy('home')
