import urllib

from types import *
from urlparse import urlparse
from pyquery import PyQuery as pq

SERVICE_DEFAULT = 'web'
SERVICE_INSTAGRAM = 'instagram'
SERVICE_IMGUR = 'imgur'
SERVICE_FLICKR = 'flickr'
SERVICE_PATH = 'path'
SERVICE_SKITCH = 'skitch'
SERVICE_MINUS = 'minus'
SERVICE_CLOUD = 'cloud'
SERVICE_500PX = '500px'

def set_natural_num(val):
    """
    if a negative number is passed in, force it to be positive. 
    e.g. -300 will return as 300
    """
    if val >= 0 and type(val) is IntType:
        return val
    else:
        val = val * -1
        return val

class WebImagery():
    
    def __init__(self):
        self.width = 200
        self.height = 200
        self.service = ''
        self.url = ''
    
    def set_image(self, url):
        """
        detect whether a url contains an image in our list of supported services
        """
        url = self.url = urlparse(url)

        if 'http' in url.scheme and self.__set_service():
            return True
        else:
            return False
    
    def get_image(self):
        """
        if this is a direct image link, just send that back
        if not, we need to scrape the image service site for the proper element that contains the direct image link
        """
        
        try:
            url = self.url
            url_path = url.scheme + "://" + url.netloc + url.path
            if self.service == SERVICE_DEFAULT:
                return url_path
            else:
                page = pq(url=url_path)

                if self.service == SERVICE_INSTAGRAM:
                    return page('img.photo').attr('src')
                elif self.service == SERVICE_IMGUR:
                    return page('#content .image img').attr('src')
                elif self.service == SERVICE_FLICKR:
                    return page('#photo .photo-div img').attr('src')
                elif self.service == SERVICE_PATH:
                    return page('.photo-background img.photo').attr('src')
                elif self.service == SERVICE_SKITCH:
                    return page('.myskitch-image .skitch-image-container img').attr('src')
                elif self.service == SERVICE_MINUS:
                    return page('link[rel="image_src"]').attr('href')
                elif self.service == SERVICE_CLOUD:
                    return page('#content img').attr('src')
                elif self.service == SERVICE_500PX:
                    return page('#mainphoto').attr('src')
                else:
                    return ""
        except:
            print "Image url is invalid"
    
    def get_image_as_html(self, alt=''):
        """
        if this is a direct image link, just send that back in html format
        if not, we need to scrape the image service site for the proper element that contains the direct image link in html format
        """

        try:
            url = self.url
            url_path = url.scheme + "://" + url.netloc + url.path
        
            self.width = set_natural_num(self.width)
            self.height = set_natural_num(self.height)
        
            if self.service == SERVICE_DEFAULT:
                return '<img src="'+url_path+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
            else:
                page = pq(url=url_path)

                if self.service == SERVICE_INSTAGRAM:
                    return '<img src="'+page('img.photo').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_IMGUR:
                    return '<img src="'+page('#content .image img').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_FLICKR:
                    return '<img src="'+page('#photo .photo-div img').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_PATH:
                    return '<img src="'+page('.photo-background img.photo').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_SKITCH:
                    return '<img src="'+page('.myskitch-image .skitch-image-container img').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_MINUS:
                    return '<img src="'+page('link[rel="image_src"]').attr('href')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_CLOUD:
                    return '<img src="'+page('#content img').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                elif self.service == SERVICE_500PX:
                    return '<img src="'+page('#mainphoto').attr('src')+'" alt="'+alt+'" width="'+str(self.width)+'" height="'+str(self.height)+'" />'
                else:
                    return ""
        except:
            print page
    
    def __set_service(self):
        """"
        if the url matches a service, set it
        """
        url = self.url

        if url.path.lower().endswith('jpg') or \
            url.path.lower().endswith('jpeg') or \
            url.path.lower().endswith('gif') or \
            url.path.lower().endswith('png'):
            
            self.service = SERVICE_DEFAULT
            return True
        elif 'instagr' in url.netloc:
            self.service = SERVICE_INSTAGRAM
            return True
        elif 'imgur' in url.netloc:
            self.service = SERVICE_IMGUR
            return True
        elif 'flickr' in url.netloc:
            self.service = SERVICE_FLICKR
            return True
        elif 'path' in url.netloc:
            self.service = SERVICE_PATH
            return True
        elif 'skitch' in url.netloc:
            self.service = SERVICE_SKITCH
            return True
        elif 'minus' in url.netloc or 'min.us' in url.netloc:
            self.service = SERVICE_MINUS
            return True
        elif 'cl.ly' in url.netloc:
            self.service = SERVICE_CLOUD
            return True 
        elif '500px' in url.netloc:
            self.service == SERVICE_500PX
            return True
        else:
            return False