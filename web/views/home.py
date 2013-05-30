from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.db.models.loading import get_models
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404
import json

for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)


def class_index(request):

    #Get the "top level" categories
    top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)
    
    template = loader.get_template('home/index.html')
    class_list = Class.objects.order_by('name')
    context = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('class_index'), 'title': 'Class Index'}],
        'class_list': class_list,
        'top_level_base_categories': top_level_base_categories,
    })
    return HttpResponse(template.render(context))

def index(request):

    #Get the "top level" categories
    top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)

    # get the highest ranked submissions
    top_ranked_videos = cache.get('top_ranked_videos')
    if not top_ranked_videos:
        top_ranked_videos = []
        for category in VoteCategory.objects.all():
            # for now, calculate an average for each video
            top_ranked_videos.append({
                'vote_category': category, 
                'submissions': Submission.objects.filter(votes__v_category=category).annotate(average_rating=Avg('votes__rating')).order_by('-average_rating')[:5],
            })
        cache.set('top_ranked_videos', top_ranked_videos, 60*10)
    
    template = loader.get_template('home/classes.html')
    context = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'top_level_base_categories': top_level_base_categories,
        'top_ranked_videos': top_ranked_videos,
        'is_post': False,
    })
    return HttpResponse(template.render(context))


def get_content_for_category(current_category, content_list, is_exposition):
    for atom in current_category.child_atoms.all():
        if is_exposition:
            content = atom.exposition_set.all()
        else:
            content = Submission.objects.filter(tags = atom).distinct()
        for c in content:
            if content_list.count(c) == 0:
                content_list.append(c)
    for child in current_category.child_categories.all():
        get_content_for_category(child, content_list, is_exposition)
    return content_list

def get_parent_categories(current_category, parent_categories, current_class=None):
    parent_categories.append(current_category)
    if current_class:
        tmp_categories = current_category.parent_categories.filter(parent_class=current_class.id)
    else:
        tmp_categories = current_category.parent_categories.all()
    while tmp_categories:
        parent_categories.append(tmp_categories[0])
        print(tmp_categories[0])
        if current_class:
            tmp_categories = tmp_categories[0].parent_categories.filter(parent_class = current_class.id)
        else:
            tmp_categories = tmp_categories[0].parent_categories.all()
    return parent_categories

def base_category(request, cat_id):
    """
    - Generates the category page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    #get category we are in
    current_category = get_object_or_404(BaseCategory, id=cat_id)
    #Get the "top level" categories
    top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)
    
    #Get list of parent categories, not perfect, improvements can be made
##    parent_categories = list()
##    parent_categories.append(current_category)
##    tmp_categories = current_category.parent_categories.all()
##    while tmp_categories:
##        parent_categories.append(tmp_categories[0])
##        print(tmp_categories[0])
##        tmp_categories = tmp_categories[0].parent_categories.all()
    parent_categories = get_parent_categories(current_category, list())

    #Setting breadcrumbs, not perfect, improvements can be made
    breadcrumbs = []
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('base_category', args=[parent_categories[-i].id]), 'title': parent_categories[-i]})

    #Get collection of videos from all atoms in this category or sub-categories
    content = get_content_for_category(current_category, list(), False)

    # un-json-fy the videos
    for c in content:
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)

    expositions = get_content_for_category(current_category, list(), True)

    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        #'lectureNotes': lectureNotes,
        'top_level_base_categories': top_level_base_categories,
        'selected_categories': parent_categories,
        'selected_category': current_category,
        'vote_categories': VoteCategory.objects.all(),
        'is_post' : False,
    })
    return HttpResponse(t.render(c))

def base_atom(request, cat_id, atom_id):
    """
    - Generates the view for a specific category
    - Creates the breadcrumbs for the page
    """
    #Get atom we are in
    current_atom = get_object_or_404(Atom, id=atom_id)
    #get category we are in
    current_category = get_object_or_404(BaseCategory, id=cat_id)
    #Get the "top level" categories
    top_level_base_categories = BaseCategory.objects.filter(parent_categories=None) #check that this works

    parent_categories = get_parent_categories(current_category, list())

    breadcrumbs = []
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('base_category', args=[parent_categories[-i].id]), 'title': parent_categories[-i]})
    breadcrumbs.append({'url': reverse('base_atom', args=[current_category.id, current_atom.id]), 'title': current_atom})

    
    content = Submission.objects.filter(tags=current_atom).distinct()


    # un-json-fy the videos
    for c in content:
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)


    expositions = current_atom.exposition_set.all()


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'top_level_base_categories': top_level_base_categories,
        'selected_categories': parent_categories,
        'selected_category': current_category,
        'selected_atom': current_atom,
        'vote_categories': VoteCategory.objects.all(),
        'is_post': False,
    })
    return HttpResponse(t.render(c))
    

def category(request, class_id, cat_id):
    """
    - Generates the category page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    #get category we are in
    current_category = get_object_or_404(Category, id=cat_id)
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
    parent_categories = get_parent_categories(current_category, list(), current_class)

    #Setting breadcrumbs, not perfect, improvements can be made
    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('category', args=[current_class.id, parent_categories[-i].id]), 'title': parent_categories[-i]})

    #Get collection of videos from all atoms in this category or sub-categories
    content = get_content_for_category(current_category, list(), False)
    


    # un-json-fy the videos
    for c in content:
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)

    expositions = get_content_for_category(current_category, list(), True)
    lectureNotes = LectureNote.objects.filter(classBelong = current_class)

    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'lectureNotes': lectureNotes,
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'selected_category': current_category,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
        'categories_in_class':categories_in_class,
        'is_post' : False,
    })
    return HttpResponse(t.render(c))


