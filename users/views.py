from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.views.generic import FormView

from users.forms import CustomUserCreationForm


class SignUpView(FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию в нашем сервисе.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    authentication_form = CustomUserCreationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # создаём пользователя (UserCreationForm сам хеширует пароль)
        # приветственное письмо (по требованиям ДЗ и по конспекту)
        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию в нашем сервисе.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        login(self.request, user)
        return super().form_valid(form)