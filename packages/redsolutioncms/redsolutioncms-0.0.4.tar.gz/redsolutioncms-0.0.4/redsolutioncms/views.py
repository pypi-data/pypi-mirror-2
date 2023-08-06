from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from redsolutioncms.forms import UserCreationForm, FrontpageForm, CategoryForm
from redsolutioncms.importpath import importpath
from redsolutioncms.loader import home_dir, process_cmd_string, project_dir
from redsolutioncms.make import AlreadyMadeException
from redsolutioncms.models import CMSSettings, ProcessTask, Category
from redsolutioncms.packages import load_package_list
import os, subprocess, datetime

CONFIG_FILES = ['manage', 'settings', 'urls', ]


def index(request):
    """
    Shows greetings form, base settings form: project name, database settings, etc.
    """
    cms_settings = CMSSettings.objects.get_settings()
    cms_settings.initialized = True
    cms_settings.save()
    SettingsForm = modelform_factory(CMSSettings, exclude=['initialized',
        'frontpage_handler', 'base_template'])
    if request.method == 'POST':
        form = SettingsForm(data=request.POST, files=request.FILES, instance=cms_settings)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('apps'))
    else:
        form = SettingsForm(instance=cms_settings)
    return render_to_response('redsolutioncms/index.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def apps(request):
    """
    Second step. Shows available packages listing.
    """
    FormsetClass = modelformset_factory(Category, CategoryForm)

    if request.method == 'POST':
        formset = FormsetClass(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('load'))
    else:
        from urllib2 import HTTPError, URLError
        try:
            load_package_list()
        except (HTTPError, URLError):
            return render_to_response('redsolutioncms/error.html', {
                'error': _('Htttp problem with index server'),
            })
        formset = FormsetClass()
    return render_to_response('redsolutioncms/apps.html', {
        'formset': formset,
    }, context_instance=RequestContext(request))


def load(request):
    """
    Show wait circle loader, fetch packages from index site.
    Template has AJAX checker, so user will be redirected to next step automatically.
    Saves installation information for packages.
    Makes settings.py, urls.py, manage.py with installed setup-packages.
    Syncdb for setup-packages.
    """
    task = ProcessTask.objects.create(
        task=process_cmd_string('"%(django)s" kill_runserver'),
        lock=True, wait=True)
    ProcessTask.objects.create(task=process_cmd_string('"%(django)s" install_packages'), wait=True)
    ProcessTask.objects.create(task=process_cmd_string('"%(django)s" change_settings'), wait=True)
    ProcessTask.objects.create(task=process_cmd_string('"%(django)s" syncdb --noinput'), wait=True)
    ProcessTask.objects.create(task=process_cmd_string('"%(django)s" runserver --noreload'))
    return render_to_response('redsolutioncms/wait.html', {
        'task_id':task.id,
        'redirect_to': reverse('custom'),
        'start_task_id':task.id,
        'title': _('Downloading packages'),
    }, context_instance=RequestContext(request))

def custom(request):
    """
    User can go to detail settings for packages or can ask to make project.
    Make files for new project.
    """
    cms_settings = CMSSettings.objects.get_settings()
    if request.method == 'POST':
        entry_points = ['redsolutioncms']
        cms_settings.base_template = 'base_template.html'
        cms_settings.save()
        # handle frontpage
        frontpage_form = FrontpageForm(request.POST)
        if frontpage_form.is_valid():
            frontpage_form.save()
            for package in cms_settings.packages.installed():
                for entry_point in package.entry_points.all():
                    entry_points.append(entry_point.module)
            make_objects = []
            for entry_point in entry_points:
                try:
                    make_object = importpath('.'.join([entry_point, 'make', 'make']))
                except ImportError, error:
                    print 'Entry point %s has no make object.' % entry_point
                    continue
                else:
                    make_objects.append(make_object)

            for make_object in make_objects:
                make_object.flush()
            for make_object in make_objects:
                try:
                    make_object.premake()
                except AlreadyMadeException:
                    pass
            for make_object in make_objects:
                try:
                    make_object.make()
                except AlreadyMadeException:
                    pass
            for make_object in make_objects:
                try:
                    make_object.postmake()
                except AlreadyMadeException:
                    pass
            return HttpResponseRedirect(reverse('build'))
    else:
        frontpage_form = FrontpageForm()
    return render_to_response('redsolutioncms/custom.html', {
        'cms_settings': cms_settings,
        'frontpage_form': frontpage_form,
    }, context_instance=RequestContext(request))

def build(request):
    cms_settings = CMSSettings.objects.get_settings()
    task = ProcessTask.objects.create(
        task=process_cmd_string('"%(django)s" kill_runserver'),
        lock=True, wait=True)

    project_params = {
        'project_bootstrap': os.path.join(project_dir, 'bootstrap.py'),
        'project_buildout_cfg': os.path.join(project_dir, 'develop.cfg'),
        'project_buildout': os.path.join(project_dir, 'bin', 'buildout'),
        'project_django': os.path.join(project_dir, 'bin', 'django'),
    }


    ProcessTask.objects.create(
        task=process_cmd_string('"%(python)s" "%(project_bootstrap)s" -c "%(project_buildout_cfg)s"', project_params),
        wait=True)
    ProcessTask.objects.create(
        task=process_cmd_string('"%(project_buildout)s" -c "%(project_buildout_cfg)s"', project_params),
        wait=True)
    ProcessTask.objects.create(
        task=process_cmd_string('"%(project_django)s" syncdb --noinput', project_params),
        wait=True)
    ProcessTask.objects.create(
        task=process_cmd_string('"%(project_django)s" runserver 8001 --noreload',
        project_params))
    ProcessTask.objects.create(
        task=process_cmd_string('"%(django)s" runserver --noreload'))

    return render_to_response('redsolutioncms/wait.html', {
        'task_id': task.id,
        'redirect_to': reverse('create_superuser'),
        'start_task_id':task.id,
        'title': _('Building your site'),
    }, context_instance=RequestContext(request))

def create_superuser(request):
    cms_settings = CMSSettings.objects.get_settings()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = User.objects.model(username='generate_password')
            user.set_password(password)
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            context = {
                'username': form.cleaned_data['username'],
                'password': user.password,
                'email': form.cleaned_data['email'],
                'current_datetime': current_datetime,
                }
            data = render_to_string(
                'redsolutioncms/project/fixtures/create_superuser.json', context)
            open(os.path.join(project_dir,
                'create_superuser.json'), 'w').write(data)
            django_name = os.path.join(project_dir, 'bin', 'django')
            subprocess.Popen([django_name, 'loaddata',
                os.path.join(project_dir, 'create_superuser.json')]).wait()
            os.remove(os.path.join(project_dir, 'create_superuser.json'))
            return HttpResponseRedirect(reverse('done'))
    else:
        form = UserCreationForm()
    return render_to_response('redsolutioncms/build.html', {
        'cms_settings': cms_settings,
        'bootstrap': os.path.join(project_dir, 'bootstrap.py'),
        'buildout': os.path.join(project_dir, 'bin', 'buildout'),
        'django': os.path.join(project_dir, 'bin', 'django'),
        'form': form,
    }, context_instance=RequestContext(request))

def done(request):
    cms_settings = CMSSettings.objects.get_settings()
    return render_to_response('redsolutioncms/done.html', {
        'cms_settings': cms_settings,
        'project_dir': project_dir,
        'django': os.path.join(project_dir, 'bin', 'django'),
    }, context_instance=RequestContext(request))

def restart(request):
    """
    Ajax view. Restarts runserver
    """
    task = ProcessTask.objects.create(task=process_cmd_string('"%(django)s" kill_runserver'),
        lock=True, wait=True)
    ProcessTask.objects.create(task=process_cmd_string('"%(django)s" runserver --noreload'))
    task.lock = False
    task.save()
    return HttpResponse()

def started(request):
    """
    User can`t see it. It will be called by javascript.
    Used to check, whether server is available after restart.
    """
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task = get_object_or_404(ProcessTask, id=task_id)
        if task.process_finished:
            return HttpResponse()
    return HttpResponseNotFound()

def cancel_lock(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task = get_object_or_404(ProcessTask, id=task_id)
        task.lock = False
        task.save()
    return HttpResponse()
