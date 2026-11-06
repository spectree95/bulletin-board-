from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from main.models import Category, Product, SubCategory


GROUPS = [
    ("Электроника", "Техника", [
        ("Ноутбук для учёбы", 150000), ("Монитор 24 дюйма", 45000),
        ("Беспроводная клавиатура", 12000), ("Наушники", 18000),
        ("Планшет", 85000),
    ]),
    ("Дом", "Мебель", [
        ("Письменный стол", 35000), ("Офисное кресло", 28000),
        ("Книжная полка", 15000), ("Журнальный столик", 20000),
        ("Комод", 42000),
    ]),
    ("Спорт", "Спортинвентарь", [
        ("Горный велосипед", 95000), ("Гантели 5 кг", 10000),
        ("Коврик для йоги", 5000), ("Футбольный мяч", 7500),
        ("Роликовые коньки", 22000),
    ]),
    ("Хобби", "Книги и музыка", [
        ("Учебник Python", 6000), ("Акустическая гитара", 38000),
        ("Настольная игра", 11000), ("Набор для рисования", 9000),
        ("Сборник рассказов", 3500),
    ]),
]


class Command(BaseCommand):
    help = "Добавляет 20 демонстрационных объявлений без дубликатов."

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = get_user_model().objects.get_or_create(
            username="bulletin_demo_seed",
            defaults={"first_name": "Демо", "phone_number": "", "is_active": False},
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        elif user.is_active or user.has_usable_password():
            raise CommandError("Имя bulletin_demo_seed занято обычным аккаунтом.")

        added = 0
        for category_name, subcategory_name, items in GROUPS:
            category, _ = Category.objects.get_or_create(name=category_name)
            subcategory, _ = SubCategory.objects.get_or_create(
                category=category, name=subcategory_name,
            )
            for title, price in items:
                name = f"[ДЕМО] {title}"
                if Product.objects.filter(author=user, name=name).exists():
                    continue
                Product.objects.create(
                    category=category, subcategory=subcategory, author=user,
                    name=name, price=Decimal(price),
                    description=(
                        f"{title}. Демонстрационное объявление для проверки сайта. "
                        "Товар не продаётся. Цена условная, фотографии не добавлены."
                    ),
                )
                added += 1
        self.stdout.write(self.style.SUCCESS(f"Добавлено объявлений: {added}."))
