from django.shortcuts import render , redirect , get_object_or_404
from .models import Post , Comment
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    posts = Post.objects.all().order_by('-published_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'posts': page_obj, 'is_paginated': page_obj.has_other_pages(), 'page_obj': page_obj})


def postdetail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created_date')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            print(f"pk {request.user.pk}")
            comment.user = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/postdetail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/newblog.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-published_date')
    context = {
        'user_profile': user,
        'posts': posts,
    }
    return render(request, 'blog/profile.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        results = []
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'blog/search_results.html', context)
