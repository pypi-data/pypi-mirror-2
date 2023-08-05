from . import wordpresslib

class WordpressSender:
    def __init__(self, xmlrpcurl, username, password):
        self.xmlrpcurl = xmlrpcurl
        self.username = username
        self.password = password

    def send(self, id, description):
        wp = wordpresslib.WordPressClient(self.xmlrpcurl, self.username, self.password)
        post = wp.getPost(id)
        post.description = description
        wp.editPost(id, post, True)

    def new_post(self, title, description, categories):
        wp = wordpresslib.WordPressClient(self.xmlrpcurl, self.username, self.password)
        post = wordpresslib.WordPressPost()
        post.title = title
        post.description = description
        post.categories = categories
        return wp.newPost(post, True)
        
    def get_last_post_in_category(self, category_name):
        wp = wordpresslib.WordPressClient(self.xmlrpcurl, self.username, self.password)
        last_post = None
        for post in wp.getRecentPosts(20):
            if(category_name in post.categories):
                return post
        return None
        
    def get_category_list(self):
        wp = wordpresslib.WordPressClient(self.xmlrpcurl, self.username, self.password)
        return wp.getCategoryList()
    
    def get_category_from_name(self, name):
        for category in self.get_category_list():
            if category.name == name:
                return category
        return None