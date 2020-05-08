from app import taskService


def test_getTaskList():
    tasks = taskService.getMyTaskList("a8439e6632b14b11b62a88a849546658")
    print(tasks)
    print(len(tasks))
    for task in tasks:
        print(task)

def test_getPublicTasks():
    tasks=taskService.getPublicTaskList()
    print(tasks)
    print(len(tasks))
    for task in tasks:
        print(task)

def test_getSupportTasks():
    tasks = taskService.getMySupportTaskList('a8439e6632b14b11b62a88a849546658')
    print(tasks)
    print(len(tasks))
    for task in tasks:
        print(task)