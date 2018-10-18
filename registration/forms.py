from registration.utils import default_token_generator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django import forms

User = get_user_model()

class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, **kwargs):

		# save user in inactive state
		user = super().save(commit=False)
		user.is_active = False
		user.save()

		# send activation email
		email_subject = kwargs['email_subject']
		email_from = kwargs['email_from']
		email_to = user.email
		email_template = kwargs['email_template']
		email_message = render_to_string(email_template, {
			'user': user.username,
			'domain': settings.DEFAULT_DOMAIN,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token': default_token_generator.make_token(user),
		})
		send_mail(email_subject, email_message, email_from, ['email_to'])

class EmailChangeForm(forms.Form):
	email1 = forms.EmailField(label="Email nuevo", max_length=254, error_messages={'invalid': ("Email inválido.")})
	email2 = forms.EmailField(label="Email nuevo (otra vez)", max_length=254, error_messages={'invalid': ("Email inválido.")})
	password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

	# makes the request available (to authenticate user)
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super().__init__(*args, **kwargs)

	def clean(self):
		username = self.request.user.username
		password = self.cleaned_data.get('password')

		validation_errors = []

		if 'email1' in self.cleaned_data and 'email2' in self.cleaned_data:
			email1 = self.cleaned_data['email1']
			email2 = self.cleaned_data['email2']
			if email1 != email2:
				email_match_error = forms.ValidationError("Los emails ingresados no coinciden. Ingrésalos nuevamente.")
				validation_errors.append(email_match_error)
			else:
				try:
					User.objects.get(email=email1)
					email_exists_error = forms.ValidationError("El email ingresado ya está siendo utilizado.")
					validation_errors.append(email_exists_error)
				except User.DoesNotExist:
					pass

		if username is not None and password:
			self.user_cache = authenticate(username=username, password=password)
			if self.user_cache is None:
				password_error = forms.ValidationError("La contraseña utilizada no es correcta.")
				validation_errors.append(password_error)

		if validation_errors:
			raise forms.ValidationError(validation_errors)

		return self.cleaned_data

	def send_mail(self, **kwargs):
		user = self.request.user
		email_subject = kwargs['email_subject']
		email_from = kwargs['email_from']
		email_to = self.cleaned_data['email1']
		email_template = kwargs['email_template']
		email_message = render_to_string(email_template, {
			'user': user.username,
			'domain': settings.DEFAULT_DOMAIN,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token': default_token_generator.make_token(user),
			'email_token': default_token_generator.make_email_token(email_to),
		})
		send_mail(email_subject, email_message, email_from, ['email_to'])





