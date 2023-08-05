import os
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify

from pygments import formatters, highlight, lexers
from pygments.lexers import guess_lexer, get_lexer_by_name

from github.libs.github import GithubAPI

GITHUB_LOGIN = getattr(settings, 'GITHUB_LOGIN', '')
GITHUB_TOKEN = getattr(settings, 'GITHUB_TOKEN', '')
GITHUB_FETCH_BLOBS = getattr(settings, 'GITHUB_FETCH_BLOBS', True)
github_client = GithubAPI(GITHUB_LOGIN, GITHUB_TOKEN)

class GithubUser(models.Model):
    login = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    blog = models.URLField(verify_exists=False, blank=True)
    following_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    public_gist_count = models.PositiveSmallIntegerField(default=0)
    public_repo_count = models.PositiveSmallIntegerField(default=0)
    
    followers = models.ManyToManyField('self', related_name='followers_set', blank=True)
    following = models.ManyToManyField('self', related_name='following_set', blank=True)

    class Meta:
        ordering = ('login',)
        db_table = 'github_user'

    def __unicode__(self):
        return self.login

    def get_absolute_url(self):
        return 'http://github.com/%s' % (self.login)

    def save(self, *args, **kwargs):
        if not self.id:
            self.fetch_github()
        super(GithubUser, self).save(*args, **kwargs)
   
    def fetch_github(self):
        user = github_client.get_user(self.login)
        if user:
            self.name = user.name or ''
            self.company = user.company or ''
            self.location = user.location or ''
            self.email = user.email or ''
            self.blog = user.blog or ''
            self.following_count = user.following_count
            self.followers_count = user.followers_count
            self.public_gist_count = user.public_gist_count
            self.public_repo_count = user.public_repo_count
        return user

    def fetch_repos(self):
        repos = github_client.get_repos(self.login)
        if repos:
            for repo in repos:
                project, created = Project.objects.get_or_create(
                        user=self, github_repo=repo.name)
                project.title = repo.name
                project.description = repo.description
                project.save()
        return repos
    
    def fetch_watching(self):
        repos = github_client.watching(self.login)
        if repos:
            for repo in repos:
                try:
                    owner = GithubUser.objects.get(login__iexact=repo.owner)
                except GithubUser.DoesNotExist:
                    owner = GithubUser.objects.create(login=repo.owner)
                project, created = Project.objects.get_or_create(
                    user=owner, github_repo=repo.name)
                if created:
                    project.title = repo.name
                    project.description = repo.description
                    project.save()
                project.watchers.add(self)
        return repos
    
    def fetch_followers(self):
        followers = github_client.followers(self.login)
        if followers:
            for follower in followers:
                try:
                    follower = GithubUser.objects.get(login__iexact=follower)
                except GithubUser.DoesNotExist:
                    follower = GithubUser.objects.create(login=follower)
                self.followers.add(follower)
        return followers
    
    def fetch_following(self):
        following = github_client.following(self.login)
        if following:
            for follower in following:
                try:
                    follower = GithubUser.objects.get(login__iexact=follower)
                except GithubUser.DoesNotExist:
                    follower = GithubUser.objects.create(login=follower)
                self.following.add(follower)
        return following
    
    def contributed_to(self):
        return Project.objects.filter(commits__author=self).exclude(user=self).distinct()


class Project(models.Model):
    user = models.ForeignKey(GithubUser, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    github_repo = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    watchers = models.ManyToManyField(GithubUser, related_name='watched', blank=True)
    
    class Meta:
        ordering = ('title',)
        unique_together = ('user', 'slug')
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)
   
    def _repo_required(func):
        def inner(self, *args, **kwargs):
            if self.github_repo and self.user:
                return func(self, *args, **kwargs)
            else:
                raise AttributeError('Missing repo or user on project')
        return inner

    def get_absolute_url(self):
        return reverse('github_project_detail', args=[self.slug])
    
    def get_latest_commit(self):
        try:
            return self.commits.all()[0]
        except IndexError:
            return None
    
    @property
    @_repo_required
    def github_url(self):
        return 'http://github.com/%s/%s' % (self.user.login, self.github_repo)
    
    @property
    @_repo_required
    def github_clone_command(self):
        if not self.user or not self.github_repo:
            return ''
        return 'git clone git://github.com/%s/%s.git' % (self.user.login, self.github_repo)
    
    @_repo_required
    def fetch_github(self):
        commits_processed = []
        
        commit_list = github_client.get_commits(self.user.login, self.github_repo)
        if not commit_list:
            return commits_processed
        
        # store all the commits - an API call can be saved here, as all the
        # necessary commit data is returned by the get_commits() call.
        for commit in commit_list:
            author_login = commit.author['login'] or commit.committer['login']
            if not author_login:
                author_login = self.user.login
            try:
                author = GithubUser.objects.get(login__iexact=author_login)
            except GithubUser.DoesNotExist:
                author = GithubUser.objects.create(login=author_login)
            instance, created = Commit.objects.get_or_create(project=self, sha=commit.id, author=author)
            if created:
                instance.created = commit.committed_date
                instance.message = commit.message
                instance.name = commit.committer.get('name', '')
                instance.tree = commit.tree
                instance.url = commit.url
                instance.project = self
                instance.save()
                commits_processed.append(instance)
        
        # download the *latest* tree if new commits exist
        if len(commits_processed) and GITHUB_FETCH_BLOBS:
            commit = commits_processed[0]
            commit.fetch_blobs()
        
        return commits_processed
    
    @_repo_required
    def contributors(self):
        authors = self.commits.values('author')
        annotated = authors.annotate(count=Count('author')).order_by('-count')
        return map(lambda bit: GithubUser.objects.get(pk=bit['author']), annotated)
    

