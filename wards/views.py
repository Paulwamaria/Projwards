from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,RedirectView
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer, ProfileSerializer
from .models import Project, Vote
from .forms import VoteForm
from users.models import Profile

# Create your views here.
def index(request):
    message = "Welcome to Prowards"

    context = {
        "message":message,
    }

    return render(request,'wards/index.html',context)

def display_profile(request,username):
    profile = Profile.objects.get(user__username= username)

    user_projects = Project.objects.filter(profile =profile).order_by('created_on')

    context={
        "profile":profile,
        "user_projects":user_projects
    }
    return render(request,'wards/profile_detail.html',context)

class ProjectListView(ListView):
    
    model = Project
    template_name='wards/index.html'
    context_object_name ='projects'
    ordering = ['-created_on']

class ProjectCreateView(LoginRequiredMixin,CreateView):
     
    model = Project
    success_url = ('/')
    fields = ['title','image','description','project_link']

    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project





class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
     
    model = Project

    fields = ['title','image','description','project_link']


    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


    def test_func(self):
        project = self.get_object()

        if self.request.user.profile == project.profile:
            return True

        return False

    def get_redirect_url(self,pk, *args, **kwargs):
        obj = get_object_or_404(Project, pk = pk)
        url= obj.get_absolute_url()
      
      
        return url


class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Project
    success_url = ('/')
    def test_func(self):
        project = self.get_object()

        if self.request.user.profile == project.profile:
            return True

        return False

class UserProjectListView(ListView):
    model = Project
    template_name='wards/profile_detail.html'
    context_object_name ='projects'
    ordering = ['-created_on']


    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        
        return Project.objects.filter(profile=user.profile).order_by('-created_on')





class VoteCreateView(LoginRequiredMixin,CreateView):
    model = Vote
    fields = ['design_votes', 'usability_votes', 'creativity_votes', 'content_votes']

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Project` instance exists
        before going any further.
        """
        self.project = get_object_or_404(Project, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class ProjectList(APIView):
    def get(self, request, format = None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many = True)
        return Response(serializers.data)



class ProfileList(APIView):
    def get(self, request, format = None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_projects, many = True)
        return Response(serializers.data)


def search_results(request):
    if 'search_project' in request.GET and request.GET["search_project"]:
        search_term = request.GET.get("search_project")
        searched_projects = Project.objects.filter(title__icontains=search_term)
        message=search_term
        return render(request, "wards/search.html", {"projects":searched_projects, "message":message})

    else:
        message = "Search term not found"

        return render(request,'wards/search.html',{"message":message})






    

