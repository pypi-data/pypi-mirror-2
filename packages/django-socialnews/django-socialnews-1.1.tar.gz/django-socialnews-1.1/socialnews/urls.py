from django.conf.urls.defaults import *
from django.contrib.auth import views
from django.views.generic import simple
from django.views.generic.simple import direct_to_template
from news.rss import LatestEntriesByTopic, LatestEntries

urlpatterns = patterns('',
    # Example:
    # (r'^implist/', include('implist.foo.urls')),
    
    (r'^google42f6e952fe543f39.html$', direct_to_template, {'template':'news/test.txt', 'mimetype':'text/plain'}),
    (r'^robots.txt$', direct_to_template, {'template':'news/robots.txt', 'mimetype':'text/plain'}),
    (r'^foo/$', direct_to_template, {'template':'news/base.html'}),
    (r'^admin/', include('django.contrib.admin.urls')),
    url(r'^logout/$', views.logout, {'template_name':'registration/logout.html'}, name='logout'),
    
    
)

urlpatterns += patterns('news.accounts',
    url(r'^register/$', 'create_user', name='register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^user/reset_password/$', 'reset_password', name='reset_password'),
    url(r'^user/reset_password/sent/$', 'reset_password_sent', name='reset_password_sent'),
    url(r'^user/reset_password/done/(?P<username>[^\.^/]+)/$', 'reset_password_done', name='reset_password_done'),
    url(r'^user/activate/(?P<username>[^\.^/]+)/$', 'activate_user', name='activate_user'),                       
    url(r'^my/$', 'user_manage', name='user_manage'),
)                        

urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'G:/tapicks/news/templates/site_media'}),
        (r'^dummy/', simple.direct_to_template, {'template':'news/dummy.html'})
    )

urlpatterns += patterns('news.subscriptions',
    url(r'^subscribe/(?P<topic_name>[^\.^/]+)/$', 'subscribe', name='subscribe'),
    url(r'^unsubscribe/(?P<topic_name>[^\.^/]+)/$', 'unsubscribe', name='unsubscribe'),
    
)

urlpatterns += patterns('news.search',
    url(r'^search/$', 'search', name='search'),
)

urlpatterns +=patterns('news.users',
    url(r'^user/(?P<username>[^\.^/]+)/$', 'user_main', name='user_main'),
    url(r'^user/(?P<username>[^\.^/]+)/comments/$', 'user_comments', name='user_comments'),
    url(r'^user/likedlinks/(?P<username>[^\.^/]+)/(?P<secret_key>[^\.^/]+)/$', 'liked_links_secret', name='liked_links_secret'),
    url(r'^my/liked/$', 'liked_links', name='liked_links'),
    url(r'^my/disliked/$', 'disliked_links', name='disliked_links'),
    url(r'^my/saved/$', 'saved_links', name='saved_links'),
)

urlpatterns += patterns('news.static',
    url(r'^aboutus/$', 'aboutus', name='aboutus'),
    url(r'^help/$', 'help', name='help'),
    url(r'^help/$', 'help', name='help'),
    url(r'^buttons/$', 'buttons', name='buttons'),
)                      

urlpatterns += patterns('news.tags',
    url(r'^(?P<topic_name>[^\.^/]+)/tag/(?P<tag_text>[^\.^/]+)/$', 'topic_tag', name='topic_tag'),
    url(r'^tag/(?P<tag_text>[^\.^/]+)/$', 'sitewide_tag', name='sitewide_tag'),
)

feeds = {
    'latest': LatestEntries,
    'topics': LatestEntriesByTopic,
}

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('news.links',
    url(r'^submit/$', 'link_submit', name='link_submit_def'),                        
    url(r'^(?P<topic_name>[^\.^/]+)/submit/$', 'link_submit', name='link_submit'),
    url(r'^up/(?P<link_id>\d+)/$', 'upvote_link', name='upvote_link'),
    url(r'^down/(?P<link_id>\d+)/$', 'downvote_link', name='downvote_link'),
    url(r'^save/(?P<link_id>\d+)/$', 'save_link', name='save_link'),
    url(r'^upcomment/(?P<comment_id>\d+)/$', 'upvote_comment', name='upvote_comment'),
    url(r'^downcomment/(?P<comment_id>\d+)/$', 'downvote_comment', name='downvote_comment'),
    url(r'^(?P<topic_name>[^\.^/]+)/comment/(?P<comment_id>\d+)/$', 'comment_detail', name='comment_detail'),
    url(r'^(?P<topic_name>[^\.^/]+)/(?P<link_id>\d+)/$', 'link_details', name='link_detail'),
    url(r'^(?P<topic_name>[^\.^/]+)/(?P<link_id>\d+)/info/$', 'link_info', name='link_info'),
    url(r'^(?P<topic_name>[^\.^/]+)/(?P<link_id>\d+)/related/$', 'link_related', name='link_related'),
)

urlpatterns += patterns('news.topics',
    url(r'^$', 'main', name='main'),
    url(r'^new/$', 'main', {'order_by':'new'}, name='new'),
    url(r'^all/$', 'main', {'order_by':'new', 'override':'all'}, name='new'),
    url(r'^recommended/$', 'recommended',  name='recommended'),                        
    url(r'^createtopic/', 'create', name='createtopic'),
    url(r'^about/$', 'site_about', name='site_about'),
    url(r'^topics/$', 'topic_list', name='topic_list'),
    
    url(r'^(?P<topic_name>[^\.^/]+)/$', 'topic_main', name='topic'),
    url(r'^(?P<topic_name>[^\.^/]+)/new/$', 'topic_main', {'order_by':'new'}, name='topic_new', ),
    url(r'^(?P<topic_name>[^\.^/]+)/manage/$', 'topic_manage', name='topic_manage'),
    url(r'^(?P<topic_name>[^\.^/]+)/about/$', 'topic_about', name='topic_about'),
)  