class Commit(models.Model):
    project = models.ForeignKey(Project, related_name='commits')
    sha = models.CharField(max_length=255)
    tree = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)
    url = models.URLField()
    author = models.ForeignKey(GithubUser, related_name='commits', null=True)
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return '%s: %s' % (self.project.title, self.message)
    
    def get_absolute_url(self):
        return self.url
    
    def fetch_github(self):
        if not self.project or not self.project.github_repo:
            raise AttributeError('Required attribute missing: "github_repo" on %s' % self.project)

        commit = github_client.get_commit(self.project.user.login, 
                                          self.project.github_repo, 
                                          self.sha)
        if commit:
            self.tree = commit.tree
            self.created = commit.committed_date
            self.name = commit.committer.get('name', '')
            self.message = commit.message
            self.url = commit.url
            self.save()
        return commit
    
    def fetch_blobs(self):
        def process_tree(tree, path=''):
            objs = github_client.get_tree(self.project.user.login, 
                                          self.project.github_repo, 
                                          tree)
            for obj in objs:
                if obj.type == 'tree':
                    process_tree(obj.sha, path + obj.name + '/')
                blob, created = Blob.objects.get_or_create(commit=self, 
                        name=obj.name, path='%s%s' % (path, obj.name))
                if created:
                    fetched = blob.fetch_github(tree, path)
            return
        process_tree(self.tree)


class Blob(models.Model):
    commit = models.ForeignKey(Commit, related_name='blobs')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255, editable=False)
    size = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=255)
    data = models.TextField()
    sha = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['-commit__created', 'commit__project__title', 'path']
    
    def __unicode__(self):
        return '%s (%s)' % (self.path, self.size)
    
    def get_absolute_url(self):
        return reverse('github_blob_detail', args=[self.commit.project.slug, self.path])
    
    @property
    def download_url(self):
        return reverse('github_blob_download', args=[self.commit.project.slug, self.path])
    
    def fetch_github(self, tree, path=''):
        if not self.commit or not self.name:
            raise AttributeError('Required attribute missing on Blob object')
        blob = github_client.get_blob(self.commit.project.user.login, 
                self.commit.project.github_repo, tree, self.name)
        if blob:
            self.path = path + blob.name
            self.size = blob.size
            self.mime_type = blob.mime_type
            self.data = blob.data
            self.sha = blob.sha
            self.save()
        return blob

    def highlight(self):
        try:
            # Guess a lexer by the contents of the block.
            lexer = guess_lexer(self.data)
        except ValueError, e:
            # Just make it plain text.
            lexer = get_lexer_by_name('text', stripall=True, encoding='UTF-8')
        formatter = formatters.HtmlFormatter()
        return highlight(self.data, lexer, formatter)

    @property
    def depth(self):
        return len(self.path.split('/'))


class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    language_code = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('github_language_detail', args=[self.slug])
        
    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)


class Gist(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    language = models.ForeignKey(Language)
    filename = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True)
    code = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    gist_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = self.code.replace('\t', '    ')
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.gist_id:
            self.gist_id = self.create_gist()
        super(Gist, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        if self.gist_url:
            return self.gist_url
        return reverse('github_gist_detail', args=[self.slug])
    
    def create_gist(self):
        filename = self.filename or self.title
        gist_id = github_client.create_gist(
            filename, 
            self.code, 
            self.language.extension)            
        return gist_id
    
    @property
    def gist_url(self):
        if not self.gist_id:
            return False
        return 'http://gist.github.com/%s' % (self.gist_id)
    
    def highlight(self):
        return highlight(self.code,
                         self.language.get_lexer(),
                         formatters.HtmlFormatter())
