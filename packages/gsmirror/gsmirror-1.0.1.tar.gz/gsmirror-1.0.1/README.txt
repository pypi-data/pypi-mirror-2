



====TABLE OF CONTENT=====
 1. ABOUT THE SCRIPT
 2. REQUIREMENTS
 3. INSTALLATION
 4. USAGE
  4.1 RUNNING THE SCRIPT   
  4.2 STRUCTURE OF THE MIRRORING SITE
  4.3 XML DOCUMENT etags.xml
  4.4 MIRRORING THE SITE AGAIN
  4.5 USAGE OF TEMPLATES
   4.5.1 BASICS AND EXAMPLES
   4.5.2 HANDLING THE LAYOUTS

1 ABOUT THE SCRIPT

The gsmirror script is a tool for exporting Google Sites to the disk as html pages.
It uses Google Data API for interacting with Google Sites and Cheetah Template Engine
for customizing the appearance of web pages. The main idea of using the script is to
mirror the same site to the same path periodically (e.g. once a day), so it is possible
to edit the site at Google Sites, but the site will be somewhere else with the desired
appearance and will be periodically updated to the current version.



2 REQUIREMENTS

To use the gsmirror script, you'll need:
 - Python 2.2+ (however, version 2.5 or higher is recommended)
 - Google Data Python client library
        -can be downloaded at http://code.google.com/p/gdata-python-client/downloads/list
        -see http://code.google.com/intl/cs/apis/gdata/articles/python_client_lib.html for help installing
 - Cheetah, The Python-Powered Template Engine
        -can be downloaded at http://www.cheetahtemplate.org/
        -see http://www.cheetahtemplate.org/docs/users_guide_html/users_guide.html#SECTION000410000000000000000
         for requirements and installation




3 INSTALLATION
  TODO


4 USAGE



4.1 RUNNING THE SCRIPT   

To run the script get to the directory with the gsmirror.py file and type:
    python gsmirror.py [options]

where possible options are:
    -s, --site <STRING>       the webspace name of your site (e.g. mySite)
                              (compulsory)
    -d, --domain <STRING>     domain of your Google Apps hosted domain (e.g. example.com)
                              (optional)
    -p, --path <STRING>       path where is (will be) the root directory (e.g. /home/me/sites/)
                              (optional) more information in path & name paragraph
    -n, --name <STRING>       name of the root directory where the site is to be saved (e.g. my_site)
                              (optional) more information in path & name paragraph
    -t, --templates <STRING>  path to the directory with template files
                              (optional)
    -l  --log                 print progress of the mirroring process
                              (optional)
        --email <STRING>      the user's email address or username
                              (optional)
        --password <STRING>   the password for the user's account
                              (optional)
    -h, --help                print help for gsmirror



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



    examples with existing sites
        python gsmirror.py -s www -d staremapy.cz -n staremapy -t ./templates/staremapy_templates/ -l
            Creates a root directory 'staremapy' at the current working
            directory and into this directory export a site
            http://sites.google.com/a/staremapy.cz/www/
            Use templates from ./staremapy_templates/

        python gsmirror.py -s gsmirrortest -l
            Creates a root directory 'gsmirrortest' at the current working
            directory and into this directory export a site
            http://sites.google.com/site/gsmirrortest/



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
        Usage of templates is described in paragraph below USAGE OF TEMPLATES


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




4.2 STRUCTURE OF THE MIRRORING SITE

