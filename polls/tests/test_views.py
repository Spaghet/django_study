import datetime

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse
from django.utils import timezone
from polls.models import Question

setup_test_environment()

def create_question(question_text, days):
    """
    Create a question based on question_text and days.
    days is positive for the future and negative for the past
    :param question_text: str
    :param days: int
    :return: Question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class IndexViewTests(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse('polls:index'))
        return self.assertIs(response.status_code, 200)

    def test_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed in the index page
        """
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 [])

    def test_with_a_past_question(self):
        """
        Questions from the past should be displayed on the index page
        :return:
        """
        create_question("Past question.", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 ["<Question: Past question.>"])

    def test_with_future_and_past_questions(self):
        """
        Even if both exist, only the past questions should exist
        :return:
        """
        create_question("Past question.", -30)
        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 ["<Question: Past question.>"])

    def test_with_two_past_questions(self):
        create_question("Past question1", -30)
        create_question("Past question2", -3)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 ["<Question: Past question2>",
                                  "<Question: Past question1>"])