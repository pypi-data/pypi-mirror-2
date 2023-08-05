## Script (Python) "getStoryTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=story
##title=getStoryTasks
##

"""
preparing the tasks information for a story: task title, task
owner(s), subtotal of estmimated hours, average of progress status,
etc.
"""
# trying to search the tasks from the portal_catalog...
tasks = context.portal_catalog.searchResults(
    portal_type = ('XPointTask', ),
    # ?????? 1. where does the story come from, it is defined in the
    # parameters list, but I still could NOT understand where is it
    # from?
    # ?????? 2. why we need a forward slash '/' here?  Will it bring
    # us to the root of this portal?
    path = {'query': '/'.join(story.getPhysicalPath()),},
    sort_on = 'Date',
    sort_order = 'reverse',
    )

# we will return this to invoker.
tasksInfo = {}
# all task list.
tasksList = []
# subtotal of estimated hours.
estimatedSubtotal = 0
# average progress percent.
averageProgress = 0

tasksInfo['thePath'] = '/'.join(story.getPhysicalPath())
tasksInfo['tasksAmount'] = len(tasks)

if len(tasks) > 0:

    # the subtotal of the progress percent.
    progressSubtotal = 0
    # for each task,
    for task in tasks:
        # add to the task list.
        tasksList.append(task)
        # calc the subtotal of the estimated hours.
        if task.getTask_estimated_hours != None:
            estimatedSubtotal = estimatedSubtotal + task.getTask_estimated_hours

        # calc the subtotal of the progress percentage.
        if task.getTask_progress_percent != None:
            progressSubtotal = progressSubtotal + task.getTask_progress_percent

    # calc the average progress.
    averageProgress = progressSubtotal / len(tasks)

else:

    # no task found, reset everything.
    tasksList = []
    estimatedSubtotal = 0
    averageProgress = 0

# preparing the return object.
tasksInfo['tasksList'] = tasksList
tasksInfo['estimatedSubtotal'] = estimatedSubtotal
tasksInfo['averageProgress'] = averageProgress

return tasksInfo
