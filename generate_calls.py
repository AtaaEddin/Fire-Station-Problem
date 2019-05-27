"""
 the author : AtaaEddin, https://github.com/AtaaEddin/Fire-Station-Problem
 create at : 25 May, 2019

 description : 
	
"""
import pandas as pd
import random
import datetime
import time
from threading import Thread

class CallsGenerator():
	"""docstring for CallsGenerator"""
	fake_callers = "./data/registers/callers.csv"

	def __init__(self, queue, lowest_interval,highest_interval, high_proirity_chance=.2):
		self.lowest_interval = lowest_interval
		self.highest_interval = highest_interval
		self.high_proirity_chance = high_proirity_chance
		self.queue = queue

		self.callers = pd.read_csv(self.fake_callers, index_col=None)

	def _assign_caller(self):
		caller_idx = random.randint(0,len(self.callers)-1)
		caller = self.callers.iloc[caller_idx]
		
		return [caller["id"],caller["first_name"]]

	def _set_call_priority(self):
		priority = None
		if random.random() <= self.high_proirity_chance:
			return "high"

		return "low"

	def _create_call(self):
		call = {
						"priority": self._set_call_priority(),
						"caller": self._assign_caller(),
						"call_time": datetime.datetime.now(),
						"status": "created",
						"handler": [],
						"handle_time": 0,
					}


		return call

	def generate(self):
		while True:
			interval = random.uniform(self.lowest_interval,self.highest_interval)
			time.sleep(interval)
			call = self._create_call()
			call["status"] = "await"
			#print(call)
			self.queue.appendleft(call)

	def start_generating(self):
		t = Thread(target=self.generate)
		t.start()
		return t


if __name__ == '__main__':
	from collections import deque
	q = deque()
	t = CallsGenerator(q,3,5).start_generating()
	t.join()