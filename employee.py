"""
 the author : AtaaEddin, https://github.com/AtaaEddin/Fire-Station-Problem
 create at : 25 May, 2019

 description : this scripts generally holds everything has to do with employees' attributes 

"""
import datetime
import time
import pandas as pd
import numpy as np
import random
import os

call_switching_chance = .1
calls_register_dir = "./data/registers/calls.csv"

class Employee(object):
	"""
		Employee class holds some of fire-station's workers Information, the full
		workers' records holded at "data/registers" and this class handles calls for the
		fire-station department. 
	"""
	

	def __init__(self, Id, first_name, postion, handle_time = 1):
		self.id = Id
		self.first_name = first_name
		self.postion = postion
		self.handle_time = handle_time
		self.isfree = True

	def get_info(self):
		return [self.id,self.first_name,self.postion]

	def allocate_call(self, call):
		# it is convienient to force sleep for couple of secs to simulate that 
		# employee is taking some time to handle the call
		time.sleep(self.handle_time)

		self.call = call
		self.call["status"] = "allocated"
		self.call["handler"] = [self.id,self.first_name,self.postion]

		#chance to escalate call to high-priority
		if self.call["priority"] == "low" and random.random() <= call_switching_chance:
			self.call["status"] = "escalated"
			self.call["priority"] = "high"
			self.call["handler"] = []


		if self.call["status"] != "escalated":
			self.deallocate_call()

		return self.call


	def deallocate_call(self):
		# again the employee taking some time to register the call in the database(csvfile)
		time.sleep(self.handle_time)
		self.call["status"] = "deallocated"
		self.call["handle_time"] = datetime.datetime.now()
		

def save_call(calls_register_dir, call):
	"""
		this function read the csv file add new row(call's information) and then save it again
	"""
	if call is None:
		return False

	if os.path.isfile(calls_register_dir):
		call_registers = pd.read_csv(calls_register_dir, index_col=False)	
	else:
		call_registers = pd.DataFrame(
			columns=["priority","caller","call_time","status","handler","handle_time"])
	
	call_registers = call_registers.append(call, ignore_index=True)

	call_registers.to_csv(calls_register_dir, index=None)

	return True

