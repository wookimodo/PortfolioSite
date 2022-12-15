from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag
from django.core.exceptions import PermissionDenied
from .forms import PostForm
from django.utils.text import slugify

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
    form_class = PostForm

    # model = Post
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response

        else:
            return redirect('/blog/')
        
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    #  fields = ['title','hook_text','content','head_image','file_upload','category','tags']
    
    template_name = 'blog/post_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
            
        return context
    
    
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',',';')
            tags_list = tags_str.split(';')
            
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response
    

    
    def dispatch(self, request, *args , **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author: 
            return super(PostUpdate, self).dispatch(request,*args , **kwargs)
        # 권한이 없는 방문자가 타인의 포스트를 수정하려고 할 때 403 오류 메세지가 뜨게
        else:
            raise PermissionDenied
