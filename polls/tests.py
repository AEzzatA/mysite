from django.test import TestCase
import datetime
from polls.models import Poll
from django.core.urlresolvers import reverse
from django.utils import timezone

def create_poll(question, days):
	''' Creates a poll with the given question published the given number
	of days offset to now (negatie for polls in the past, postive for future)
	'''
	return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollMethodTests(TestCase):
	def test_was_published_recently_with_future_poll(self):
		''' was_published_recently() should return False for polls whose
		pub_date is in the future'''

		future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(), True)

class PollViewTest(TestCase):
	
    def test_index_view_with_no_polls(self):
    	"""
        If no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Polls with a pub_date in the past should be displayed on the index page.
        """
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )


    def test_index_view_with_a_future_poll(self):
    	''' Polls with a pub_date in the future should not be displayed
    	on the index page'''
    	create_poll(question="Future pill.", days=30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertContains(response, "No polls are available.", status_code=200)
    	self.assertQuerysetEqual(response.context['latest_poll_list'], [])


    def test_index_with_future_poll_and_past_poll(self):
    	'''Even if both future and past polls exist, only the past polls
    	should be displayed'''
    	create_poll(question="Past poll.", days=-30)
    	create_poll(question="Future poll.", days=30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertQuerysetEqual(
    		response.context['latest_poll_list'],
    		['<Poll: Past poll.>'])

    def test_index_with_two_past_polls(self):
    	create_poll(question='Past poll 1.', days=-30)
    	create_poll(question='Past poll 2.', days=-3)
    	response = self.client.get(reverse('polls:index'))
    	self.assertQuerysetEqual(
    		response.context['latest_poll_list'],
    		['<Poll: Past poll 2.>', '<Poll: Past poll 1.>'])

class PollIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_poll(self):
		''' Detail view of a poll with a pub_date in the future should
		return a 404 not found'''
		future_poll = create_poll(question='Future poll.', days=5)
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		''' The detail view of a poll with a pub_date in the past should
		display the poll's question'''
		past_poll = create_poll(question='Past poll.', days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
		self.assertContains(response, past_poll.question, status_code=200)