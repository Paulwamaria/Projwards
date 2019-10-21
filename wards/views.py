from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,RedirectView
from django.http import HttpResponse
from .models import Project, Vote
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

    context={
        "profile":profile
    }
    return render(request,'users/profile_detail.html',context)

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
    template_name='wards/index.html'
    context_object_name ='projects'
    ordering = ['-created_on']


    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Project.objects.filter(profile=user.profile).order_by('-created_on')



    

