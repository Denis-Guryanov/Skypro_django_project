from django.http import HttpResponse
from django.shortcuts import render
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        # Устанавливаем текущую дату и время создания
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем success_url для динамической переадресации на созданную запись
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = "product"
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_list.html"
    success_url = reverse_lazy("catalog:product_list")


class ContactFeedbackView(View):
    def get(self, request):
        # Отображаем форму
        return render(request, "catalog/contact.html")

    def post(self, request):
        # Обработка отправки формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}! Сообщение получено.")
