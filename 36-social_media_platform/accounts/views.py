from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.all().order_by('-created_at')
    
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'accounts/profile.html', context)