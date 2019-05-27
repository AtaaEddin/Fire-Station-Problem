"""
 the author : AtaaEddin, https://github.com/AtaaEddin/Fire-Station-Problem
 create at : 25 May, 2019

 description : this script is to make it easy to test the system quickly, so having a script 
 ready to fill out employee's information instead of manually writing it down in the 'employee.json' file is a good idea

"""
import random
import pandas as pd
import json

from employee import Employee

EMP_JSON = "./employees.json"

class EmployeesGenerator():
	"""
		this class generates employees randomly and save it to csv file  
	"""
	fake_emps_dir = "./data/random/fake_employees.csv"
	registers_dir = "./data/registers/employees.csv"

	def __init__(self, **kwargs):
		self.emps = {} 
		self.emps['junior'] = kwargs['junior']
		self.emps['senior'] = kwargs['senior']
		self.emps['manager'] = kwargs['manager']
		self.emps['director'] = kwargs['director']

	def _get_fake_employees(self):
		"""
			this function takes fake informations about employees which been generated using online tool
			the file is in "registers_dir" directory
		"""
		all_emps = 0
		for _,emps_num in self.emps.items():
			all_emps += emps_num

		df = pd.read_csv(self.fake_emps_dir, names=['id','first name','last name','Email','gender'], index_col=False)
		df = df[:all_emps]

		return df

	def generate(self):
		"""
			this function is where we generate all the employees, it uses Employee class
			to generate a dictionary contains lists of Employee objects.
		"""
		emps_arr_objects = {'junior': [],
							'senior': [],
							'manager': [],
							'director': [],
							}

		# add postion attribute to the employees table(DataFrame)  
		emps_df = self._get_fake_employees()
		postions = []
		for pos,emps_num in self.emps.items():
			postions.extend([pos] * emps_num)
		emps_df["postion"] = postions

		# read employees table(DataFrame) and get its attributes to create Employee objects
		for i,row in emps_df.iterrows():
			_id = row['id']
			first_name = row['first name']
			pos = row['postion']
			emps_arr_objects[pos].append(Employee(_id,first_name,pos))

		# save employees' registers
		emps_df.to_csv(self.registers_dir, index=None)

		return emps_arr_objects


# for testing purposes
if __name__ == '__main__':
	
	with open(EMP_JSON) as fjson:
		emps = json.load(fjson)

	generator = EmployeesGenerator(**emps['employees'])
	generator.generate()

	print(pd.read_csv(generator.registers_dir, index_col=False).head())