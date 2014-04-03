from random import choice


class Task:
	def __init__(self, timeToComplete, skills, constraints):
		'''
		:param skills: dict f.e. { 'a':3, 'b':1 }, where literal is the name of the skill and number is expected skill level
		:param constraints: list of tasks that this task depends on
		'''
		self.time = timeToComplete
		self.skills = skills
		self.constraints = constraints

	def __str__(self):
		return str(self._id)


class Person:
	def __init__(self, skills, cost):
		'''
		:param skills: dict f.e. { 'a':3, 'b':1 }, where literal is the name of the skill and number is skill level
		'''
		self.skills = skills
		self.cost = cost

	def canDo(self, task):
		can = True
		for s in task.skills.keys():
			can &= s in self.skills and self.skills[s] >= task.skills[s]
		#print("canDo: p:{}  t:{} -> {}".format(self.cost,task.time,can))
		return can

	def __str__(self):
		return "Person " + str(self.cost)


class Project:
	def __init__(self, tasks, persons):
		self.tasks_matrix = Project.__createPersonTasksMatrix(tasks, persons)
		self.tasks = tasks
		self.persons = persons

	def getPersonsForTask(self, t):
		return self.tasks_matrix[t]

	@staticmethod
	def __createPersonTasksMatrix(tasks, persons):
		'''
		:rtype : dict of <Task, List<Person>>
		:param tasks:
		:param persons:
		'''
		r = dict()
		for t in tasks:
			l = [p for p in persons if p.canDo(t)]
			assert l  # it would mean no one can do this task
			r[t] = l
		return r

	@staticmethod
	def getPossibleTaskStartTime( t):
		time = 0
		for tt in t.constraints:
			time = max(Project.getPossibleTaskStartTime(tt), time)
		return time


class ProjectSchedule:

	class TaskAssignment:
		def __init__(self, startTime, person):
			"""
			:type person: Person
			:type startTime: int
			"""
			self.startTime = startTime
			self.person = person

		def __str__(self):
			return "<sTime:{} p:{}>".format(self.startTime, self.person._id)


	''' :type : Project'''
	project = None
	data = []

	def __init__(self, assignments, project):
		project = project if project else ProjectSchedule.project
		assert project and (len(assignments) == len(project.tasks))
		for a, t in zip(assignments, project.tasks):
			assert (not a) or (a.person.canDo(t))

		self.data = assignments
		self.project = project

	def copy(self):
		return ProjectSchedule(list(self.data), self.project)

	def _isOK(self, debug=False):
		proj = self.project
		tasks = proj.tasks
		assert len(self.data) == len(tasks)

		ok = True
		# check tasks per person + if person can do this task
		for p in proj.persons:
			personsAssignements = [(a, self._getTaskForAssignment(a)) for a in self.data if a and (a.person == p)]

			# assert can do all assigned tasks
			for (a, t) in personsAssignements:
				if not a.person.canDo(t):
					raise Exception("Person {} is unable to complete task {}".format(a.person._id, t._id))

			# check 'no timeline conflicts'
			personsAssignements2 = sorted(personsAssignements, key=lambda e: e[0].startTime)
			lastTaskEnd = 0
			for (a, t) in personsAssignements2:
				if debug: print("last: {}, current: {} --> {}".format(lastTaskEnd, a.startTime, ("OK" if a.startTime >= lastTaskEnd else "~~ !")))
				ok &= a.startTime >= lastTaskEnd
				lastTaskEnd = a.startTime + t.time

		if not ok:
			if debug: print("Not ok: timeline conflicts")
			return False

		#check precedence rules
		for task, a in zip(tasks, self.data):
			#if debug: print("\ttask{}'s constraints: {} ".format(task.time, task.constraints))
			if a:
				for constr in task.constraints:
					# assert this constraint task is finished before task from assignment starts
					constrAssign = self.data[tasks.index(constr)]
					constrFinTime = constrAssign.startTime + constr.time
					ok &= constrAssign and a.startTime >= constrFinTime
		if debug:
			print("OK!" if ok else "Not ok: precedence conflicts")

		return ok

	def _getTaskForAssignment(self, assignment):
		return self.project.tasks[self.data.index(assignment)]

	def doable(self, task): # TODO not tested
		'''
		:type task Task
		'''
		constraintsAssignements = [ a for (a,t) in zip(self.data, self.project.tasks) if t in task.constraints]
		return not ( None in constraintsAssignements)

	def getAllDoableTasks(self):  # TODO not tested
		return [ t for (a,t) in zip(self.data, self.project.tasks) if not a and self.doable(t)]

	def assign(self,task,person): # TODO not tested
		'''
		:type task Task
		:type person Person
		'''
		tasks = self.project.tasks
		ind = tasks.index(task)
		time = 0
		# check assignments for this person
		personsAssignements = [a for a in self.data if a and a.person == person]
		if personsAssignements:
			a = sorted(personsAssignements, key=lambda e: e.startTime)[-1] # last assignment
			time = a.startTime + self._getTaskForAssignment(a).time
		# check task's precedence rules
		for t in task.constraints:
			a = self.data[tasks.index(t)]
			if a: time = max(time, t.time+a.startTime)

		# assignment
		self.data[ind] = ProjectSchedule.TaskAssignment(time,person)

	def done(self):  # TODO not tested
		return sum([1 for a in self.data if a]) == len(self.project.tasks)


	@staticmethod
	def generateRandomSchedule(project, debug=True):
		r = []
		for t in project.tasks:
			ps = project.getPersonsForTask(t)
			assert ps  #someone has to do this task..
			a = ProjectSchedule.TaskAssignment(0, choice(ps))
			r.append(a)
		return ProjectSchedule(r, project)




