from django import forms
from network.models import Post, Comment, Follower, User


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            'content'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comments',
        ]
        widgets = {
            'comments' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'put a comment',
        })}