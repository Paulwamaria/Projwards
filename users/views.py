from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProjwardsRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = ProjwardsRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            messages.success(request, f'Account created for {username}')
            return redirect('home')
    else:
        form = ProjwardsRegistrationForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)    
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance = request.user)
        
        p_form = ProfileUpdateForm(instance = request.user.profile)


    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html',context)




class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile

