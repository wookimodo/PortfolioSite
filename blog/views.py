from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post
    # template_name = 'blog/post_list.html'  
    paginate_by = 3   # pagination 기능 활성화, page 당 3개 
    ordering = '-pk'
    
class PostDetail(DetailView):
    model = Post
