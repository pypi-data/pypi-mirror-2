from . import mdelicious
from . import DeliciousLinks
from . import DeliciousLink

class DeliciousQuery:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_links(self, tags, start_date=None, end_date=None):
    
        md = mdelicious.MDelicious(self.username, self.password)
        links = md.posts_all(tag=tags, start_date=start_date, end_date=end_date)
        result = DeliciousLinks.DeliciousLinks()
   
        for link in links:
            result.append(DeliciousLink.DeliciousLink(link["href"], link["tags"], link["description"], link["extended"], link["time"]))
        return result
    
    def show(self):
        print "U: %s" % (self.username)