def atom(request, class_id, cat_id, atom_id):
    """
    - Generates the view for a specific category
    - Creates the breadcrumbs for the page
    """
    #Get atom we are in
    current_atom = get_object_or_404(Atom, id=atom_id)
    #get category we are in
    current_category = get_object_or_404(Category, id=cat_id)
##    #Get the parents of the category we are in
##    parents = current_category.parent_categories.all() #Check that it is correct
    
    #Get class we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None) #check that this works

    #Get list of parent categories, not perfect, improvements can be made
    parent_categories = get_parent_categories(current_category, list(), current_class)


    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('category', args=[current_class.id, parent_categories[-i].id]), 'title': parent_categories[-i]})
    breadcrumbs.append({'url': reverse('atom', args=[current_class.id, current_category.id, current_atom.id]), 'title': current_atom})

    
    content = Submission.objects.filter( Q(tags=current_atom) ).distinct()


    # un-json-fy the videos
    for c in content:
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)


    expositions = current_atom.exposition_set.all()
    lectureNotes = LectureNote.objects.filter(classBelong = current_class)


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'lectureNotes': lectureNotes,
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'selected_category': current_category,
        'selected_atom': current_atom,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
        'is_post': False,
    })
    return HttpResponse(t.render(c))


def classes(request, class_id):
    """
    - Generates the home page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
    # get the highest ranked submissions
    top_ranked_videos = cache.get('top_ranked_videos')
    if not top_ranked_videos:
        top_ranked_videos = []
        for category in VoteCategory.objects.all():
            # for now, calculate an average for each video
            top_ranked_videos.append({
                'vote_category': category, 
                'submissions': Submission.objects.filter(votes__v_category=category).annotate(average_rating=Avg('votes__rating')).order_by('-average_rating')[:5],
            })
        cache.set('top_ranked_videos', top_ranked_videos, 60*10)


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url':reverse('classes', args=[current_class.id]), 'title': current_class.name}],
        'top_level_categories': top_level_categories,
        'top_ranked_videos': top_ranked_videos,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
        'is_post': False,
    })
    return HttpResponse(t.render(c))

def post(request, class_id, sid):
    """
    - Generates the view for the specific post (submission) from `sid`
    - Creates the appropriate breadcrumbs for the categories
    """
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
    s = Submission.objects.get(id=sid)
    
    if s.video:
        s.video = [v for v in json.loads(s.video)]

    current_atom = s.tags.all()[0]
    current_category = current_atom.category_set.filter(parent_class = current_class.id)[0]
    
    parent_categories = get_parent_categories(current_category, list(), current_class)


    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]

    breadcrumbs.append({'url' : reverse('post', args=[current_class.id, s.id]), 'title': s})

##    if len(parent_categories) >= 1:
##        parent = parent_categories[0]
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id,parent.id]), 'title': parent})
##    else: parent = None
##
##    categories = s.tags.filter( ~Q(parent=None) )
##    if len(categories) >= 1: 
##        category = categories[0]
##    else: category = None
##
##    if parent == None:
##        c = category.parent.all()
##        if len(c) > 0:
##            c = category.parent.all()[0]
##            breadcrumbs.append({'url': reverse('category', args=[current_class.id,c.id]), 'title': c})
##                
##    if category:
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id,category.id]), 'title': category})


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': [s],
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'selected_category': current_category,
        'selected_atom': current_atom,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
        'is_post': True,
    })
    return HttpResponse(t.render(c))