The directory structure of the mirroring site is of the form as follows:
    -ROOT_DIRECTORY and PATH_TO_ROOT_DIRECTORY are specified in gsmirror options
    -A top-level page PAGENAME (located at http://sites.google.com/site/MY_SITE/PAGENAME)
     is saved in a file index.html in PATH_TO_ROOT_DIRECTORY/ROOT_DIRECTORY/PAGENAME/
    -A subpage SUBPAGE of PAGENAME (located at http://sites.google.com/site/MY_SITE/PAGENAME/SUBPAGE)
     is saved in a file index.html in PATH_TO_ROOT_DIRECTORY/ROOT_DIRECTORY/PAGENAME/SUBPAGE/
    -Attachment are saved to the same directory as the page they belog to.
    -The etags.xml file is saved to PATH_TO_ROOT_DIRECTORY/ROOT_DIRECTORY/
    -The landing page (a page choosen as the main page, usually 'home') is saved 
     in a file index.html in PATH_TO_ROOT_DIRECTORY/ROOT_DIRECTORY/
     However, subpages and attachments of the landing page are saved 
     in PATH_TO_ROOT_DIRECTORY/ROOT_DIRECTORY/LANDING_PAGENAME/


4.3 XML DOCUMENT etags.xml

    etags.xml is an XML document that is stored in the root directory.
    The document contains information about the state of the site elements
    such as timestamp of the mirroring, list of attachments and list of pages,
    where each list item consist of ETag of attachment/page, ID of attachment/page
    and path to the attachment/page.



4.4 MIRRORING THE SITE AGAIN

    In case the site has been mirrored (to the same path) before (ie. there is
    a file etags.xml in path/root_directory/). Information about the last
    mirroring are loaded from etags.xml and the mirroring process will continue
    only if there has been some changes since the last mirroring and
    will download and save only new or modified attachments.




4.5 USAGE OF TEMPLATES


4.5.1 BASICS AND EXAMPLES

    Every template file contains mixture of html/css code and Cheetah code.
    For complete documetation of the Cheetah syntax see
    http://www.cheetahtemplate.org/docs/users_guide_html/users_guide.html

    The script uses five templates:
        file_cabinet_template.tmpl,
        announcements_page_template.tmpl,
        announcement_template.tmpl,
        listpage_template.tmpl and
        webpage_template.tmpl
    Each one for a different page type supported by Google Site, these page types 
    are respectively:
        filecabinet
        announcementspage
        announcement
        listpage
        webpage

    Although every page typy serves for different purpose, the usege of
    templates is almost the same for all of them (differences are described at
    the end of this paragraph).

    A template has two objects at its disposal, page and site.
    So let's begin with an example of a simple template.

    <html>
        <head>
            <title>$page.title</title>
        </head>
        <body>$page.content</body>
    </html>

    This template uses two atrtibutes of the page object, title is a page title
    and content is a content of html body.


    The basic attributes of page object are:
    PAGE
      -attachments
          list of attachments
      -author
          object that has two atributes, name and email
      -childs
          list of subpages
      -comments
          list of comments
      -content
          content of the html body tag of the page
      -parent
          parent page
      -revision
          a page revision number
      -updated
          date object containing the date of creation or last modification

    The basic attributes of attachment object are:
    ATTACHMENT
      -author
          object that has two atributes, name and email
      -name
          the attachment name
      -revision
          an attachment revision number
      -summary
          description of the attachment
      -updated
          date object containing the date of creation or last modification

    The basic attributes of comment object are:
    COMMENT
      -author
          object that has two atributes, name and email
      -revision
          a comment revision number
      -text
          text of the comment
      -updated
          object containing the date of creation or last modification




    An example illustrating how to handle comments in the template.
    <h3>Comments</h3>
        <table>
        #for $comment in $page.comments
            <tr><td>
                $comment.author.name, $comment.author.email, $comment.updated.format(), revision: $comment.revision
                <p>$comment.text</p>
            </td></tr>
        #end for
        </table>

    If you want this fragment to be shown only if the page has at least one
    comment, you can surround it with
    #if $page.comments THE CODE FRAGMENT ABOVE #end if





    About the updated object:
    UPDATED
      It has the important method - format, which has a string argument specifying
      the format of a datetime; the string argument consists of directives
      (see python time module at http://docs.python.org/library/time.html)
      and other additional letters. If no argument is specified, the default
      format ('%B %d, %Y, %I:%M %p') is used.
      EXAMPLES:
        The result of
          $page.updated.format()<br/>
          $page.updated.format('%B %d, %Y, %I:%M %p')<br/>
          $page.updated.format('%d. %m. %Y %H:%M:%S')<br/>
          $page.updated.format('%a, %d %b %Y %H:%M:%S')
        is
          February 24, 2010, 05:07 PM
          February 24, 2010, 05:07 PM
          24. 02. 2010 17:07:54
          Wed, 24 Feb 2010 17:07:54





   An example of creating navigation:
	NAVIGATION
	<table>
        #for $child in $site.childs
        <tr><td>
            <a href="$child.get_alternative_path_to($page)">$child.title</a>
        </td></tr>
	#end for
    </table>

   Here was used the other object - site, that has the list of childs (the top-level pages)
	For highlighting the landing page ('home' by default), one can use methods
   get_landing_page() and
	get_non_landing_pages()
	that can be used, for instance, for locating the landing page on the top of the navigation
	example
	NAVIGATION
	<table>
		<tr><td>
		<a style="background-color:yellow" href="$site.get_landing_page().get_alternative_path_to($page)">$site.get_landing_page().title</a>	
    	</td></tr>
		#for $child in $site.get_non_landing_pages()
			<tr><td>
			<a href="$child.get_alternative_path_to($page)">$child.title</a>	
    		</td></tr>
		#end for
	</table>

	


    An example of navigation "top-level_page > subpage > current_page"
    #for $predecessor in $page.get_predecessors()
        <a href="$predecessor.get_alternative_path_to($page)">$predecessor.title</a> >
    #end for
    $page.title




    An example of adding announcements to the announcemetpage:
    #for $announcement in $page.get_announcements()
        <h3><a href="$announcement.get_alternative_path_to($page)">$announcement.title</a></h3>
        <p>$announcement.embedded_content</p>
    #end for


	An example of creating a list of subpages
	<h3>Subpages</h3>
	#for $child in $page.childs
		<a href="$child.get_alternative_path_to($page)">$child.title</a><br/>
	#end for



    An example of adding a table with (web)attachments to the filecabinet:
    <table>
    #for $file in $page.attachments
        <tr>
        <td><a href="$file.name">$file.name</a></td>
        <td>$file.summary</td>
        <td>$file.author.name</td>
        <td><a href="mailto:$file.author.email">$file.author.email</a></td>
        <td>$file.updated.format()</td>
        <td>$file.revision</td>
        </tr>
    #end for
    #for $file in $page.web_attachments
        <tr>
        <td><a href="$file.web_src">$file.name</a></td>
        <td>$file.summary</td>
        <td>$file.author.name</td>
        <td><a href="mailto:$file.author.email">$file.author.email</a></td>
        <td>$file.updated.format()</td>
        <td>$file.revision</td>
    </tr>
    #end for
    </table>






    An example of adding list items to the listpage:
    <table><tr>
    #for $header in $page.list_items.headers
        <th>$header</th>
    #end for
    <th>autor</th><th>updated</th><th>revision</th></tr>
    #for $item in $page.list_items.items
        <tr>
        #for $cell in $item.cells
            <td>$cell</td>
        #end for
        <td>$item.author.name</td>
        <td>$item.updated.format()</td>
        <td>$item.revision</td>
        </tr>
    #end for
    </table>




4.5.2 HANDLING THE LAYOUTS

Google Sites supprots nine kinds of layout:
	One column (simple)
	Two column (simple)
	Three colum (simple)
	One column 
	Two column 
	Three colum 
	Left sidebar
	Right sidebar
	Left and right sidebars


Layout information are included in HTML code via classes. 
Each layout and every layout component (panel) has it's class name which can be set in CSS (in the template) to specify particular page sections.

Class names for all layouts and their components are described below:



One column (simple)

                             sites-layout-name-one-column
 -----------------------------------------------------------------------------------
|                                                                                   |
|                              sites-tile-name-content-1                            |
|                                                                                   |
 -----------------------------------------------------------------------------------


Two column (simple)

                             sites-layout-name-two-column
 -----------------------------------------------------------------------------------
|                                           |                                       |
|       sites-tile-name-content-1           |       sites-tile-name-content-2       |
|                                           |                                       |
 -----------------------------------------------------------------------------------



Three colum (simple)

                             sites-layout-name-three-column 
 -----------------------------------------------------------------------------------
|                           |                           |                           |
| sites-tile-name-content-1 | sites-tile-name-content-2 | sites-tile-name-content-3 |
|                           |                           |                           |
 -----------------------------------------------------------------------------------


One column 

                             sites-layout-name-one-column-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
|                                                                                   |
|                              sites-tile-name-content-1                            |
|                                                                                   |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------


Two column 

                             sites-layout-name-two-column-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
|                                           |                                       |
|       sites-tile-name-content-1           |       sites-tile-name-content-2       |
|                                           |                                       |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------



Three colum 

                             sites-layout-name-three-column-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
|                           |                           |                           |
| sites-tile-name-content-1 | sites-tile-name-content-2 | sites-tile-name-content-3 |
|                           |                           |                           |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------



Left sidebar

                            sites-layout-name-left-sidebar-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
|          sites-tile-name-content-1       |       sites-tile-name-content-2        |
|            sites-canvas-sidebar          |                                        |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------


    


Right sidebar

                            sites-layout-name-right-sidebar-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
|          sites-tile-name-content-1       |       sites-tile-name-content-2        |
|                                          |          sites-canvas-sidebar          |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------



Left and right sidebars


                            sites-layout-name-dual-sidebar-hf
 -----------------------------------------------------------------------------------
|                               sites-tile-name-header                              |
 -----------------------------------------------------------------------------------
| sites-tile-name-content-1 | sites-tile-name-content-2 | sites-tile-name-content-3 |
|    sites-canvas-sidebar   |                           |   sites-canvas-sidebar    |
 -----------------------------------------------------------------------------------
|                               sites-tile-name-footer                              |
 -----------------------------------------------------------------------------------

If you want to set a particular object in a particular layout, you have to specify the layout class, a panel class and the object tag as follows

.LAYOUT_NAME .PANEL_NAME OBJECT_TO_BE_SET {
//CSS code
}

Examples:
To set color of title (H2) of Three colum layout in the third column just add the following code into CSS

.sites-layout-name-three-column-hf .sites-tile-name-content-3 H2 {
	color: #0000ff;
}

To specify the header for all layout (which contain header panel) just omit layout class

.sites-tile-name-header {
// CSS code
}

More complex examle:

.sites-tile-name-footer {
	color: #ffffff;
  	background: #55554C 
  	border-top: solid 1px #72726E;
  	border-bottom: solid 3px #53534A;
}

.sites-layout-name-right-sidebar-hf {
	margin-top:10px;	
}

.sites-layout-name-right-sidebar-hf .sites-canvas-sidebar {    
	float: left;
   width: 210px;
	margin-left: 20px ;		
}

.sites-layout-name-right-sidebar-hf .sites-tile-name-content-1 {    				
   width: 430px;	 	
	margin-left: 15px ;
	margin-bottom: 5px;			
  }

.sites-layout-name-right-sidebar-hf h4 {    
	color: #00ff00;
	margin-bottom: 10px ;		
 }

.sites-layout-name-one-column-hf .sites-tile-name-content-1 {
	width: 640px;	 		
	margin-left:20px;
	margin-right:20px;
}







    For more details about the objects and their attributes see module objects
    and for more examples check out the default templates.





