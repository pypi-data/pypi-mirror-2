# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns("djangopypi.views",
    url(r'^$', "root", name="djangopypi-root"),
    url(r'^packages/$','packages.index', name='djangopypi-package-index'),
    url(r'^search/$','packages.search',name='djangopypi-search'),
    url(r'^pypi/$', 'root', name='djangopypi-release-index'),
    
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/$','packages.details',
        name='djangopypi-package'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/doap.xml$','packages.doap',
        name='djangopypi-package-doap'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/manage/$','packages.manage',
        name='djangopypi-package-manage'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/manage/versions/$','packages.manage_versions',
        name='djangopypi-package-manage-versions'),
    
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/$',
        'releases.details',name='djangopypi-release'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/doap.xml$',
        'releases.doap',name='djangopypi-release-doap'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/manage/$',
        'releases.manage',name='djangopypi-release-manage'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/metadata/$',
        'releases.manage_metadata',name='djangopypi-release-manage-metadata'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/files/$',
        'releases.manage_files',name='djangopypi-release-manage-files'),
)