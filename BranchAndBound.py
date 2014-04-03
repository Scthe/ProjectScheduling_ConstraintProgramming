from Entity import Project,Person,Task, ProjectSchedule

class Node:
	__parent = None
	__assignment = None
	__children = []


class branchAndBound:

	def __init__(self, p, bestAssignEvaluator):
		"""
		:type p: Project
		"""
		for t in p.tasks:
			t._possibleStartTime = Project.getPossibleTaskStartTime(t)
		unscheduledTasks = sorted(p.tasks, key=lambda e:e._possibleStartTime)
		tasksLen = len(p.tasks)

		while tasksLen>0:
			tasks = getAvailableTasks()




			tasksLen -= 1

	def assignmentsPermutation(self, state, tasks):
		res = []







		return res

















# reasons to discard branch:
#	- it's highest possible value is lower than lowest of other branch
#	- min==max
#	-? the other branch has much higher min-max difference, where max is so big that the current branch is not really changing it's values regardles of the children nodes