from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from catalog.models import Product


class HomeListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactFeedbackView(View):
    def get(self, request):
        # Отображаем форму
        return render(request, "catalog/contact.html")

    def post(self, request):
        # Обработка отправки формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}! Сообщение получено.")
