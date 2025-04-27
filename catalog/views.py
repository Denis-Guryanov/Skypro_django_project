from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "product"


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
