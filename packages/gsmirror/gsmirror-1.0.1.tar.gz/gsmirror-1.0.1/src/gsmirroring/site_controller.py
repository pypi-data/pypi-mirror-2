__author__="hanis (Jan Rychtar)"


from Cheetah.Template import Template
import gdata.sites.client
import gdata.sites.data
import gdata.gauth
from BeautifulSoup import BeautifulSoup


import time
import re
import os
import shutil


from objects import Site
from objects import Page
from objects import ListPage
from objects import ListItem
from objects import Date
from objects import LandingPage


from xml_module import ETagDocument



FEED_FETCH_STEP = 300

SOURCE = 'hanis-gsmirror-v1'

DEFAULT_TEMPLATES = './templates/default_templates/'

TMPL_FILE_CABINET = 'file_cabinet_template.tmpl'
TMPL_ANNOUNCEMENTS_PAGE = 'announcements_page_template.tmpl'
TMPL_ANNOUNCEMENT = 'announcement_template.tmpl'
TMPL_LISTPAGE = 'listpage_template.tmpl'
TMPL_WEBPAGE = 'webpage_template.tmpl'


PAGE_NAME = 'index.html'
ETAGS_DOC = 'etags.xml'

#------------possible kinds of content entries------------------------
ANNOUNCEMENT = 'announcement'
ANNOUNCEMENTS_PAGE = 'announcementspage'
ATTACHMENT = 'attachment'
COMMENT = 'comment'
FILE_CABINET = 'filecabinet'
LIST_ITEM = 'listitem'
LIST_PAGE = 'listpage'
WEBPAGE = 'webpage'
WEB_ATTACHMENT = 'webattachment'

PAGE_TYPES = [ANNOUNCEMENTS_PAGE, ANNOUNCEMENT, FILE_CABINET, WEBPAGE, LIST_PAGE]
#---------------------------------------------------------------------


