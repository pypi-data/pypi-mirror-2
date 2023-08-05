
__author__="hanis (Jan Rychtar)"


from xml.dom import minidom


class ETagDocument():
    """
         Representation of an XML file that contains information about
         the state of the site elements such as timestamp of the last
         mirroring, list of attachments and list of pages (where each
         list item consist of ETag of attachment (page), attachment (page) ID
         and path to the attachment (page))

         An ETagDocument is used in two ways
         case 1) To hold information about the last mirroring
         case 2) To collect information about the current mirroring
    """

    ATTACHMENT = 'attachment'
    PAGE = 'page'


    def __init__(self):
        self.document=None
        self.attachment_map = {}
        self.page_map = {}

    def create(self):
        """
        The method is used in case 2. It creates a new document
        """
        self.document = minidom.Document()
        site_element = self.document.createElement('site')        
        self.document.appendChild(site_element)

        attachments_element = self.document.createElement('attachments')
        pages_element = self.document.createElement('pages')
        site_element.appendChild(attachments_element)
        site_element.appendChild(pages_element)


    def set_modification_time(self, time):
        """
        The method is used in case 2. It adds a timestamp of the current 
        mirroring to the document
        """
        self.document.getElementsByTagName('site')[0].setAttribute('updated', time)



    def check_attachment(self, id, etag):
        """
        The method is used in case 1. It checks if an attachment with ID=id and
        ETag=etag was added or modified since the last time. If not,
        the attachment is removed from the attachment_map.

        Args:
            id: The ID of the attachment to be checked
            etag: The ETag of the attachment to be checked
        Returns:
            True if the ETagDocument contains an attachment with ID=id and
            ETag=etag
            False otherwise
        """
        if self.attachment_map.has_key(id) and self.attachment_map[id][0] == etag:
            del self.attachment_map[id]
            return False
        else:
            return True


    def check_page(self, id, source):
        """
        The method is used in case 1. It checks if an page with ID=id
        source=source was added or moved since the last time. If not,
        the page is removed from the page_map.

        Args:
            id: The ID of the page to be checked
            source: The source of the page to be source
        """
        if self.page_map.has_key(id) and self.page_map[id][1] == source:
            del self.page_map[id]




    def get_unused_pages(self):
        """
        The method is used in case 1. Returns pages that weren't removed from
        the page_map while using check_page method

        Returns: List containing tuples of the form [etag, source]
        """
        return self.page_map.values()


    def get_unused_attachments(self):
        """
        The method is used in case 1. Returns attachments that weren't removed
        from the attachment_map while using check_attachment method

        Returns: List containing tuples of the form [etag, source]
        """
        return self.attachment_map.values()


    def add_element(self, id, source, etag, type):
        """
        The method is used in case 2. Adds an element to the XML document
        representing by the ETagDocument.
        The element consists of three attributes (id, source, etag) that hold
        information about either attachment or page (according to the type)
        Args:
            id: ID of the attachment (page)
            source: Path to the attachment (page)
            etag: ETag of the attachment (page)
            type: Type of the element, possible types are 'attachment' and 'page'
        """
        element = self.document.createElement(type)
        element.setAttribute('id', str(id))
        element.setAttribute('source', str(source))
        element.setAttribute('etag', str(etag))
        self.document.getElementsByTagName(self.get_parent_element(type))[0].appendChild(element)



    def get_parent_element(self, type):
        if type == self.ATTACHMENT:
            return 'attachments'
        elif type == self.PAGE:
            return 'pages'



    def get_modification_time(self):
        """
        The method is used in case 1. It gets a timestamp from the last
        mirroring
        """
        return self.document.getElementsByTagName('site')[0].getAttribute('updated')



    def get_document(self, path):
        """
        The method is used in case 1. It parses an XML document at the path and 
        procces it (ie. fill page_map and attachment_map)
        
        Args:
            path: A path to the etag XML document
        """
        self.document = minidom.parse(path)
        for node in self.document.getElementsByTagName('attachment'):
            self.attachment_map[node.getAttribute('id')]=[node.getAttribute('etag'),node.getAttribute('source')]
        for node in self.document.getElementsByTagName('page'):
            self.page_map[node.getAttribute('id')]=[node.getAttribute('etag'),node.getAttribute('source')]


        
    def to_string(self):
        return self.document.toprettyxml(encoding='UTF-8')



if __name__ == "__main__":
    pass
    