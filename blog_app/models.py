from django.db import models
from django.urls import reverse
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    preview_image = models.ImageField(
        upload_to="blog_previews/", verbose_name="Превью", blank=True, null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Meta:
    verbose_name = "публикация"
    verbose_name_plural = "публикации"
    ordering = ["name"]
