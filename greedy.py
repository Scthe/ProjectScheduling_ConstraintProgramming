from Entity import Project,Person,Task, ProjectSchedule

# duration optimization
class Evaluate_Time:

	def _measureTime(self, s):
		'''
		:type s ProjectSchedule
		'''
		return max([(s.getTaskForAssignment(a).time + a.startTime) for a in s.data if a])

	def __call__(self, state, task, resources):
		'''
		:type state ProjectSchedule
		:type task Task
		:type resources list[Person]
		'''
		best = None
		best_time = 0
		for r in resources:
			ns = state.copy()
			ns.assign(task,r)
			assert ns.isOK()
			# measure time
			time = self.measureTime(ns)
			if time < best_time or (not best):
				best_time = time
				best = r
		assert best
		return best

# cost optimization
class Evaluate_Cost:

	def _measureCost(self, s):
		'''
		:type s ProjectSchedule
		'''
		p = ProjectSchedule.project
		return sum( [ (t.time*a.person.cost) for (t,a) in zip( p.tasks, s.data)] )


	def __call__(self, state, task, resources):
		'''
		:type state ProjectSchedule
		:type task Task
		:type resources list[Person]
		'''
		return sorted(resources, key=lambda p: p.cost)[0] # : )


def greedySchedule(p, bestAssignEvaluator):
	"""
	:type p: Project
	"""
	unscheduledTasks = list(p.tasks) # sort of possible start time ?
	state = ProjectSchedule([None for _ in range(len(p.tasks))])
	while unscheduledTasks:
		#t = choice(unscheudledTasks) # :) , remember to remove
		task = unscheduledTasks.pop(0)
		resources = p.getPersonsForTask(task)
		best = bestAssignEvaluator(state, task, resources)
		state.assign(task, best)

	assert state._isOK()
	et = Evaluate_Time()
	ec = Evaluate_Cost()
	print( "Project: time-{}, cost-{}".format( et._measureTime(state), ec._measureCost(state) ))

if __name__ == '__main__':
	print(type([]))
	pass