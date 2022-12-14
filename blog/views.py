from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag

# Create your views here.
class PostList(ListView):
    model = Post
    # template_name = 'blog/post_list.html'  
    paginate_by = 3   # pagination 기능 활성화, page 당 3개 
    ordering = '-pk'
    
    def get_context_data(self, **kwargs):
        # get_context_data에서 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context = super(PostList,self).get_context_data()
        # 원하는 쿼리셋을 만들어 딕셔너리 형태로 context에 담은 것.
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()        
        return context
    
def category_page(request, slug):
    
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:           
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )

def tag_page(request, slug):        
    
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )
    
class PostDetail(DetailView):
    
    model = Post
    
    def get_context_data(self, **kwargs):
        # get_context_data에서 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context = super(PostDetail,self).get_context_data()
        # 원하는 쿼리셋을 만들어 딕셔너리 형태로 context에 담은 것.
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()   
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')
