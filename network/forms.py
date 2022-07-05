from django import forms
from network.models import Post, Follower, User


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder':'Enter'}),label='Enter your Post')
    class Meta:
        model = Post
        fields = [
            'content'
        ]
    
    

 