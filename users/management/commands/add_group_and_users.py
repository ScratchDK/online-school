from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import CustomUser
from django.core.management import call_command


class Command(BaseCommand):
    help = "Добавляет группу moders и троих пользователей с разными правами"

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка существующих данных...")

        # Удаляем всех пользователей, кроме суперпользователей
        CustomUser.objects.filter(is_superuser=False).delete()

        # Удаляем все группы
        Group.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Старые данные успешно удалены!"))

        call_command("loaddata", "groups_users_fixture.json")
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))
