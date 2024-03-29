from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode = True)
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return f'/blog/category/{self.slug}/'
  
  class Meta:
    verbose_name_plural = 'categories'
    
class Tag(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode = True)
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return f'/blog/tag/{self.slug}/'
  
class Post(models.Model):
  title = models.CharField(max_length=30)
  hook_text = models.CharField(max_length=100, blank=True)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True) # add 할 때의 시간
  updated_at = models.DateTimeField(auto_now=True)  # update 할 때의 시간
  head_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank=True)
  file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank=True)
  author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
  tags = models.ManyToManyField(Tag, blank=True)
  
  # 모델에 정의돼있는 함순데, 오버라이딩한 것.
  def get_absolute_url(self):
    return f'/blog/{self.pk}/'

  def __str__(self):
    return f'[{self.pk}--{self.title} :: {self.author}]'
  
  def get_file_name(self):
    return os.path.basename(self.file_upload.name)

  def get_file_ext(self):
    return self.get_file_name().split('.')[-1]
