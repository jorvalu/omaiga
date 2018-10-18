from comments.models import Comment, Point
from django import forms

class CommentForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), label='Comentario:')

	class Meta:
		model = Comment
		fields = ('text',)

class PointForm(forms.ModelForm):
	class Meta:
		model = Point
		fields = ('value',)
