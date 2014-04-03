from Entity import Project,Person,Task, ProjectSchedule
from z2.Evaluate import Evaluate_Time, Evaluate_Cost

class Permutator():

	eval = []
	bestState, bestScore = None, -1 # TODO assumed only one state can be the best, use list instead !

	def __init__(self, bestAssignEvaluator):
		self.eval = bestAssignEvaluator

	def __expand(self, state, i=0):
		# get task to ponder about
		task = self.taskSelection[i]
		if not task:
			# ah ! no more tasks - we can eval current solution
			score = self.eval( state)
			if (not self.bestState) or (score < self.bestScore):
				self.bestState = state # side effects !
				self.bestScore = score # well, we could use some nice return etc, but side effects are simpler..
		else:
			ns = state.copy()
			# get resources list for the task
			resources = state.project.getPersonsForTask(task)
			# try to fit all possible resources
			for res in resources:
				ns.assign(task, res)
				self.__expand(ns,i+1)

	def __call__(self, state, taskSelection):
		self.taskSelection = list(taskSelection)
		self.taskSelection.append(None) # ok, this is just stupid, but allows much nicer syntax in __expand
		self.bestState = None
		# do all the work. just like that
		self.__expand(state)

class branchAndBound:

	def __call__(self, p, evaluator):
		state = ProjectSchedule([None for _ in range(len(p.tasks))])
		permutator = Permutator(evaluator)
		while not state.done():
			# get all possible tasks
			tasks = state.getAllDoableTasks()
			# do stuff
			permutator(state, tasks)
			# get best schedule
			bestSch = permutator.bestState
			# move on
			state = bestSch

		assert state._isOK() and state.done()
		et = Evaluate_Time()
		ec = Evaluate_Cost()
		print( "Project: time-{}, cost-{}".format( et(state), ec(state) ))

if __name__ == '__main__':
	pass
