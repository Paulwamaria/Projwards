from django.urls import path
from .views import ProjectListView,ProjectDetailView,ProjectCreateView,ProjectUpdateView,ProjectDeleteView,UserProjectListView,VoteCreateView
from . import views



urlpatterns = [
    path('',ProjectListView.as_view(), name = 'home'),
    path('project/new/',ProjectCreateView.as_view(), name = 'project-create'),
    path('project/<int:pk>/',ProjectDetailView.as_view(), name = 'project-detail'),
    path('project/<int:pk>/vote',VoteCreateView.as_view(), name = 'project-vote'),
    path('project/<int:pk>/update/',ProjectUpdateView.as_view(), name = 'project-update'),
    path('project/<int:pk>/delete/',ProjectDeleteView.as_view(), name = 'project-delete'),
    path('profile/details/<str:username>/',views.display_profile, name = 'profile-detail'),
    path('user/<str:username>/',UserProjectListView.as_view(), name = 'user-projects'),
    path('api/projects/', views.ProjectList.as_view()),
    path('api/profiles/', views.ProfileList.as_view()),
    path('search/',views.search_results, name = 'search_results'),
]



