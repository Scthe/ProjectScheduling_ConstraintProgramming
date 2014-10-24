from Entity import Project, Person, Task, ProjectSchedule
from Evaluate import Evaluate_Time, Evaluate_Cost, timeit
from Project_IO import readProjectDefinition, writeScheduleToFile

@timeit
def greedySchedule(p, bestAssignEvaluator):
	"""
	:type p: Project
	"""
	unscheduledTasks = list(p.tasks)
	state = ProjectSchedule([None for _ in range(len(p.tasks))], p)
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
	print("Project: time:{:4d}h <{:6.2f} days>, cost: {:5.2f}".format(et(state), et(state) / 8, ec(state)))
	return state

if __name__ == '__main__':
	f1 = "json/D01_10_3_5_3.json"  # 512 | 90
	f2 = "json/D02_20_6_10_6.json"  # 57,330,892,800
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
		"json/d0/15_9_12_9.json"
	]

	# e = Evaluate_Time()
	e = Evaluate_Cost()

	for f in ff:
		p = readProjectDefinition(f)
		s = greedySchedule(p, e)
		# for i, task in enumerate(p.tasks):
		# 	t = min( [p.cost for p in p.getPersonsForTask(task)])
		# 	t2 = s.data[i].person.cost
			#print("#{}:: my:{:5f}; min {:5f} (selected from {} res.) --> {}".format(i, t2, t,len(p.getPersonsForTask(task)), ("Match !" if t2 - t == 0 else "~~")))
		newName = "results/greedy_"+f[f.rfind('/')+1:]
		writeScheduleToFile(s, newName)

	print("--- end ---")