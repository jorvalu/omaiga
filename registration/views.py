from django.views.generic import TemplateView, FormView, RedirectView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from registration.forms import SignUpForm, EmailChangeForm
from registration.utils import default_token_generator
from registration.utils import get_user
from links.models import Link, Vote
from comments.models import Comment
from django.http import Http404

User = get_user_model()

class SignUpView(FormView):
	form_class = SignUpForm
	template_name = 'registration/signup.html'
	email_from = 'contacto@omaiga.com.sv'
	email_subject = 'registration/signup_activation_subject.txt'
	email_html = 'registration/signup_activation_email.html'
	email_txt = 'registration/signup_activation_email.txt'
	success_url = reverse_lazy('signup_activation_sent')

	def form_valid(self, form):
		kwargs = {
			'email_from': self.email_from,
			'email_subject': self.email_subject,
			'email_html': self.email_html,
			'email_txt': self.email_txt,
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

class EmailChangeView(LoginRequiredMixin, FormView):
	form_class = EmailChangeForm
	template_name = 'registration/email_change.html'
	email_from = 'contacto@omaiga.com.sv'
	email_subject = 'registration/email_change_activation_subject.txt'
	email_html = 'registration/email_change_activation_email.html'
	email_txt = 'registration/email_change_activation_email.txt'
	success_url = reverse_lazy('email_change_activation_sent')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		kwargs = {
			'email_from': self.email_from,
			'email_subject': self.email_subject,
			'email_html': self.email_html,
			'email_txt': self.email_txt,
		}
		form.send_mail(**kwargs)
		return super().form_valid(form)

class EmailChangeActivationSentView(LoginRequiredMixin, TemplateView):
	template_name = 'registration/email_change_activation_sent.html'

class EmailChangeActivationView(LoginRequiredMixin, FormView):
	redirect_url = reverse_lazy('profile')

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

class CustomPasswordResetView(PasswordResetView):
    html_email_template_name = 'registration/password_reset_email.html'
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'
    from_email = 'contacto@omaiga.com.sv'

class BaseProfileView(ListView):

	def get_profile_user(self):
		try:
			profile_user = User.objects.get(username=self.kwargs['username'])
		except:
			raise Http404("No encontrado.")
		return profile_user

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profile_user'] = self.get_profile_user()
		return context

class ProfileSentView(BaseProfileView):
	template_name = 'registration/profile_sent.html'
	ordering = ['-date']
	model = Link

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.filter(user=self.get_profile_user())[:10]
		return queryset

class ProfileVotedView(BaseProfileView):
	template_name = 'registration/profile_voted.html'
	model = Vote

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.filter(user=self.get_profile_user())[:10]
		return queryset

class ProfileCommentsView(BaseProfileView):
	template_name = 'registration/profile_comments.html'
	ordering = ['-date']
	model = Comment

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.filter(user=self.get_profile_user())[:10]
		return queryset
