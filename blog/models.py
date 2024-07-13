from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model) :
    title = models.CharField(max_length = 100 , null= False , blank = False)
    content = models.TextField(null = False , blank = False )
    author = models.ForeignKey(User , on_delete= models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self) :
        return self.title
    
    @staticmethod
    def fillModel() :
        for i in range(50) :
            post = Post()
            post.title = f"Post {i}"
            post.content = f"Content of Post {i}"
            post.author = User.objects.get(id = 1)
            post.save()

class Comment(models.Model) :
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.TextField(null = False , blank = False)
    created_date = models.DateTimeField(auto_now_add=True)
