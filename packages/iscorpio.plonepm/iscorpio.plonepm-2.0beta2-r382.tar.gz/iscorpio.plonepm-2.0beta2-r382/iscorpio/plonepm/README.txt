iscropio.plonepm
================

Plone Project Management is a light weight project management software
closely follow the eXtreame Programming's concept.  It helps project
manager to break down a complex project to a set of stories and create
a set of tasks for each story.  Then project manager can assign each
task to team members.

Plone Project Managementprovides progress bars for each task, each
story and the whole project.  So project managers can have a clear and
direct view of how is this project going.

Meanwhile, Plone Project Management also provides a set of document
types (memos, issues, and proposals) to keep tracking the whole
project's progress.

Leverage on Plone Workflow

leverage on plone workflow to let everybody can add memo, issue,
and/or proposal to each task, story, and project.

we need "Add plone content" + plone_workflow setting, and revise the 
folder_workflow to disable list content of folder.

Leverage on Smart Folder

leverage on smart folder to provide a full list of memos, issues, and
proposals for the whole project.

Leverage on portal_catalog

For this version, you have to manually create index and metadata for 
field getXpoint_tracking_status

Thinking about programmly add the following metadata to portal_catalog.
  getXpoint_tracking_status
  getTask_estimated_hours
  getTask_used_hours
  getTask_owners
  getTask_progress_percent
  getTask_completion_date
we may not need the add those fields into index, except
getXpoint_tracking_status.

????? looks like we have to add all of them into the index.

