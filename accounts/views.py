from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm

def register(req):
    if req.user.is_authenticated: return redirect('post_list')
    
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            messages.success(req, f'Welcome, {user.username}!')
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(req, 'accounts/register.html', {'form': form})

@login_required
def profile(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            messages.success(req, 'Profile updated')
            return redirect('profile')
    else:
        form = ProfileForm(instance=req.user)
        
    ctx = {
        'form': form, 
        'post_count': req.user.posts.count(), 
        'comment_count': req.user.comment_set.count()
    }
    return render(req, 'accounts/profile.html', ctx)

def post_list(req):
    q = req.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(req, 'blog/post_list.html', {'posts': posts, 'q': q})

def post_detail(req, pk):
    p = get_object_or_404(Post, pk=pk)
    
    if req.method == 'POST':
        if not req.user.is_authenticated: return redirect('login')
        form = CommentForm(req.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = p
            c.author = req.user
            c.save()
            return redirect('post_detail', pk=p.pk)
    else:
        form = CommentForm()
        
    return render(req, 'blog/post_detail.html', {'post': p, 'comments': p.comments.all(), 'form': form})

@login_required
def post_create(req):
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = req.user
            p.save()
            return redirect('post_detail', pk=p.pk)
    else:
        form = PostForm()
    return render(req, 'blog/post_form.html', {'form': form})

@login_required
def post_update(req, pk):
    p = get_object_or_404(Post, pk=pk)
    if p.author != req.user: return redirect('post_detail', pk=pk)
    
    if req.method == 'POST':
        form = PostForm(req.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=p.pk)
    else:
        form = PostForm(instance=p)
    return render(req, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(req, pk):
    p = get_object_or_404(Post, pk=pk)
    if p.author != req.user: return redirect('post_detail', pk=pk)
        
    if req.method == 'POST':
        p.delete()
        return redirect('post_list')
        
    return render(req, 'blog/post_confirm_delete.html', {'post': p})

@login_required
def post_like(req, pk):
    p = get_object_or_404(Post, pk=pk)
    if p.likes.filter(id=req.user.id).exists():
        p.likes.remove(req.user)
    else:
        p.likes.add(req.user)
    return redirect('post_detail', pk=pk)
