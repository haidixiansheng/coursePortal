from django.conf.urls import *

urlpatterns = patterns('',
    url(r'templateA/?$', 'assignment.views.template.indexA', name="atemplate_index"),
    url(r'template/?$', 'assignment.views.template.indexQ', name="qtemplate_index"),
    url(r'template/add/?$', 'assignment.views.template.addT', name="add_template"),
    url(r'template/create/?$', 'assignment.views.template.create', name="create_template"),
    url(r'template/createA/?$', 'assignment.views.template.create_assignment', name="create_assignment_template"),
    url(r'template/view/(?P<id>\d+)/?$', 'assignment.views.template.detailQ', name='view_template'),
    url(r'template/viewA/(?P<id>\d+)/?$', 'assignment.views.template.detailA', name='view_assignment_template'),
    url(r'template/generate/?$', 'assignment.views.template.genQ', name='genQ'),
    url(r'template/generateA/?$', 'assignment.views.template.genA', name='genA'),

    url(r'utility/checktitle/?$', 'assignment.views.utility.checkAssignmentTitle', name='check_title'),

    url(r'add_question/?$', 'assignment.views.question.addQ', name='add_question'),
    url(r'(?P<pk>\d+)/question/(?P<id>\d+)/?$', 'assignment.views.question.instanceDetail', name='question_instance'),
    url(r'question/(?P<id>\d+)/?$', 'assignment.views.question.detail', name='question_detail'),
    url(r'question/create/?$', 'assignment.views.question.create', name='question'),
    url(r'question/preview/?$', 'assignment.views.question.preview', name='preview'),
    
    url(r'assign/preview/(?P<a>\d+)/?$', 'assignment.views.staff.previewTemplate', name='preview_assignment2'),
    url(r'assign/preview/?$', 'assignment.views.staff.previewAssignment', name='preview_assignment'),
    url(r'assign/qpreview/?$', 'assignment.views.staff.previewQuestion', name='preview_question'),
    url(r'students/?$', 'assignment.views.staff.viewStudent', name='view_student'),
    url(r'evaluate/?$', 'assignment.views.staff.metrics', name='metrics'),

    url(r'eval/?$', 'assignment.views.student.eval', name='eval'),
    url(r'save/?$', 'assignment.views.student.save', name='save'),
    url(r'grades/?$', 'assignment.views.student.grades', name='grades'),
    url(r'list/?$', 'assignment.views.student.list', name='list'),
    
    url(r'unmade/?$', 'assignment.views.assign.unmake', name='unmake'),
    url(r'unassign/?$', 'assignment.views.assign.unassign', name='unassign'),
    url(r'assign/index/?$', 'assignment.views.assign.index', name='assignment_index'),
    url(r'assign/create/?$', 'assignment.views.assign.create', name='create_assignment'),    
    url(r'assign/add/?$', 'assignment.views.assign.addA', name='add_assignment'),
    url(r'assign/edit/(?P<id>\d+)/?$', 'assignment.views.assign.editA', name='edit_assignment'),
    url(r'assign/instantiate/?$', 'assignment.views.assign.instantiate', name='instantiate'),
    url(r'assign/?$', 'assignment.views.assign.assign', name='assign'),
    url(r'(?P<id>\d+)/?$', 'assignment.views.assign.detail', name='assignment_detail'),
    url(r'', 'assignment.views.assign.main', name='assignment'),
)