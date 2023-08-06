from picplz.objects import PicplzUser, PicplzPlace, PicplzComment, Pic, PicplzCity
from picplz.errors import PicplzError
import urllib,urllib2,cgi,simplejson

class PicplzAPI():
    """ picplz API """
    
    authenticator = None
    api_base = 'https://api.picplz.com/api/v2'
    feed_endpoint = api_base + '/feed.json'
    pic_endpoint = api_base + '/pic.json'
    like_endpoint = api_base + '/pic/like.json'
    comment_endpoint = api_base + '/pic/comment.json'
    user_endpoint = api_base + '/user.json'
    follow_endpoint = api_base + '/user/follow.json'
    place_endpoint = api_base + '/place.json'
    city_endpoint = api_base + '/city.json'
    
    def init(self,authenticator=None):
        if authenticator is not None:
            self.authenticator = authenticator
            
    def __check_for_picplz_error__(self,json):
        error_text = 'Unknown picplz error'
        result = simplejson.loads(json)
        if result.has_key('result'):
            if result['result'] == "error":
                if result.has_key('text'): 
                    error_text = result['text']
                raise PicplzError('An error occurred: %s' % (error_text))
            
    def __make_unauthenticated_request__(self,endpoint,params_dict):
        
        params = urllib.urlencode(params_dict)
        full_uri = "%s?%s" % (endpoint,params)
        response = urllib2.urlopen(full_uri)
        response_text = response.read()
        self.__check_for_picplz_error__(response_text)
        return response_text
    
    def __make_authenticated_post__(self,endpoint,params_dict): 

        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        response = urllib2.urlopen(request)
        response_text = response.read()
        self.__check_for_picplz_error__(response_text)
        return response_text
        
    def __make_authenticated_put__(self,endpoint,params_dict):
        
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        response_text = response.read()
        self.__check_for_picplz_error__(response_text)
        return response_text
        
    def __make_authenticated_delete__(self,endpoint,params_dict): 

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        request.get_method = lambda: 'DELETE'
        response = opener.open(request)
        response_text = response.read()
        self.__check_for_picplz_error__(response_text)
        return response_text
        
    def get_feed(self,type,pic_formats=None,pic_page_size=None,last_pic_id=False):
        
        parameters = {'type':type}
        if pic_formats is not None:
            parameters['pic_formats']=pic_formats
        if last_pic_id:
            parameters['last_pic_id']=last_pic_id
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        return self.__make_unauthenticated_request__(self.feed_endpoint, parameters)
    
    def get_pics(self,ids=None,place=None,user=None,last_pic_id=False):
        
        if (id is None and place is None and user is None):
            raise PicplzError("get_pic method requires one of: a comma delimited list of pic ids, a PicplzPlace, or PicplzUser")
        
        if user is not None:
            return user.fetch_all_pics()
        
        pics = []
        
        return pics
        
    def get_pic(self,id=None,longurl_id=None,shorturl_id=None,include_comments=False):
        """" get individual pic, requires one of id, longurl_id, or shorturl_id"""
        
        if (id is None and longurl_id is None and shorturl_id is None):
            raise PicplzError("get_pic method requires one of a pic id, longurl_id or shorturl_id")
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if longurl_id is not None:
            parameters['longurl_id']=longurl_id
        if shorturl_id is not None:
            parameters['shorturl_id']=shorturl_id
        if include_comments is not None:
            parameters['include_comments']=1
        
        returned_json = self.__make_unauthenticated_request__(self.pic_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        pic_data = returned_data['value']['pics'][0]
        pic = Pic.from_dict(self,pic_data)

        return pic

    def like_pic(self):
        
        if self.authenticator is None:
            raise PicplzError("like_pic requires an authenticated API instance")
        
        return None
    
    def unlike_pic(self):
        
        if self.authenticator is None:
            raise PicplzError("unlike_pic requires an authenticated API instance")
        
        return None
    
    def comment(self):
        
        if self.authenticator is None:
            raise PicplzError("comment requires an authenticated API instance")
        
        return None
        
    def get_user(self, username=None,id=None,include_detail=False,include_pics=False,pic_page_size=None,last_pic_id=False):
        """ get user info, requires either username or the user's picplz id"""
        
        if (id is None and username is None):
            raise PicplzError("get_pic method requires one of a pic id, longurl_id or shorturl_id")
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if username is not None:
            parameters['username']=username
        if include_detail:
            parameters['include_detail']=1
        if include_pics:
            parameters['include_pics']=1
        if last_pic_id:
            parameters['last_pic_id']=last_pic_id
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        returned_json = self.__make_unauthenticated_request__(self.user_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        data = returned_data['value']['users'][0]
        user = PicplzUser.from_dict(self, data)
        try:
            has_more_pics = returned_data['value']['users'][0]['more_pics']
            if has_more_pics:
                user.__has_more_pics__ = True
            else:
                user.__has_more_pics__ = False
        except:
            user.__has_more_pics__ = False
        try:
            last_pic_id = returned_data['value']['users'][0]['last_pic_id']
            user.__last_pic_id__ = last_pic_id
        except:
            user.__last_pic_id__ = False
        
        return user
        
    def is_authenticated_user_following(self, username=None,id=None):
        """ query whether or not the currently authenticated user is following another user
        requires either username or id of the followee user"""
        if self.authenticator is None:
            raise PicplzError("is_authenticated_user_following requires an authenticated API instance")
        
        return None
        
    def follow_user(self,username=None,id=None):
        
        if self.authenticator is None:
            raise PicplzError("follow_user requires an authenticated API instance")
        
        return None
        
    def unfollow_user(self,username=None,id=None):

        if self.authenticator is None:
            raise PicplzError("unfollow_user requires an authenticated API instance")
        
        return None
        
    def get_place(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        place = PicplzPlace()
        
        return place
    
    def get_city(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        place = PicplzCity()
        
        return place
        