from django.contrib import admin
from .models import Post, Category

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
  # 입력한 그대로 slug에 기록이 되도록.
  prepopulated_fields = {'slug':('name',) }

admin.site.register(Category, CategoryAdmin)