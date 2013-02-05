from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from libreqda.forms import ProjectForm
from libreqda.models import Project


@login_required
def home(request):
    return redirect('browse_projects')


@login_required
def browse_projects(request, template='browse_projects.html'):
    user = request.user
    projects = user.projects.all()

    return render(request, template, {'projects': projects})


@login_required
def new_project(request, template='new_project.html'):
    if request.method == 'POST':
        p = Project()
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            p.owner = request.user
            p.save()

            return redirect('browse_projects')
    else:
        form = ProjectForm()

    form_action = reverse('new_project')
    return render(request,
                  template,
                  {'project_form': form,
                   'form_action': form_action,
                   'back_url': reverse('browse_projects')})
