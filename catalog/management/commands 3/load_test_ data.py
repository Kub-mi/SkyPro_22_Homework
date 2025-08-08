from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаляет старые данные и добавляет тестовые категории и продукты'

    def handle(self, *args, **kwargs):
        self.stdout.write('Удаляю старые данные...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Создаю категории...')
        fruits = Category.objects.create(name='Фрукты', description='Список фруктов')
        vegetables = Category.objects.create(name='Овощи', description='Список овощей')

        self.stdout.write('Создаю продукты...')
        Product.objects.create(name='Банан', description='Плод банана', price=29.00, category=fruits)
        Product.objects.create(name='Баклажан', description='Плод баклажана', price=28.00, category=vegetables)

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены'))