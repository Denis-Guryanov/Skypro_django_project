from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/create_post.html"
    success_url = reverse_lazy("blog:post_detail")  # Переадресация на детали записи

    def form_valid(self, form):
        # Устанавливаем текущую дату и время создания
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем success_url для динамической переадресации на созданную запись
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Увеличиваем счетчик просмотров
        self.object.views_count += 1
        self.object.save()
        return context


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # Ограничиваем количество постов на странице

    def get_queryset(self):
        # Фильтруем только опубликованные посты
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/edit_post.html"
    context_object_name = "post"

    def get_success_url(self):
        # Переадресация на страницу деталей после успешного редактирования
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy(
        "blog:post_list"
    )  # Переадресация на список постов после удаления
    template_name = "blog/post_list.html"
