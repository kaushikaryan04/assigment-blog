
from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug']
        widgets = {
            'content':forms.Textarea(attrs = {'rows':1 , 'cols' : 100})
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
           'content': forms.Textarea(attrs={'rows':1, 'cols':100}),
         }
