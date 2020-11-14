from django import forms
from . models import Post , Comment

class PostModleForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content' , 'image' )



class CommentModelFrom(forms.ModelForm):
    body = forms.CharField(label='' , widget=forms.TextInput(attrs={'placeholder':'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)