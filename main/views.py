# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, CustomUser, Like, Comment
from .forms import PostForm, CustomUserCreationForm, CommentForm, UserSearchForm

@login_required
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user__in=request.user.following.all()).order_by('-created_at')
        liked_posts = [post.id for post in posts if post.likes.filter(user=request.user).exists()]
    else:
        posts = Post.objects.all().order_by('-created_at')
        liked_posts = []
    return render(request, 'main/home.html', {'posts': posts, 'liked_posts': liked_posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def follow_user(request, pk):
    user_to_follow = get_object_or_404(CustomUser, pk=pk)
    request.user.following.add(user_to_follow)
    return redirect('user_profile', pk=pk)

@login_required
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(CustomUser, pk=pk)
    request.user.following.remove(user_to_unfollow)
    return redirect('user_profile', pk=pk)

@login_required
def user_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    num_posts = Post.objects.filter(user=user).count()
    num_following = user.following.count()
    num_followers = user.followers.count()
    posts = Post.objects.filter(user=user).order_by('-created_at')
    is_following = request.user.following.filter(pk=pk).exists()
    return render(request, 'main/user_profile.html', {
        'user': user,
        'num_posts': num_posts,
        'num_followers': num_followers,
        'num_following': num_following,
        'posts': posts,
        'is_following': is_following
        })

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('home')

@login_required
def comment_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'main/comment_post.html', {'form': form, 'post': post})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user == comment.post.user:
        comment.delete()
    return redirect('home')

def user_search(request):
    form = UserSearchForm()
    results = []
    query = ''
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Perform the search
            results = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'main/search_results.html', {'form': form, 'results': results, 'query': query})
