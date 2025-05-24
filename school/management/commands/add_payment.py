from django.core.management.base import BaseCommand
from school.models import Payment, Course
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Добавляет пару курсов и их оплату'

    def handle(self, *args, **kwargs):
        # Удаление всех существующих курсов и платежей
        Course.objects.all().delete()
        Payment.objects.all().delete()

        call_command('loaddata', 'course_fixture.json')
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))

        call_command('loaddata', 'payment_fixture.json')
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
