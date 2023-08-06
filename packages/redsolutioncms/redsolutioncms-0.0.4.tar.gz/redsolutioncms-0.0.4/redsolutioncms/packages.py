# -*- coding: utf-8 -*-
from xmlrpc_urllib2_transport import ProxyTransport
from django.utils.translation import ugettext as _
from django.conf import settings
from zc.buildout import easy_install
import xmlrpclib
import os
from redsolutioncms.models import CMSSettings, Category
import urllib2
import re
from pkg_resources import parse_version

PYPI_INDEX = 'http://pypi.python.org/simple'


def search_pypi_xmlrpc(query):
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi', transport=ProxyTransport())
    return client.search({'name': query})

def get_package_info(package_name, package_index_url=PYPI_INDEX):
    proxy_handler = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy_handler)
    link_pattern = re.compile('.*<a.*href=[\'"](?P<href>.*?)[\'"].*>(?P<text>[\W\w]*)</a>.*')

    package = {}
    package['name'] = package_name
    package['summary'] = _('No description')
    # Go and find out package versions and screenshots
    url = package_index_url + '/%s/' % package_name
    versions = set()
    for hyperlink in opener.open(url).readlines():
        # Example:
        # <a href="/media/dists/redsolutioncms.django-seo-0.2.0.tar.gz#md5=3bb1437373cc1ce46a216674db75ffa6">
        # redsolutioncms.django-seo-0.2.0.tar.gz</a><br />
        match = re.match(link_pattern, hyperlink)
        if match:
            href, text = match.groups()
            version_match = re.match(
                '.*%s-(?P<version>[\d\.\w]+)(?P<extension>\.tar\.gz|\.zip|\.py\d\.\d\.egg)' % package['name'], href)
            if version_match:
                versions.add(version_match.groupdict()['version'])
            screenshot_match = re.match('(?P<filepath>.+)(?P<extension>\.png|\.jpg|\.gif)', href)
            if screenshot_match:
                # If image hosts on PYPI (relative link)
                if 'http://' not in href:
                    index_root = package_index_url.replace('/simple', '')
                    href = index_root + href
                package['screenshot'] = href
            classifier_match = re.match('http\:\/\/www\.redsolutioncms\.org\/classifiers\/([\w\/]+)', href)
            if classifier_match:
                # Fetch classifiers from links
                package['category'] = classifier_match.groups()

    if versions:
        package['version'] = versions.pop()
        # Do not append packages without versions
        return package

def add_package(packages, package):
    if package['name'] in packages:
        old_package = packages[package['name']]
        new_version = parse_version(package['version'])
        old_version = parse_version(old_package['version'])
        if new_version > old_version:
            packages[package['name']] = package
    else:
        packages.update({package['name']: package})

def search_index(query):
    packages = {}
    if getattr(settings, 'CUSTOM_PACKAGE_INDEX', None):
        # Work with custom /simple/ index
        # http proxy issue
        proxy_handler = urllib2.ProxyHandler()
        opener = urllib2.build_opener(proxy_handler)
        query_pattern = re.compile(
            '.*<a.*href=[\'"](?P<href>.*?)[\'"].*>(?P<text>[\w\.\-]*%s[\w\.\-]*)</a>.*'
             % query)

        for line in opener.open(settings.CUSTOM_PACKAGE_INDEX).readlines():
            # Example:
            # <a href="/simple/redsolutioncms.django-model-url/">redsolutioncms.django-model-url</a><br />
            match = re.match(query_pattern, line)
            if match:
                href, text = match.groups()
                package_info = get_package_info(text, settings.CUSTOM_PACKAGE_INDEX)
                if package_info:
                    add_package(packages, package_info)
    else:
        # Standard way: working with PYPI
        for package in search_pypi_xmlrpc(query):
            package_info = get_package_info(package['name'], PYPI_INDEX)
            if package_info:
                if package_info.get('screenshot'):
                    package['screenshot'] = package_info['screenshot']
                if package_info.get('category'):
                    package['categories'] = package_info['category']
            add_package(packages, package)

    try:
        packages.pop('redsolutioncms')
    except KeyError:
        pass
    return packages

def install(modules, path='parts'):
    '''
    Install module in given path
    Module should be dictionary object, returned by xmlrpc server pypi:
    Example:
        {'_pypi_ordering': 16,
         'name': 'django-tools',
         'summary': 'miscellaneous tools for django',
         'version': '0.10.0.git-ce3ec2d',
    }
    Returns WorkingSet object, 
    see
        http://peak.telecommunity.com/DevCenter/PkgResources#workingset-objects
    terminology:
         http://mail.python.org/pipermail/distutils-sig/2005-June/004652.html
    '''

    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)

    # TODO: If traceback risen here, installation of the all package list fails
    return easy_install.install(['%s==%s' % (module_['name'], module_['version'])
        for module_ in modules], path,
        index=getattr(settings, 'CUSTOM_PACKAGE_INDEX', None),
        use_dependency_links=False)

def load_package_list():
    """
    Creates objects in CMSPackages model for all modules at PYPI
    """
    cms_settings = CMSSettings.objects.get_settings()
    all_packages = search_index('redsolutioncms')

    # Flush old apps?
    cms_settings.packages.all().delete()
    cms_settings.categories.all().delete()
    # fill database again
    # create required catagories
    Category.objects.create(name='frontpage', required=True, settings=cms_settings)
    Category.objects.create(name='templates', required=True, settings=cms_settings)

    for package in all_packages.itervalues():
        cms_package = cms_settings.packages.create(
            selected=False,
            package=package['name'],
            version=package['version'],
            verbose_name=package['name'].replace('django-', '').replace('redsolutioncms.', ''),
            description=package['summary'],
            screenshot=package.get('screenshot'),
        )
        # fill cms_settings foreign key
        cms_settings.packages.add(cms_package)
        if package.get('categories'):
            for category in package['categories']:
                category_obj, created = Category.objects.get_or_create(
                    name=category, settings=cms_settings)
                category_obj.packages.add(cms_package)
        else:
            other_category, created = Category.objects.get_or_create(
                name='other', settings=cms_settings)
            other_category.packages.add(cms_package)

def test():
    print 'Searching module mptt'
    modules = search_index('mptt')
    if modules:
        print 'found %s modules' % len(modules)
    workset = install([modules[0]])
    mptt_distr = workset.by_key['django-mptt']
    print 'Trying to import mptt'
    mptt_distr.activate()
    from mptt.exceptions import InvalidMove
    print 'Successfull!'

if __name__ == '__main__':
    # run with no parameters for basic test case.
    test()
