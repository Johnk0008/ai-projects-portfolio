from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'posts/public_home.html')
    
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'posts/home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created!')
    return redirect('home')