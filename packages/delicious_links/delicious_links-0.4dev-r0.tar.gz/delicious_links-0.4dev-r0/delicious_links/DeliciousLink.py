
class DeliciousLink:
    def __init__(self, url, tags, title, description, datetime):
        self.url = url
        self.tags = tags  
        self.title = title
        self.description = description
        self.datetime = datetime
        
    def show(self):
        return "[URL: %s, Tags: %s, Title: %s, Description: %s, Datetime: %s]" % (
            self.url, self.tags, self.title, self.description, self.datetime
        ) 