class SiteController():
    """
    The key class that provides the functionality for connecting to the Google
    Sites, downloaading site content, processing content, applying templates
    and saving to the disk.
    """

    def __init__(self, site, domain=None, templates=None, progression = False, email=None, password=None):
        """
        Creates a new Site Controller
        
        Args:
            site: the webspace name of your site (e.g. mySite)
            domain: domain of your Google Apps hosted domain (e.g. example.com)
            templates: path to the directory with template files
            progression: if True, print progress of the mirroring process
            email: the user's email address or username
            password: the password for the user's account
        """

        if domain:
            self.client = gdata.sites.client.SitesClient(source=SOURCE, site=site, domain=domain)
        else:
            self.client = gdata.sites.client.SitesClient(source=SOURCE, site=site)

        self.progression = progression

        if templates:
            self.templates_path = templates
        else:
            self.templates_path = DEFAULT_TEMPLATES

        if password:
            self.client.client_login(email=email, password=password, source = self.client.source)

        self.etag_new = ETagDocument()
        self.etag_old = None
        self.landing_page = None



    def process_modification_doc(self, path, directory):
        """
        The method serves for checking whether or not the site has been mirrored
        before (ie. there is a file etags.xml at the path path/directory/ that
        contatins information about the last mirroring).
        In case this is the first mirroring of the site, the class attribute
        etag_old is set to None, which means that the mirroring process will
        crates a directory hierarchy and save all the current content of the
        site to the disk.
        In case the site has been mirrored before (to the same path),
        information about the last mirroring are set to etag_old (from
        path/directory/etags.xml), which means that the mirroring process will
        continue only if there has been some changes since the last time and
        will download and save only new or modified attachments.
        Args:
            path: path where is (will be) the root directory (e.g. /home/me/sites/)
            directory: name of the root directory where the site is to be saved (e.g. my_site)
        """
        path_to_etags = path + directory + '/' + ETAGS_DOC
        if os.access(path_to_etags, os.F_OK):
            self.etag_old = ETagDocument()
            self.etag_old.get_document(path_to_etags)
        self.etag_new.create()


    def modified_since_lasttime(self):
        """
        Returns: True if either it is the first mirroring of the site (etag_old
                    is set to None), or the sites has been modified since the
                    last time.
                 False if it's not the first mirroring and the site hasn't been
                 modified since the last time.
        """
        if self.etag_old:
            uri = '%s?max-results=%s' % (self.client.MakeActivityFeedUri(), 1)
            feed = self.client.GetActivityFeed(uri=uri)
            updated = Date(feed.entry[0].updated.text).get_unix_time()
            last_mirroring = self.etag_old.get_modification_time()
            return float(updated) > float(last_mirroring)
        else:
            return True



    def get_template(self, template_path):
        file_template = open(template_path, 'r')
        templateDef = file_template.read()
        file_template.close()
        return Template(templateDef)


    def save_as_file(self, content, path):
        outfile = file(path , 'w')
        outfile.write(content)
        outfile.close()


    def download_attachments(self):
        uri = '%s?kind=%s' % (self.client.make_content_feed_uri(), 'attachment')
        feed = self.client.GetContentFeed(uri=uri)
        for entry in feed.entry:
            self.client.DownloadAttachment(entry, OUTPUT_PATH + entry.title.text)



    def request_page_content(self, page_id):
        uri = '%s%s' % (self.client.make_content_feed_uri(), page_id)
        response = self.client.request(method='GET', uri=uri)
        content_str = str(response.read())
        return BeautifulSoup(content_str[content_str.find('<content'): content_str.find('</content>') + 10]).prettify()



    def get_site_path(self):
        if self.client.domain == 'site':
            path = 'http://sites.google.com/site/%s/' % (self.client.site)
        else:
            path = 'http://sites.google.com/a/%s/%s/' % (self.client.domain, self.client.site)
        return path

    def get_site_short_path(self):
        if self.client.domain == 'site':
            path = '/site/%s/' % (self.client.site)
        else:
            path = '/%s/%s/' % (self.client.domain, self.client.site)
        return path



    def parse_comment(self, comment):
        temp = comment[comment.find('<td'):comment.rfind('</td')]
        return temp[temp.find('>')+1:]



    def replace_paths(self, page_content, level, page):
        site_path = self.get_site_path()
        link_list = re.findall(r'<a href="'+ site_path +'.*?"', page_content)
        if self.landing_page.id == page.id:
            level = 0
        for link in link_list:
            att_test = link.find('?attredirects')            
            if att_test == -1:
                if link.endswith(self.landing_page.path, 0, -1):
                    relative_path = level * '../'
                    new_link = '<a href="%s%s"' % (relative_path, PAGE_NAME)
                else:
                    relative_path = level * '../' + link[len(site_path)+9:-1]
                    new_link = '<a href="%s/%s"' % (relative_path, PAGE_NAME)
            else:
                relative_path = level * '../' + link[len(site_path)+9:att_test]
                new_link = '<a href="%s"' % (relative_path)
            page_content = page_content.replace(link, new_link)

        #in one particular case there are links that don't start with htttp://sites/google ??!!
        #so this is considered as a temporary patch
        site_short_path = self.get_site_short_path()
        link_list = re.findall(r'<a href="'+ site_short_path +'.*?"', page_content)
        if self.landing_page.id == page.id:
            level = 0
        for link in link_list:
            att_test = link.find('?attredirects')
            if att_test == -1:
                if link.endswith(self.landing_page.path, 0, -1):
                    relative_path = level * '../'
                    new_link = '<a href="%s%s"' % (relative_path, PAGE_NAME)
                else:
                    relative_path = level * '../' + link[len(site_short_path)+9:-1]
                    new_link = '<a href="%s/%s"' % (relative_path, PAGE_NAME)
            else:
                relative_path = level * '../' + link[len(site_short_path)+9:att_test]
                new_link = '<a href="%s"' % (relative_path)
            page_content = page_content.replace(link, new_link)
        #-------------------------------------------------------------------------------
        return page_content



    def replace_attachment_source(self, page, attachment, parent, as_announcement=None):
        site_path = self.get_site_path()
        current_src='%s_/rsrc/[^>]*/%s%s' % (site_path, parent.path, attachment.name)
        src_list = re.findall(r''+current_src, page)        
        if as_announcement:
            new_src='./%s/%s' % (parent.pagename, attachment.name)
        else:
            new_src=attachment.link
        for src_item in src_list:
            page = page.replace(src_item, new_src)
        return page



    def save_site_to_disk(self, site, path, directory):
        """
        The method save the site to the disk to the path path/directory/.
        First, it removes attachments and pages that were saved last time and
        are not in the current version.

        Args:
            site: The output of the method get_site
            path: path where is (will be) the root directory (e.g. /home/me/sites/)
            directory: name of the root directory where the site is to be saved (e.g. my_site)
        """
        path_to_site = path + directory + '/'

        if self.etag_old:
            self.remove_unused(attachments=self.etag_old.get_unused_attachments(), pages=self.etag_old.get_unused_pages(), path=path_to_site)

        if not os.access(path_to_site, os.F_OK):
            os.mkdir(path_to_site)

        for child in site.childs:
            self.save_page_to_disk(page=child, path=path_to_site, site=site)

        self.etag_new.set_modification_time(str(time.time()))
        self.save_as_file(content=self.etag_new.to_string(), path=path_to_site + ETAGS_DOC)


    def remove_unused(self, attachments, pages, path):
        for attachment in attachments:
            if os.access(attachment[1], os.F_OK):
                if self.progression:
                    print 'removing unused attachment: ' + attachment[1]
                os.remove(attachment[1])
        for page in pages:
            abs_path = path + page[1]
            if os.access(abs_path, os.F_OK):
                if self.progression:
                    print 'removing unused page: ' + abs_path
                shutil.rmtree(abs_path)



    def save_page_to_disk(self, page, path, site):    
        full_path = path + page.path

        if not os.access(full_path, os.F_OK):
            if self.progression:
                print 'creating directory: ' + full_path
            os.mkdir(full_path)

        if self.progression:
            print 'saving page: ' + page.pagename

        self.etag_new.add_element(id=page.id,
                source=page.path, etag=page.etag, type=self.etag_new.PAGE)

        if page.kind == WEBPAGE:
            template_out = self.get_template(self.templates_path + TMPL_WEBPAGE)
        elif page.kind == FILE_CABINET:
            template_out = self.get_template(self.templates_path + TMPL_FILE_CABINET)
        elif page.kind == ANNOUNCEMENTS_PAGE:
            template_out = self.get_template(self.templates_path + TMPL_ANNOUNCEMENTS_PAGE)
        elif page.kind == ANNOUNCEMENT:
            template_out = self.get_template(self.templates_path + TMPL_ANNOUNCEMENT)
        elif page.kind == LIST_PAGE:
            template_out = self.get_template(self.templates_path + TMPL_LISTPAGE)
            
        template_out.page = page
        template_out.site = site

        if (page.id == self.landing_page.id):
            page_path = path
        else:
            page_path = full_path

        self.save_as_file(content=str(template_out), path=page_path + PAGE_NAME)

        for attachment in page.attachments:
            self.save_attachment_to_file(attachment, full_path)

        for child in page.childs:
            self.save_page_to_disk(child, path, site=site)



    def save_attachment_to_file(self, attachment, path):
        uri = '%s%s' % (self.client.MakeContentFeedUri(), attachment.id)
        att_entry = self.client.GetEntry(uri, desired_class=gdata.sites.data.ContentEntry)
        
        self.etag_new.add_element(id=attachment.id,
                source=path + attachment.name, etag=attachment.etag, type=self.etag_new.ATTACHMENT)
        if attachment.save:
            if self.progression:
                print 'saving attachment: ' + path + attachment.name
            self.client.DownloadAttachment(att_entry, path + attachment.name)
        elif self.progression:
            print 'omitting attachment: ' + path + attachment.name


    def get_landing_page(self):
        uri = '%s?path=/' % (self.client.MakeContentFeedUri())
        feed = self.client.GetContentFeed(uri=uri)
        entry = feed.entry[0]
        path=entry.GetAlternateLink().href
        rel_path = path[len(self.get_site_path()):]
        return LandingPage(id=entry.GetNodeId(), pagename=entry.page_name.text,
            path=entry.GetAlternateLink().href, rel_path=rel_path)


    def get_site(self):
        """
        This method downloads all the current site content (except of
        attachments) to the memory.

        Returns: objects.Site representing all the content of the mirrored site
        """
        site = Site()
        if self.progression:
            print 'downloading site'
        self.landing_page = self.get_landing_page()
        step = 0
        while True:
            uri = '%s?start-index=%s&max-results=%s' % (self.client.MakeContentFeedUri(), step*FEED_FETCH_STEP + 1, (FEED_FETCH_STEP - 1))
            feed = self.client.GetContentFeed(uri=uri)
            step+=1
            if not feed.entry: break
            for entry in feed.entry:
                if entry.FindParentLink() is None and entry.Kind() in PAGE_TYPES:
                    self.get_page(entry, level=1, parent=site)
        return site



    def get_site_content(self, level=1, parent=None):
        if self.progression:
            print 'downloading ocontent of: ' + parent.pagename
        step = 0
        while True:
            uri = '%s?parent=%s&start-index=%s&max-results=%s' % (self.client.MakeContentFeedUri(),
                        parent.id, step*FEED_FETCH_STEP + 1, (FEED_FETCH_STEP - 1))
            feed = self.client.GetContentFeed(uri=uri)
            step+=1
            if not feed.entry: break
            for entry in feed.entry:
                kind = entry.Kind()
                if kind in PAGE_TYPES:
                    self.get_page(entry, level, parent)
                if kind == ATTACHMENT:
                    self.get_attachment(entry, parent=parent)
                elif kind == COMMENT:
                    self.get_comment(entry, parent)
                elif kind == LIST_ITEM:
                    self.get_list_item(entry, parent)
                elif kind == WEB_ATTACHMENT:
                    self.get_web_attachment(entry, parent)


    def get_page(self, entry, level, parent):
        if self.progression:
            print 'downloading page: ' + entry.page_name.text
        landing = (entry.GetNodeId() == self.landing_page.id)

        page = Page(id=entry.GetNodeId(),
                    kind=entry.Kind(),
                    title=entry.title.text,
                    author_name=entry.author[0].name.text,
                    author_email=entry.author[0].email.text,
                    updated=entry.updated.text,
                    revision=entry.revision.text,
                    pagename=entry.page_name.text,
                    parent=parent,
                    etag=entry.etag,
                    landing=landing)

        if self.etag_old:
            self.etag_old.check_page(page.id, page.path)

        if page.kind == LIST_PAGE:
            list_page = ListPage()
            for header in entry.data.column:
                list_page.add_header(header.name)
            page.list_items = list_page

        content_str = self.request_page_content(entry.GetNodeId())
        self.get_site_content(level=level+1, parent=page)


        if page.landing:
            for attachment in page.attachments:
                attachment.link = './' + self.landing_page.rel_path + '/' + attachment.name
                

        if page.kind == ANNOUNCEMENT:
            content_str2 = content_str
            content_str2 = self.replace_paths(page_content=content_str2, level=level-1, page=page)
            for attachment in page.attachments:
                content_str2 = self.replace_attachment_source(page=content_str2, attachment=attachment, parent=page, as_announcement=True)
            page.embedded_content = content_str2

        content_str = self.replace_paths(page_content=content_str, level=level, page=page)
        for attachment in page.attachments:
            content_str = self.replace_attachment_source(page=content_str, attachment=attachment, parent=page)
        page.content = content_str
        parent.add_child(page)



    def get_list_item(self, entry, parent):
        if self.progression:
            print 'downloading list item at: ' + parent.pagename
        item = ListItem(author_name=entry.author[0].name.text,
                        author_email=entry.author[0].email.text,
                        updated=entry.updated.text,
                        revision=entry.revision.text)

        for cell in entry.field:
            item.add_cell(cell.text)
        parent.list_items.add_list_item(item)


    def get_attachment(self, entry, parent):
        if self.progression:
            print 'downloading attachment information: ' + entry.title.text
        if self.etag_old:
            save = self.etag_old.check_attachment(id=entry.GetNodeId(), etag=entry.etag)
        else:
            save = True
        parent.add_attachment(id=entry.GetNodeId(),
                                etag=entry.etag,
                                author_name=entry.author[0].name.text,
                                author_email=entry.author[0].email.text,
                                name=entry.title.text,
                                summary=entry.summary.text,
                                updated=entry.updated.text,
                                revision=entry.revision.text,
                                save = save)


    def get_web_attachment(self, entry, parent):
        if self.progression:
            print 'downloading webattachment: ' + entry.title.text
        parent.add_web_attachment(id=entry.GetNodeId(),
                                author_name=entry.author[0].name.text,
                                author_email=entry.author[0].email.text,
                                name=entry.title.text,
                                summary=entry.summary.text,
                                updated=entry.updated.text,
                                revision=entry.revision.text,
                                web_src=str(entry.content.src))



    def get_comment(self, entry, parent):
        if self.progression:
            print 'downloading comment at: ' + parent.pagename
        parent.add_comment(text=self.parse_comment(self.request_page_content(entry.GetNodeId())),
                            author_name=entry.author[0].name.text,
                            author_email=entry.author[0].email.text,
                            updated=entry.updated.text,
                            revision=entry.revision.text)




if __name__ == "__main__":
    pass


