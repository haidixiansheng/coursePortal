from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
import numpy as np
from string import Template
from math import *

def viewStudent(request):
	user = request.user
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
	context = {
   	'class_list': user.author.all() | user.allowed_classes.all(),
   	'user': user,
   	'breadcrumbs':breadcrumbs
   }
	return render(request, 'assignment/students.html', context)

def previewAssignment(request):
	assignment = json.loads(request.POST['previewdata'])
	question_list=[]
	try:
		for q in assignment['questions']:
			question={
				'title':'',
				'solution':'',
				'text':'',
				'choices':[]
	   	}
			question['title'] = q['title']
			q['solution']= q['solution'].replace('<br>', '\n')
			q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
			for integer_index in range(len(q['choices'])):
				q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
				q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
			exec q['code']
			question['solution']=eval(q['solution'])

			#q text formatted here
			local_dict = dict(locals())
			question['text'] = Template(q['text']).substitute(local_dict)

			for choice in q['choices']:
				answer = eval(choice)
				question['choices'].append(answer)
			if len(q['choices']) > 0:
				question['choices'].append(question['solution'])
			question_list.append(question)

	except Exception as ex:
		test=''
		test += str(ex)
		return HttpResponse(test)

	context = {
		'question_list': question_list,
   	'assignment': assignment
	}
	return render(request, 'assignment/preview.html', context)


class ClassStats():
	className=''
	classid=''
	data=[]
	average=0.0
	deviation=0.0
	minimum=0.0
	maximum=0.0
	plot=None

def metrics(request):
	user=request.user
	stat_set=[]
	maxPossible=0
	achieved=0
	for c in user.allowed_classes.all() | user.author.all():
		stats=ClassStats();
		stats.className=c.name
		stats.classid=c.id
		#Generate data
		data=[]
		maxPossible = 0.0
		achieved = 0.0
		for s in c.students.all():
			for i in s.assignmentInstances.all():
				maxPossible+=i.max_score
				achieved+=i.score
			if maxPossible>0:
				data.append((achieved/maxPossible)*100)
		stats.data=data
		#Calculate average
		stats.average = np.average(stats.data)#can add weighting
		#Calculate std deviation
		stats.deviation = np.std(stats.data)
		#Number completed?
		#Min, Max
		stats.minimum=np.nanmin(stats.data)
		stats.maximum=np.nanmax(stats.data)
		#median
		stats.median=np.median(stats.data)
		stat_set.append(stats)

	context = {
		"user":request.user,
		"stat_set":stat_set,
	}
	return render(request, 'assignment/metrics.html', context)



	