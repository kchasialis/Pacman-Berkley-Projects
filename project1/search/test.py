startPos = problem.getStartState()
frontier = util.Queue()
frontier.push(startPos)
explored = []

while not frontier.isEmpty():
	currentPos = frontier.pop()
	explored.append(currentPos)
	successorsOfCurrent = problem.getSuccessors(currentPos)
    if problem.isGoalState(currentPos):
        return actions

	for successor in successorsOfCurrent:
		if successor[0] not in explored:
			frontier.push(successor[0])
return []