#region tests
t1 = Task(1, {'a': 3, 'b': 2}, [])  #1,3
t2 = Task(2, {'a': 1, 'd': 2}, [])  #3
t3 = Task(3, {'c': 3}, [])  #3,4
t4 = Task(4, {}, [])  #everyone
t5 = Task(5, {}, [t1])  #everyone

p1 = Person({'a': 3, 'b': 2}, 1)  #1,4,5
p2 = Person({'a': 3, 'b': 1}, 2)  #4,5
p3 = Person({'a': 5, 'b': 5, 'c': 5, 'd': 5}, 3)  #1,2,3,4,5
p4 = Person({'a': 3, 'c': 3}, 4)  #3,4,5
p5 = Person({}, 5)  #,4,5

a1 = ProjectSchedule.TaskAssignment(0, p1)
a2 = ProjectSchedule.TaskAssignment(0, p3)
a3 = ProjectSchedule.TaskAssignment(0, p4)
a4 = ProjectSchedule.TaskAssignment(0, p2)
a5 = ProjectSchedule.TaskAssignment(0, p2)


def personTasksMatrixTest():
	tasks = [t1, t2, t3, t4, t5]
	persons = [p1, p2, p3, p4, p5]
	p = Project(tasks, persons)

	#print ("\n".join(map(str, p.tasks_matrix)))
	#for e in p.tasks_matrix:
	#	print( str(e.time) +(", ".join(map(str, p.tasks_matrix[e]))))
	countSame = lambda l1, l2: sum([1 for x in l1 if x in l2])
	lists_equal = lambda l1, l2: len(l1) == len(l2) == countSame(l1, l2)
	test = lambda i, l: lists_equal(p.getPersonsForTask(tasks[i]), l)
	assert test(0, [persons[0], persons[2]])
	assert test(1, [persons[2]])
	assert test(2, [persons[2], persons[3]])
	assert test(3, persons)
	assert test(4, persons)

	print("\t-- personTasksMatrixTest: OK !")

def generateRandomTest():
	tasks = [t1, t2, t3, t4, t5]
	persons = [p1, p2, p3, p4, p5]
	p = Project(tasks, persons)
	# ProjectSchedule.project = p

	for _ in range(100):
		e1 = ProjectSchedule.generateRandomSchedule(p, True)
		for assign in e1.data:
			assert assign.person.canDo(e1._getTaskForAssignment(assign))
	print("\t-- generateRandomTest: OK !")

def isOkTest():
	debug = False
	tasks = [t1, t2, t3, t4, t5]
	persons = [p1, p2, p3, p4, p5]
	p = Project(tasks, persons)

	# conflict - tasks at the same time
	b1 = ProjectSchedule.TaskAssignment(0, p3)
	b2 = ProjectSchedule.TaskAssignment(0, p3)
	e1 = ProjectSchedule([b1, b2, a3, a4, a5], p)
	assert not e1._isOK(debug)

	#conflict - precedence rules
	pp2 = Project([t1, t5], persons)
	b1 = ProjectSchedule.TaskAssignment(9, p1)
	b2 = ProjectSchedule.TaskAssignment(0, p3)  # depends on  t1
	e1 = ProjectSchedule([b1, b2], pp2)
	assert not e1._isOK(debug)

	#conflict - person does not have skills to do task
	b2 = ProjectSchedule.TaskAssignment(0, p3)
	e1 = ProjectSchedule([b1, b2, a3, a4, a5], p)
	b2.person = p2  # cannot do t1
	try:
		e1._isOK(debug)
		assert False
	except:
		pass  # exception is expected !

	#ok
	pp2 = Project([t1, t2, t5], persons)
	b1 = ProjectSchedule.TaskAssignment(0, p3)
	b2 = ProjectSchedule.TaskAssignment(2, p3)
	b3 = ProjectSchedule.TaskAssignment(3, p5)
	e1 = ProjectSchedule([b1, b2, b3],pp2)
	assert e1._isOK(debug)

	print("\t-- isOkTest: OK !")

#endregion


if __name__ == '__main__':
	print("### Testing ###")

	personTasksMatrixTest()
	generateRandomTest()
	isOkTest()

	print("### Testing end ###")
