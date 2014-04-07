from z2.Entity import ProjectSchedule

# duration optimization
class Evaluate_Time:

	def __call__(self, s):
		'''
		:type s ProjectSchedule
		:returns schedule execution duration
		'''
		return max([ (s._getTaskForAssignment(a).time + a.startTime) for a in s.data if a])

	#def __call__(self, state, task, resources):
	def getBestAssignment(self, state, task, resources):
		'''
		:type state ProjectSchedule
		:type task Task
		:type resources list[Person]
		:returns best resource for the given task
		'''
		best = None
		best_time = 0
		ns = state.copy()
		for r in resources:
			ns.assign(task, r)
			assert ns._isOK()
			# measure time
			time = self.__call__(ns)
			if not best or time < best_time:
				best_time = time
				best = r
		assert best
		return best, best_time

# cost optimization
class Evaluate_Cost:

	def __call__(self, s):
		'''
		:type s ProjectSchedule
		:returns total cost of the schedule
		'''
		p = s.project
		return sum( [ (t.time*a.person.cost) for (t,a) in zip( p.tasks, s.data) if a] )


	def getBestAssignment(self, state, task, resources):
		'''
		:type state ProjectSchedule
		:type task Task
		:type resources list[Person]
		'''
		r = sorted(resources, key=lambda p: p.cost)[0] # : )
		ns = state.copy()
		ns.assign(task, r)
		rScore = self.__call__(ns)
		return r,rScore
