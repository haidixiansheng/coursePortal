from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
import json
from web.forms.submission import SubmissionForm
from web.models import AtomCategory, Submission, Class, BaseCategory

class PlainErrorList(ErrorList):
    """
    Look at this amazing class documentation
    
    """
    def __unicode__(self):
        """This function returns the unicode name of the class"""
        return self.as_plain()
    def as_plain(self):
        """This function returns the error message
        
        **Not sure**
        
        """
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

@login_required()
def index(request, sid):
    """
    This function does a lot of really cool things
    
    """
    #Get the "top level" categories
    top_level_categories = BaseCategory.objects.filter(parent_categories=None)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, error_class=PlainErrorList)
        if sid:
            if form.is_valid():
                sub = Submission.objects.get(pk=sid)
                sub.title = form.cleaned_data['title']
                sub.content = form.cleaned_data['content']
                sub.video = json.dumps(form.cleaned_data['video'].split(' '))
                sub.tags = form.cleaned_data['tags']
                sub.save()
                messages.success(request, 'Successfully saved.')
                return HttpResponseRedirect(reverse('submit', args=[sid]))
            messages.warning(request, 'Error saving. Fields might be invalid.')
        else:
            if form.is_valid():
                s = Submission(owner=request.user)
                s.title = form.cleaned_data['title']
                s.content = form.cleaned_data['content']
                s.video = json.dumps(form.cleaned_data['video'].split(' '))
                s.save()
                s.tags = form.cleaned_data['tags']
                s.save()
                return HttpResponseRedirect(reverse('post', args=[s.id]))
            messages.warning(request, 'Error submitting.')
    else:
        if sid:
            sub = Submission.objects.get(pk=sid)
            if sub.video: video = ' '.join(json.loads(sub.video))
            else: video = ''
            i_data = {
                'title': sub.title,
                'content': sub.content,
                'video': video,
                'tags': sub.tags.all(),
            }
            form = SubmissionForm(initial=i_data, error_class=PlainErrorList)
        else:
            form = SubmissionForm(error_class=PlainErrorList)

    if sid: form_action = reverse('submit', args=[sid])
    else: form_action = reverse('submit')
    

    t = loader.get_template('submit.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'form': form,
        #'child_categories': child_categories,
        #'parent_categories': L,
    })
    return HttpResponse(t.render(c))
