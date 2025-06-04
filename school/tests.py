from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from school.models import Lesson, Course, Subscription
from users.models import CustomUser


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@mail.ru',
            username="TestUser",
            password='12345'
        )
        self.course = Course.objects.create(
            title='Тестовый курс',
            content='Курс для тестирования'
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            content='Урок для тестирования',
            course=self.course,
            owner=self.user
        )

        self.list_url = reverse('school:lessons')
        self.create_url = reverse('school:lessons_create')
        self.detail_url = reverse('school:lessons_detail', args=[self.lesson.id])
        self.update_url = reverse('school:lessons_update', args=[self.lesson.id])
        self.delete_url = reverse('school:lessons_delete', args=[self.lesson.id])

        self.valid_data = {
            "title": "Новый урок",
            "content": "Новое содержание",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=new"
        }
        self.invalid_data = {
            'title': '',
            'content': 'Невалидный урок',
            'video_url': 'http://invalid.com/video'
        }

        # Аутентификация
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_lesson_create(self):
        response = self.client.post(self.create_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        updated_data = {'title': 'Обновленный урок'}
        response = self.client.patch(self.update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')

    def test_lesson_delete(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_video_url_validation(self):
        response = self.client.post(self.create_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@mail.ru',
            username="TestUser",
            password='12345'
        )
        self.other_user = CustomUser.objects.create_user(
            email='testuser2@mail.ru',
            username="TestUser2",
            password='12345'
        )
        self.course = Course.objects.create(
            title='Тестовый курс',
            content='Курс для тестирования'
        )
        self.client.force_authenticate(user=self.user)

        self.subscribe_url = reverse('school:subscription')

        self.course_id = {
            "course_id": self.course.id
        }

        self.invalid_id = {"course_id": 999}

    def test_subscription(self):
        response = self.client.post(self.subscribe_url, self.course_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_invalid_course_id(self):

        response = self.client.post(self.subscribe_url, self.invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
