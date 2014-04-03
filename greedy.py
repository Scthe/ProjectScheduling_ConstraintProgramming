from Entity import Project,Person,Task, ProjectSchedule
from z2.Evaluate import Evaluate_Time, Evaluate_Cost

def greedySchedule(p, bestAssignEvaluator):
	"""
	:type p: Project
	"""
	unscheduledTasks = list(p.tasks)
	state = ProjectSchedule([None for _ in range(len(p.tasks))])
	while unscheduledTasks:
		bestNextScore = -1
		bestNextTask, bestNextResource = None, None
		# select best task to assign resources next
		for task in unscheduledTasks:
			if state.doable(task):
				resources = p.getPersonsForTask(task)
				bestR, bestScore = bestAssignEvaluator.getBestAssignment(state, task, resources)
				if not bestNextTask or bestScore < bestNextScore:
					bestNextResource = bestR
					bestNextScore = bestScore
					bestNextTask = task
		unscheduledTasks.remove(bestNextTask)
		state.assign(bestNextTask, bestNextResource)

	assert state._isOK() and state.done()
	et = Evaluate_Time()
	ec = Evaluate_Cost()
	print( "Project: time-{}, cost-{}".format( et(state), ec(state) ))

if __name__ == '__main__':
	pass