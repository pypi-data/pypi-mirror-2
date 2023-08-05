class DeliciousLinks:
    def __init__(self, list = []):
        self.links = list
        
    def append(self, link):
        self.links.append(link)
        
    def filter_by_tag(self, tag):
        return DeliciousLinks([link for link in self.links if tag in link.tags])

    def filter_by_start_date(self, start_date):
        return DeliciousLinks([link for link in self.links if link.datetime > start_date])

    def filter_by_end_date(self, end_date):
        return DeliciousLinks([link for link in self.links if link.datetime < end_date])
        
    def group_by_tag(self):
        result = {}
        for link in self.links:
            for tag in link.tags:
                if not tag in result: result[tag] = []
                result[tag].append(link)
        return result
        
    def show(self):
        for link in self.links:
            print link.show().encode("UTF-8")

class DeliciousQuery:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_links(self, tags, start_date=None, end_date=None):
    
        md = mdelicious.MDelicious(self.username, self.password)
        links = md.posts_all(tag=tags, start_date=start_date, end_date=end_date)
        result = DeliciousLinks()
   
        for link in links:
            result.append(DeliciousLink.DeliciousLink(link["href"], link["tags"], link["description"], link["extended"], link["time"]))
        return result
    
    def show(self):
        print "U: %s" % (self.username)
    