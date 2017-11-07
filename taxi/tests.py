# -*- coding: utf-8 -*-
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Recruit


def create_recruit(cont_req, days):
    """
    Create a recruit with the given `cont_req` and published the
    given number of `days` offset to now (negative for recruits published
    in the past, positive for recruits that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    dep_time = time + datetime.timedelta(days=3)
    return Recruit.objects.create(path_from = 'GIST', path_to = 'Usquare', dep_time = dep_time, cont_req = cont_req, pub_date = time)


class RecruitModelTests(TestCase):
    def test_was_published_recently_with_future_Recruit(self):
        """
        was_published_recently() returns False for recruit whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_recruit = Recruit(pub_date=time)
        self.assertIs(future_recruit.was_published_recently(), False)

    def test_was_published_recently_with_old_Recruit(self):
        """
        was_published_recently() returns False for recruits whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        old_recruit = Recruit(pub_date=time)
        self.assertIs(old_recruit.was_published_recently(), False)

    def test_was_published_recently_with_recent_Recruit(self):
        """
        was_published_recently() returns True for recruits whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(days=2, hours=23, minutes=59, seconds=59)
        recent_recruit = Recruit(pub_date=time)
        self.assertIs(recent_recruit.was_published_recently(), True)

class RecruitIndexViewTests(TestCase):
    def test_no_recruits(self):
        """
        If no recruits exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('taxi:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No taxi are available.")
        self.assertQuerysetEqual(response.context['latest_recruit_list'], [])

    def test_past_recruit(self):
        """
        Recruits with a pub_date in the past are displayed on the
        index page.
        """
        create_recruit(cont_req="Past recruit.", days=-30)
        response = self.client.get(reverse('taxi:index'))
        self.assertQuerysetEqual(
            response.context['latest_recruit_list'],
            ['<Recruit: Past recruit.>']
        )

    def test_future_recruit(self):
        """
        Recruits with a pub_date in the future aren't displayed on
        the index page.
        """
        create_recruit(cont_req="Future recruit.", days=30)
        response = self.client.get(reverse('taxi:index'))
        self.assertContains(response, "No taxi are available.")
        self.assertQuerysetEqual(response.context['latest_recruit_list'], [])

    def test_future_recruit_and_past_recruit(self):
        """
        Even if both past and future recruits exist, only past recruits
        are displayed.
        """
        create_recruit(cont_req="Past recruit.", days=-30)
        create_recruit(cont_req="Future recruit.", days=30)
        response = self.client.get(reverse('taxi:index'))
        self.assertQuerysetEqual(
            response.context['latest_recruit_list'],
            ['<Recruit: Past recruit.>']
        )

    def test_two_past_recruits(self):
        """
        The recruits index page may display multiple recruits.
        """
        create_recruit(cont_req="Past recruit 1.", days=-30)
        create_recruit(cont_req="Past recruit 2.", days=-5)
        response = self.client.get(reverse('taxi:index'))
        self.assertQuerysetEqual(
            response.context['latest_recruit_list'],
            ['<Recruit: Past recruit 2.>', '<Recruit: Past recruit 1.>']
        )


class RecruitDetailViewTests(TestCase):
    def test_future_recruit(self):
        """
        The detail view of a recruit with a pub_date in the future
        returns a 404 not found.
        """
        future_recruit = create_recruit(cont_req='Future recruit.', days=5)
        url = reverse('taxi:detail', args=(future_recruit.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_recruit(self):
        """
        The detail view of a recruit with a pub_date in the past
        displays the recruit's text.
        """
        past_recruit = create_recruit(cont_req='Past Recruit.', days=-5)
        url = reverse('taxi:detail', args=(past_recruit.id,))
        response = self.client.get(url)
        print response
        self.assertContains(response, past_recruit.cont_req)
