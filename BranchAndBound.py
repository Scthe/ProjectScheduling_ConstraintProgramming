import locale
from Entity import Project,Person,Task, ProjectSchedule
from Evaluate import Evaluate_Time, Evaluate_Cost, timeit
from Project_IO import readProjectDefinition, writeScheduleToFile

class Permutator():

	eval = []
	bestState, bestScore = None, -1 # TODO assumed only one state can be the best, use list instead !

	def __init__(self, bestAssignEvaluator):
		self.eval = bestAssignEvaluator

	def __expand(self, state, i=0):
		# get task to ponder about
		task = self.taskSelection[i]
		if not task: # TODO use yield ?
			#print("{:,d} /{:,d} -> {:.2f}".format(self.permutation_i, self.permutationCount, (self.permutation_i/ self.permutationCount*100)))
			self.permutation_i += 1

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
		from functools import reduce
		self.permutationCount = reduce(lambda x, y: x*y, [len(state.project.getPersonsForTask(t)) for t in taskSelection])
		self.permutation_i = 0

		self.taskSelection = list(taskSelection)
		self.taskSelection.append(None) # ok, this is just stupid, but allows much nicer syntax in __expand
		self.bestState = None
		# do all the work. just like that
		self.__expand(state)

@timeit
def branchAndBound(p, evaluator):
	"""
	:type p: Project
	"""
	state = ProjectSchedule([None for _ in range(len(p.tasks))], p)
	permutator = Permutator(evaluator)
	while not state.done():
		#print("done {} /{}".format(sum([1 for a in state.data if a]), len(state.data)))
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
	print( "Project: time:{:4d}h < {:6.2f} days>, cost: {:5.2f}".format( et(state),et(state)/8, ec(state) ))
	return state

if __name__ == '__main__':
	f1 = "json/D01_10_3_5_3.json" # 512
	f2 = "json/D02_20_6_10_6.json" # 57,330,892,800
	f3 = "json/json_ex.json"
	f4 = "json/D03_50_10_25_10.json"
	f5 = "json/100_5_20_9_D3.json"
	f6 = "json/a.json"
	ff = [
		"json/d0/10_3_5_3.json",
		"json/d0/10_5_8_5.json",
		"json/d0/10_7_10_7.json",
		"json/d0/15_3_5_3.json",
		"json/d0/15_6_10_6.json",
		#"json/d0/15_9_12_9.json"
	]

	e = Evaluate_Time()
	# e = Evaluate_Cost()
	for f in ff:
		p = readProjectDefinition(f)
		s = branchAndBound(p,e)
		newName = "results/bb_"+f[f.rfind('/')+1:]
		writeScheduleToFile(s, newName)

	print("--- end ---")