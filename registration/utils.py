from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.crypto import constant_time_compare, salted_hmac
from django.contrib.auth import get_user_model

class DefaultTokenGenerator(PasswordResetTokenGenerator):
	"""
	Extends PasswordResetTokenGenerator to add functionality of securely sending 
	an email address via email_token, so that the email_change views doesn't need
	to touch the database
	"""
	def _make_hash_value(self, user, timestamp):
		return str(user.pk) + str(timestamp) + str(user.is_active) + str(user.email)

	def make_email_token(self, email):
		return self._make_email_token(email)

	def _make_email_token(self, email):
		urlsafe_email = urlsafe_base64_encode(email.encode()).decode()
		hash_string = salted_hmac(
			self.key_salt,
			urlsafe_email,
			secret=self.secret,
		).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
		return "%s-%s" % (urlsafe_email, hash_string)

	def check_email_token(self, token):
		if not (token):
			return False
		try: # parse the token
			email_b64, _ = token.split("-") 
		except ValueError:
			return False
		try: # convert base64 email to string
			email_str = urlsafe_base64_decode(email_b64).decode()
		except ValueError:
			return False
		# Check that the email has not been tampered with
		if not constant_time_compare(self._make_email_token(email_str), token):
			return False
		return email_str

default_token_generator = DefaultTokenGenerator()

User = get_user_model()
def get_user(uidb64):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	return user
