from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from registration.forms import SignUpForm, EmailChangeForm
from registration.utils import default_token_generator
from registration.utils import get_user

User = get_user_model()

class SignUpView(FormView):
	form_class = SignUpForm
	template_name = 'registration/signup.html'
	email_from = 'webmaster@misitio.com'
	email_subject = 'registration/signup_activation_subject.txt'
	email_template = 'registration/signup_activation_email.html'
	success_url = reverse_lazy('signup_activation_sent')

	def form_valid(self, form):
		kwargs = {
			'email_from': self.email_from,
			'email_subject': self.email_subject,
			'email_template': self.email_template,
		}
		form.save(**kwargs)
		return super().form_valid(form)

class SignUpActivationSentView(TemplateView):
    template_name = 'registration/signup_activation_sent.html'

class SignUpActivationView(RedirectView):
	redirect_url = reverse_lazy('link_list')

	def dispatch(self, request, *args, **kwargs):
		assert 'uidb64' in kwargs and 'token' in kwargs

		user = get_user(kwargs['uidb64'])
		token = default_token_generator.check_token(user, kwargs['token'])
		
		if user is not None and token:
			user.is_active = True
			user.save()
			login(request, user)
			messages.success(self.request, 'Tu cuenta ha sido activada satisfactoriamente.')
			return HttpResponseRedirect(self.redirect_url)
		else:
			messages.error(self.request, 'El link de activación no es válido o ha expirado.')
			return HttpResponseRedirect(self.redirect_url)

class EmailChangeView(FormView):
	form_class = EmailChangeForm
	template_name = 'registration/email_change.html'
	email_from = 'webmaster@misitio.com'
	email_subject = 'registration/email_change_activation_subject.txt'
	email_template = 'registration/email_change_activation_email.html'
	success_url = reverse_lazy('email_change_activation_sent')

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		kwargs = {
			'email_from': self.email_from,
			'email_subject': self.email_subject,
			'email_template': self.email_template,
		}
		form.send_mail(**kwargs)
		return super().form_valid(form)

class EmailChangeActivationSentView(TemplateView):
	template_name = 'registration/email_change_activation_sent.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class EmailChangeActivationView(FormView):
	redirect_url = reverse_lazy('profile')

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		assert 'uidb64' in kwargs and 'token' in kwargs and 'email_token' in kwargs

		user = get_user(kwargs['uidb64'])
		token = default_token_generator.check_token(user, kwargs['token'])
		email_token = default_token_generator.check_email_token(kwargs['email_token'])

		if user is not None and token and bool(email_token):
			user.email = email_token
			user.save()
			messages.success(self.request, 'Email actualizado satisfactoriamente.')
			return HttpResponseRedirect(self.redirect_url)
		else:
			messages.error(self.request, 'El link de confirmación no es válido o ha expirado.')
			return HttpResponseRedirect(self.redirect_url)

class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

