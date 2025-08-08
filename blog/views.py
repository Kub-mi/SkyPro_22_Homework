from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from django.http import HttpResponse


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


def test_email_view(request):
    send_mail(
        'Тест Django',
        'Если ты читаешь это, то всё работает ✅',
        'your_email@gmail.com',
        ['mikhailkubrak02@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Письмо отправлено!')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            send_mail(
                subject='Статья набрала 100 просмотров!',
                message=f'Поздравляем! Ваша статья "{obj.title}" достигла 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your_email@gmail.com'],  # Заменить на твой
                fail_silently=True
            )

        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
