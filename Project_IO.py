import json
from Entity import Project, Task, Person, ProjectSchedule

'''
	{
	 "id":1,
	 "duration":36,
	 "skills":{
		"name":" Q2",
		"level":1
	 },
	 "dependables":[]
	}

	{
	 "cost":0.0,
	 "skills":[
		{
		   "name":" Q0",
		   "level":1
		},
		{
		   "name":" Q1",
		   "level":0
		}
	 ]
	}
	'''

def readSkills(obj):
	skills = dict()
	for s in obj["skills"]:
		#print( s)
		if "name" in s.keys():
			skills[s["name"]] = s["level"]
		#else: print("s")
	return skills

def readProjectDefinition(filePath):
	with open(filePath, "rt") as txt:
		data = json.load(txt)
	#print( data)

	#read tasks
	tasks = []
	for tt in data["tasks"]:
		t = Task(tt["duration"], readSkills(tt), [])
		#print(tt["dependables"])
		t._dependables = tt["dependables"]
		t._id = tt["id"]
		tasks.append(t)
	# read dependables
	for t in tasks:
		t.constraints = [tt for tt in tasks if (tt._id in t._dependables and t._id != tt._id)]
	#print(str(t._dependables)+"->"+str(len(t.constraints))+" :: "+str(",".join(map(str,t.constraints))))

	#read people
	people = []
	for pp in data["people"]:
		p = Person(readSkills(pp), pp["cost"])
		p._id = pp["id"]
		people.append(p)

	return Project(tasks, people)


'''
def storeEvalData(eval):
	print("store eval data")
	print( "total collected: " + str(len(eval.best)))
	#ok = [e for e in eval.best if eval(e) <= eval.bestScore] # !!!
	#print( len(ok))
	obj = { "score":eval.bestScore, "values":[]}
	for i,assign in enumerate(eval.best[0].data):
		obj["values"].append({"taskId":i,"startTime":assign.startTime,"person:":assign.person._id})
	with open('data.txt', 'w') as outfile:
		json.dump(obj, fp=outfile, indent=4 )
'''