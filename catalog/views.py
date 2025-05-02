from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .forms import ProductForm
from .models import Product, Category
from .services import get_product_from_cache, get_products_by_category


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "object_list"  # Изменено с "product" на "object_list"

    def get_queryset(self):
        return get_product_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Добавляем список категорий
        return context


class ProductsByCategoryView(ListView):
    template_name = "catalog/product_list.html"  # Используем тот же шаблон
    context_object_name = "object_list"

    def get_queryset(self):
        self.category_slug = self.kwargs.get("category_slug")
        return get_products_by_category(self.category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.category_slug)
        context["categories"] = Category.objects.all()
        context["current_category"] = category  # Для подсветки активной категории
        context["title"] = f'Продукты в категории "{category.name}"'
        return context


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    success_url = reverse_lazy("catalog:product_list")
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматическая привязка владельца
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем success_url для динамической переадресации на созданную запись
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = "product"
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_list.html"
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.owner == request.user
        is_moderator = request.user.has_perm("catalog.can_unpublish_product")

        if not (is_owner or is_moderator):
            raise PermissionDenied("Недостаточно прав для удаления.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.has_perm("catalog.delete_product"):
            return reverse("catalog:product_list")
        raise PermissionDenied


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user.has_perm("catalog.can_unpublish_product"):
            product.is_published = False
            product.save()
        return redirect("catalog:product_list")


class ContactFeedbackView(View):
    def get(self, request):
        # Отображаем форму
        return render(request, "catalog/contact.html")

    def post(self, request):
        # Обработка отправки формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}! Сообщение получено.")
