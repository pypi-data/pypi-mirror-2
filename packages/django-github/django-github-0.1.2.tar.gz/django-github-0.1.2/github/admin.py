from django.contrib import admin
from github.models import Project, Blob, Commit, GithubUser, Gist, Language

class GithubUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'name', 'blog')
    search_fields = ('login', 'name', 'company', 'blog')

    actions = ['fetch_github', 'fetch_repos', 'fetch_watching', 'fetch_followers', 'fetch_following']

    def fetch_github(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_github():
                user.save()
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_github.short_description = 'Fetch from Github'

    def fetch_repos(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_repos():
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_repos.short_description = 'Fetch repos from Github'
    
    def fetch_watching(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_watching():
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_watching.short_description = 'Fetch repos these users watch'
    
    def fetch_following(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_following():
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_following.short_description = 'Fetch who these users follow'
    
    def fetch_followers(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_followers():
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_followers.short_description = 'Fetch these users followers'

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'github_repo',)
    list_filter   = ('created',)
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}
    
    actions = ['fetch_github']
    
    def fetch_github(self, request, queryset):
        updated = []
        for project in queryset:
            if project.fetch_github():
                updated.append(project.title)
        self.message_user(request, "%s successfully updated." % ', '.join(updated))
    fetch_github.short_description = 'Fetch from Github'

class CommitAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'sha', 'created')
    list_filter = ('created',)
    actions = ['fetch_github', 'fetch_blobs']

    def fetch_github(self, request, queryset):
        fetched = []
        for commit in queryset:
            if commit.fetch_github():
                fetched.append(commit.sha)
        self.message_user(request, 'Successfully fetched %s' % (', '.join(fetched)))
    fetch_github.short_description = 'Fetch commit data'

    def fetch_blobs(self, request, queryset):
        fetched = []
        for commit in queryset:
            if commit.fetch_blobs():
                fetched.append(commit.sha)
        self.message_user(request, 'Successfully fetched blobs for %s' % (', '.join(fetched)))
    fetch_blobs.short_description = 'Fetch blobs for commits'

class BlobAdmin(admin.ModelAdmin):
    pass

class GistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    actions = ['create_gist']
    
    def create_gist(self, request, queryset):
        created = []
        for gist in queryset:
            gist.gist_id = gist.create_gist()
            if gist.gist_id:
                created.append(gist.title)
            gist.save()
        self.message_user(request, "%s successfully created." % ', '.join(created))
    create_gist.short_description = 'Create gist on GitHub'

class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Gist, GistAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(GithubUser, GithubUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(Blob, BlobAdmin)
