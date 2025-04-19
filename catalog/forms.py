from django import forms
from django.core.exceptions import ValidationError

from .models import Product


def validate_image(image):
    # Проверка формата файла
    if not image.name.endswith((".png", ".jpg", ".jpeg")):
        raise ValidationError("Поддерживаемые форматы изображений: JPEG или PNG.")

    # Проверка размера файла (5 МБ)
    if image.size > 5 * 1024 * 1024:  # 5 МБ
        raise ValidationError("Размер файла не должен превышать 5 МБ.")


class ProductForm(forms.ModelForm):
    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "image",
        ]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            validate_image(image)
        return image

    def clean_name(self):
        name = self.cleaned_data.get("name")
        self.validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        self.validate_forbidden_words(description)
        return description

    def validate_forbidden_words(self, text):
        text_lower = text.lower()
        for word in self.forbidden_words:
            if word in text_lower:
                raise forms.ValidationError(f"Слово '{word}' недопустимо.")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if int(price) is not None and int(price) < 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применение стилей к полям формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",  # Используйте ваши классы CSS
                    "placeholder": f"Введите {field.label}",  # Подсказка
                }
            )
