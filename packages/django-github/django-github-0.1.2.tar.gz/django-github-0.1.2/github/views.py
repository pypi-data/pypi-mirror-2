import simplejson

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from github.models import Project, Blob, Gist, GithubUser

GITHUB_KEY = getattr(settings, 'GITHUB_KEY', '1337')

def project_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Project.objects.all(),
        paginate_by=paginate_by,
        page=int(request.GET.get('page', 0)),
        **kwargs
    )

def project_detail(request, project_slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Project.objects.all(),
        slug=project_slug,
        slug_field='slug',
        template_object_name='project',
    )

def commit_list(request, project_slug, paginate_by=20, template_name='github/commit_list.html', **kwargs):
    project = get_object_or_404(Project, slug=project_slug)
    return list_detail.object_list(
        request,
        queryset=project.commits.all(),
        extra_context={'project': project},
        template_name=template_name,
        paginate_by=paginate_by,
        page=int(request.GET.get('page', 0)),
        **kwargs
    )

def blob_list(request, project_slug, template_name='github/blob_list.html', **kwargs):
    project = get_object_or_404(Project, slug=project_slug)
    latest_commit = project.get_latest_commit()
    if not latest_commit:
        raise Http404
    return list_detail.object_list(
        request,
        queryset=latest_commit.blobs.all(),
        extra_context={'project': project, 'commit': latest_commit},
        template_name=template_name,
        **kwargs
    )

def blob_detail(request, project_slug, path, template_name='github/blob_detail.html', **kwargs):
    project = get_object_or_404(Project, slug=project_slug)
    latest_commit = project.get_latest_commit()
    blob = get_object_or_404(latest_commit.blobs.all(), path=path)
    if not latest_commit:
        raise Http404
    return render_to_response(template_name, 
            { 'object': blob, 'project': project, 'commit': latest_commit }, 
            context_instance=RequestContext(request))

def blob_download(request, project_slug, path):
    project = get_object_or_404(Project, slug=project_slug)
    latest_commit = project.get_latest_commit()
    blob = get_object_or_404(latest_commit.blobs.all(), path=path)
    response = HttpResponse(blob.data, blob.mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % (blob.name)
    return response

def gist_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Gist.objects.all(),
        paginate_by=paginate_by,
        page=int(request.GET.get('page', 0)),
        **kwargs
    )

def gist_detail(request, gist_slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Gist.objects.all(),
        slug=gist_slug
    )

def user_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=GithubUser.objects.all(),
        paginate_by=paginate_by,
        page=int(request.GET.get('page', 0)),
        template_name='github/user_list.html',
        **kwargs
    )

def user_detail(request, login, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=GithubUser.objects.all(),
        slug=login,
        slug_field='login',
        template_name='github/user_detail.html',
    )

@csrf_exempt
def github_hook(request, secret_key):
    if secret_key != GITHUB_KEY:
        raise Http404
    if request.method == 'POST':
        try:
            data = simplejson.loads(request.POST['payload'])
            repo = data['repository']['name']
            project = Project.objects.get(github_repo=repo)
            project.fetch_github()
            return HttpResponse('OK')
        except project.DoesNotExist:
            pass
    return HttpResponse('')
