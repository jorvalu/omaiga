from links.models import Link, Vote
from django import forms

class LinkForm(forms.ModelForm):
	class Meta:
		model = Link
		exclude = ('rank', 'user', 'date')
		labels = {
			'url': 'Link:',
			'title': 'Titular:',
			'description': 'Descripción:',
			'category': 'Categoría'
		}
		help_texts = {
			'url': 'Pega el enlace de la noticia',
			'title': 'Máximo 120 caracteres',
			'description': 'Describe con fidelidad el contenido del enlace (20 - 500 caracteres)',
			'category': 'Selecciona una categoría',
		}

class VoteForm(forms.ModelForm):
	class Meta:
		model = Vote
		exclude = ('user', 'link')