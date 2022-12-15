from django.contrib import admin
from .models import Post, Category, Tag
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
  # 입력한 그대로 slug에 기록이 되도록.
  prepopulated_fields = {'slug':('name',) }

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
  # 입력한 그대로 slug에 기록이 되도록.
  prepopulated_fields = {'slug':('name',) }
  
admin.site.register(Tag, TagAdmin) 

# admin site에 summernote 적용
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    
admin.site.register(Post, PostAdmin)