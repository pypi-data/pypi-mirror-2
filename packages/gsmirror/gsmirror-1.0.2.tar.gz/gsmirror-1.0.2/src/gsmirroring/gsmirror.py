#! /usr/bin/python


__author__="hanis (Jan Rychtar)"


import getopt
import sys


from gsmirroring.site_controller import SiteController


def usage():
    print """
    usage: python gsmirror.py options

    options:
        -s, --site <STRING>       the webspace name of your site (e.g. mySite)
        -d, --domain <STRING>     domain of your Google Apps hosted domain (e.g. example.com)
        -p, --path <STRING>       path where is (will be) the root directory (e.g. /home/me/sites/)
        -n, --name <STRING>       name of the root directory where the site is to be saved (e.g. my_site)
        -t, --templates <STRING>  path to the directory with template files
        -l  --log                 print progress of the mirroring process
        -h, --help                print help for gsmirror
            --email <STRING>      the user's email address or username
            --password <STRING>   the password for the user's account

    examples:
        python gsmirror.py --site=mysite --path=/home/me/sites/ --name=my_site --templates=/home/me/teplates/
             Run the mirroring of the site 'mysite' found in
             the URL http://sites.google.com/site/mysite/ and
             save it into the directory 'my_site' at
             the path '/home/me/sites/' using templates
             at the path '/home/me/teplates/'
        python gsmirror.py -s mysite2 -d mydomain.org -p /home/me/ -n my_site2 -l
             Run the mirroring of the site 'mysite2' hosted on
             a Google Apps domain 'mydomain.org' found in
             the URL http://sites.google.com/a/mydomain.org/mysite2/ and
             save it into the directory 'my_site2' at
             the path '/home/me/' using default templates
             at the path './templates/default_templates/' and during the mirroring will
             print information about a progress.

    templates:
        If you use your own templates (i.e. templates option is specified) then
        there (at the path you specified) have to be five files named as follows:
            'file_cabinet_template.tmpl'
            'announcements_page_template.tmpl'
            'announcement_template.tmpl'
            'listpage_template.tmpl'
            'webpage_template.tmpl'
        If you don't specify templates, default templates will be used.
        Default templates consist of the same five files as above and are stored
        in the directory './templates/default_templates/'.
        For more information about templates check out the readme.txt file or
        default templates.


    path & name:
        These two options determine where the site is to be saved.
        PATH indicate the desired path at the disk where is (will be created)
        a directory named NAME that is supposed to be the root directory in which
        the site will be saved.
        PATH should be an abslolute path and has to end with '/'
        (e.g. /home/john/my_sites/).
        NAME sholud somehow describe the site and has to have the format of the
        direcotry name (e.g. cars_for_sale).
        If NAME isn't specified, the SITE option (site name) is used.
        If PATH isn't specified, the current working directory ('./') is used.

    For more information check out the readme.txt file
    """


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:d:p:n:t:l', ['site=',
                    'domain=', 'path=', 'name=', 'templates=', 'email=',
                    'password=', 'log', 'help'])

    except getopt.error, msg:
        print str(msg)
        usage()
        sys.exit(2)

    site = None
    domain = None
    path = None
    name = None
    templates = None
    log = False
    email = None
    password = None

    for option, arg in opts:
        if option in ('--help', '-h'):
            usage()
            sys.exit()
        elif option in ('--site', '-s'):
            site = arg
        elif option in ('--domain', '-d'):
            domain = arg
        elif option in ('--path', '-p'):
            path = arg
        elif option in ('--name', '-n'):
            name = arg
        elif option in ('--templates', '-t'):
            templates = arg
        elif option == '--email':
            email = arg
        elif option == '--password':
            password = arg
        elif option in ('--log', '-l'):
            log = True

    if not site:
        print 'site argument is missing'
        usage()
        sys.exit(2)

    if not name:
        name=site

    if not path:
        path='./'



    siteController = SiteController(site=site, domain=domain, progression=log,
                    email=email, password=password, templates=templates)

    siteController.process_modification_doc(path=path, directory=name)
    if siteController.modified_since_lasttime():
        site = siteController.get_site()
        siteController.save_site_to_disk(site=site, path=path, directory=name)


if __name__ == "__main__":
    main()


 