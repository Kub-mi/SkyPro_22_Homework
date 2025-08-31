from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

GROUP_NAME = "Модератор продуктов"
PERMS = [
    ("catalog", "can_unpublish_product"),  # кастомное право из Meta.permissions
    ("catalog", "delete_product"),         # стандартное право на удаление
]

class Command(BaseCommand):
    help = "Создаёт группу модераторов и назначает права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name=GROUP_NAME)

        product_ct = ContentType.objects.get_for_model(Product)
        assigned = 0

        for app_label, codename in PERMS:
            try:
                perm = Permission.objects.get(
                    content_type=product_ct, codename=codename
                )
            except Permission.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f"Право {app_label}.{codename} не найдено. "
                    f"Убедись, что миграции применены (manage.py migrate)."
                ))
                continue
            group.permissions.add(perm)
            assigned += 1

        group.save()
        self.stdout.write(self.style.SUCCESS(
            f"Группа «{GROUP_NAME}» готова, назначено прав: {assigned}"
        ))
