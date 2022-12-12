from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # add 할 때의 시간
    updated_at = models.DateTimeField(auto_now=True)     # update 할 때의 사간
    
    # 모델에 정의돼있는 함순데, 오버라이딩한 것.
    def get_absolute_url(self):
      return f'/blog/{self.pk}/'

    def __str__(self):
        return f'[{self.pk}--{self.title}]'