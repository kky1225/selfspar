from django.urls import path

from . import views

urlpatterns = [
    # 프로젝트 목록이 selfspar의 홈 화면이다.
    path('', views.ProjectListView.as_view(), name='home'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project_create'),
]
