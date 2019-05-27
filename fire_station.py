"""
 the author : AtaaEddin, https://github.com/AtaaEddin/Fire-Station-Problem
 create at : 26 May, 2019

 description : this is the main script for the fire-station problem where we have
	employees ['juniors','seniors','managers','directors'] responseable to receive and manage 
	the incoming calls from callers, and we handled several situations in-managing calls.

	all employees,callers and calls are tracked down in csv files 

"""
from threading import Thread
from collections import deque
import numpy as np
import json
import time

from generate_employees import EmployeesGenerator
from generate_calls import CallsGenerator
from employee import save_call

# GLOBAL VARIABLES

MAX_THREADS = 4

# EMPLOYESS
EMP_JSON = "./employees.json"
LOW_PRIORITY_EMP = [] # juniors, seniors, managers
HIGH_PRIORITY_EMP =[] # managers, directors

#CALLS
calls_q = deque() 

# define a time domain to select an interval value randomly
# from the domain EX:[2's' ... 5's'] --(rand)--> 3's'  
LOWEST_TIME_INTERVAL = 0 # in sec
HIGHEST_TIME_INTERVAL = 1.5

HIGH_PRIORITY_CALLS_RATIO = .5 # %20 of calls are high-priority

# all records are holded and saved to csv files 
calls_dir = "./data/registers/calls.csv"
escalated_calls_dir = "./data/registers/escalated_calls.csv" # this is an optional addition to track a specific type of calls

def init_priority_stacks(emps):

	"""
		this function initialize two stack(list) of employees to manage two type of calls
		low-priority calls and high-priority calls

		Inputs:
			emps (type == dict) = dict keys are the employee type and its values are arrays contains Employee objects

		Outputs:
			None			
	"""

	global LOW_PRIORITY_EMP
	LOW_PRIORITY_EMP = [
						emps['junior'],
						emps["senior"],
						emps["manager"]
						]
	# flatten array
	LOW_PRIORITY_EMP = np.hstack(LOW_PRIORITY_EMP)

	global HIGH_PRIORITY_EMP
	HIGH_PRIORITY_EMP = [
						emps["manager"],
						emps["director"]
						]

	HIGH_PRIORITY_EMP = np.hstack(HIGH_PRIORITY_EMP)

def DispatchCall(calls_q):

	"""
		this function handles any call pushed to the queue(calls_q) and saves call's informations
		inside csv files

		Inputs:
			calls-q (type == deque) = send and receive json-objects between call generator and this function

		Outputs:
			None
	"""
	new_call = None

	while True:
		time.sleep(.1)

		try:
			new_call = calls_q.pop()
		except :
			new_call = None

		# handle call
		if new_call is not None:

			# low-priority and high-priority calls are handled by different employees
			if new_call["priority"] == "high":
				call = handle_call(HIGH_PRIORITY_EMP,new_call)
			if new_call["priority"] == "low":
				call = handle_call(LOW_PRIORITY_EMP,new_call)
			
			# if call is de-allocated that means call has been processed successfully
			# else either call has been esclated or system couldn't find free employee either cases call will pushed again
			if call["status"] == "deallocated":
				save_call(calls_dir,new_call)
			else:
				if call["status"] == "escalated":
					save_call(escalated_calls_dir,call) # optional 
				calls_q.append(call)

			print(new_call) 			


def handle_call(stack,new_call):

	"""
		this function gets called in DispatchCall function, its job to find the first available employee
		and allocate the call to it 

		Inputs:
			stack: (type == np.array) list of Employee objects
			new_call: (type == json) json file contians call's information

		Outputs:
			call: (type == json) call's information updated key'status' will be changed to deallocated or escalated
	"""

	for employee in stack:
		if employee.isfree:
			# lock employee
			employee.isfree = False
			# process call
			call = employee.allocate_call(new_call)
			# de-lock
			employee.isfree = True
			# return updated call to be save futher down the line
			return call			

	# couldn't find any free empoyee
	return new_call

if __name__ == "__main__":

	# init employees' objects via json file
	with open(EMP_JSON) as fjson:
		emps = json.load(fjson)

	emp_generator = EmployeesGenerator(**emps['employees'])
	all_emps = emp_generator.generate()

	# init employees stacks
	init_priority_stacks(all_emps)

	# init calls generator
	calls_gen = CallsGenerator(queue=calls_q,
							lowest_interval=LOWEST_TIME_INTERVAL,
							highest_interval=HIGHEST_TIME_INTERVAL,
							high_proirity_chance=HIGH_PRIORITY_CALLS_RATIO)


	try:
		# start generating calls using one thread
		gen_thread = calls_gen.start_generating()

		# assign some threads to run DispatchCall function
		workers_threads = []
		for i in range(MAX_THREADS):
			workers_threads.append(Thread(target=DispatchCall, args=(calls_q,)))
			workers_threads[i].start()

	except Exception as e:
		raise e
	finally:
		gen_thread.join()

		for worker in workers_threads:
			worker.join()



