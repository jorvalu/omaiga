from aggregator.celery import app
from links.models import Link
import logging

@app.task
def rank_all():
	logging.info("RANK_ALL WAS CALLED")
	try:
		for link in Link.objects.all():
			link.set_rank()
			logging.info('RANK_ALL WAS EXECUTED SUCCESSFULLY')
	except:
		logging.error('RANK_ALL RETURNED AN EXCEPTION')
