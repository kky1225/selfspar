from django.urls import path

from . import views

urlpatterns = [
    # 프로젝트 목록이 selfspar의 홈 화면이다.
    path('', views.ProjectListView.as_view(), name='home'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path(
        'projects/<int:project_pk>/targets/new/',
        views.TargetKindSelectView.as_view(),
        name='target_kind_select',
    ),
    path(
        'projects/<int:project_pk>/targets/new/<str:kind>/',
        views.TargetCreateView.as_view(),
        name='target_create',
    ),
]
