"""
This module provides several classes that represent Google Sites entities.
Classes are used for storing data and the subsequent usage in templates.
"""

__author__="hanis (Jan Rychtar)"


import time
import calendar


PAGE_NAME = 'index.html'



class Author():
    def __init__(self, name, email):
        self.email = email
        self.name = name


class CollectiveObject:
    """
    Represents attributes thet are common to all objects and defines methods for
    setting the attributes
    """
    revision = None
    updated = None
    author = None
    def set_author(self, author_name, author_email):
        self.author = Author(author_name, author_email)
    def set_date_and_revision(self, updated, revision):
        self.updated = Date(updated)
        self.revision = revision


class Commentable():
    """
    Classes that represents entities which may store comments inherit a method
    for adding comments from this class.
    """
    def add_comment(self, text, author_name, author_email, updated, revision):        
        self.comments.append(Comment(text, author_name, author_email, updated, revision))


class Parent():
    """
    Classes that represents entities which may store subpages
    (e.g. webpages) inherit a method for adding subpages from this class.
    """
    def add_child(self, child):
        self.childs.append(child)


class Attachmentable():
    """
    Classes that represents entities which may store attachments or 
    webattachments inherit from methods for adding attachments and 
    webattachments this class.
    """
    def add_attachment(self, id, etag, author_name, author_email, name, summary, updated, revision, save):
        self.attachments.append(Attachment(id, author_name, author_email, name, summary, updated, revision, etag=etag, save=save))
    def add_web_attachment(self, id, author_name, author_email, name, summary, updated, revision, web_src):
        self.web_attachments.append(Attachment(id, author_name, author_email, name, summary, updated, revision, web_src))



class Site(Parent, Attachmentable):
    """
    Represents the root object that store all entities of the site
    """
    def __init__(self):
        self.childs = []
        self.attachments = []
        self.path=''
        self.path_to_root=''
        self.landing_page_id = 0
        self.landing=False

    def get_landing_page(self):
        for child in self.childs:
            if child.landing:
                return child

    def get_non_landing_pages(self):
        childs = []
        for child in self.childs:
            if not child.landing:
                childs.append(child)
        return childs


class LandingPage():
    def __init__(self, id, pagename, path, rel_path):
        self.id=id
        self.pagename=pagename
        self.path=path
        self.rel_path=rel_path        



class Page(CollectiveObject, Commentable, Parent, Attachmentable):
    """
    Represents webpages, file cabinets, announcement pages, announcements anad 
    list pages
    """
    def __init__(self, id, title, pagename, kind, author_name, author_email,
                    updated, revision, parent, content=None,
                    embedded_content=None, etag=None, landing=False):
        self.id = id
        self.etag = etag
        self.kind = kind
        self.set_author(author_name, author_email)
        self.set_date_and_revision(updated, revision)
        self.title = title
        self.content = content
        self.embedded_content = embedded_content #only for announcemects
        self.comments = [] #list of comments
        self.childs = [] #list of subpages
        self.attachments = [] #list of attachments
        self.web_attachments = [] #only for file cabinets
        self.parent = parent
        self.pagename = pagename
        self.landing = landing
        #self.subpage_path = './' + self.pagename + '/' + PAGE_NAME
        self.path=self.parent.path + self.pagename + '/'
        self.path_to_root=parent.path_to_root + '../'
        self.list_items=None #only for list pages        

    def get_path_to_root(self):
        if self.landing:
            return './'
        else:           
            return self.path_to_root


    def get_predecessors(self):
        """
        Returs the list of all predecessors (except the object representing the
        site) sorted by distance from the page in increasing order
        """
        predecessors = []
        page = self
        while True:
            page = page.parent
            if isinstance(page, Site):
                break
            predecessors.append(page)
        predecessors.reverse()
        return predecessors


    def get_announcements(self):
        """
        Returns list of subpages that represents announcements
        """
        announcements = []
        for page in self.childs:
            if page.kind == 'announcement':
                announcements.append(page)
        return announcements



    def get_alternative_path_to(self, page):
        if self.landing:
            if page.landing:
                alt = './' + PAGE_NAME
            else:
                alt = page.path_to_root + PAGE_NAME
        elif page.landing:
            alt = self.path + PAGE_NAME
        else:
            alt = page.path_to_root + self.path + PAGE_NAME
        return alt




class Comment(CollectiveObject):
    def __init__(self, text, author_name, author_email, updated, revision):
        self.set_author(author_name, author_email)
        self.text = text
        self.set_date_and_revision(updated, revision)



class Attachment(CollectiveObject):
    def __init__(self, id, author_name, author_email, name, summary, updated, revision, web_src=None, etag=None, save=False):
        self.id = id
        self.etag = etag
        self.set_author(author_name, author_email)
        self.summary = summary
        self.name = name
        self.set_date_and_revision(updated, revision)
        self.link = './' + name
        self.web_src = web_src #only for web attachments
        self.save = save


class ListPage():
    def __init__(self):
        self.headers = []
        self.items = []
    def add_header(self, header):
        self.headers.append(header)
    def add_list_item(self, item):
        self.items.append(item)



class ListItem(CollectiveObject):
    def __init__(self, author_name, author_email, updated, revision):
        self.cells = []
        self.set_author(author_name, author_email)
        self.set_date_and_revision(updated, revision)
    def add_cell(self, cell):
        self.cells.append(cell)




class Date():
    """
    Google Sites API use the format ISO8601 for datetime of the form:
    yyyy-mm-ddThh:mm:ss.mmmZ
    Since such a format isn't suitable for web pages, this class allows
    the script to choose an arbitrary format (set in a template) for displaying
    datetime strings.
    """
    def __init__(self, date_string=None, unix_time=None):
        """
        Exactly one argument is admissible. 
        
        Args:
            date_string: String of the form "yyyy-mm-ddThh:mm:ss.mmmZ" (ISO8601).            
            unix_time: Number of seconds since the Unix Epoch 
                (January 1 1970 00:00:00 GMT)                    
        """
        if date_string:
            temp = date_string[0:date_string.find('.')]
            self.date = time.strptime(temp, '%Y-%m-%dT%H:%M:%S')
        elif unix_time:
            self.date = time.gmtime(unix_time)


    def get_unix_time(self):
        return calendar.timegm(self.date)



    def format(self, format=None):
        """            
            Args:
                format: String specifying the format of a datetime, where
                    String consists of directives (see python time module) and 
                    other additional letters.
            Returns: String representing a datetime of a form specified in 
            format argument
        """
        if format is None:
            format = '%B %d, %Y, %I:%M %p'
        return time.strftime(format, self.date)


    def get_current_unix_time(self):
        return time.time()


if __name__ == "__main__":
    pass
