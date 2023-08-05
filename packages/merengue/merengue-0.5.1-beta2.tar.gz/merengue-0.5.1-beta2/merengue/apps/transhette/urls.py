from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('transhette.views',
    url(r'^$', 'home', name='transhette-home'),
    url(r'^restart/$', 'restart_server', name='transhette-restart-server'),
    url(r'^apply_changes/$', 'do_restart', name='apply_changes'),
    url(r'^pick/$', 'list_languages', name='transhette-pick-file'),
    url(r'^download/$', 'download_file', name='transhette-download-file'),
    url(r'^select/(?P<langid>[\w\-]+)/(?P<idx>\d+)/$', 'lang_sel', name='transhette-language-selection'),
    url(r'^set_new_translation/$', 'set_new_translation', name='set_new_translation'),
    url(r'^inline_demo/$', 'inline_demo', name='inline_demo'),
    url(r'^update/confirmation/$', 'update_confirmation', name='transhette-confirmation-file'),
    url(r'^update/file/((?P<no_confirmation>\w+)/)?$', 'update', name='transhette-update-file'),
    url(r'^update/catalogue/((?P<no_confirmation>\w+)/)?$', 'update_catalogue', name='transhette-update-catalogue'),
    url(r'^change/catalogue/$', 'change_catalogue', name='transhette-change-catalogue'),
    url(r'^translation_conflicts/$', 'translation_conflicts', name='translation_conflicts'),
    url(r'^ajax/$', 'ajax', name='transhette-ajax'),
)
