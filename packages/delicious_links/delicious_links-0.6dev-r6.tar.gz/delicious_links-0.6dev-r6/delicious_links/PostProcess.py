from DailyLinks import DailyLinks

class PostProcess:
    def __init__(self, delicious_login, wordpress_sender, templates):
        self.delicious_login = delicious_login
        self.wordpress_sender = wordpress_sender
        self.templates = templates
        self.dl = DailyLinks()
    
    def page_update(self, tag, tag_titles, page_id):
        html = self.dl.get_result(self.delicious_login, tag, tag_titles, self.templates)
        self.wordpress_sender.send(page_id, html)
        
    def new_post(self, tag, tag_titles, category_name, title):
        ws = self.wordpress_sender
        last_post = ws.get_last_post_in_category(category_name)
        if not last_post:
            print 'Last post not found'
        else:
            category = ws.get_category_from_name(category_name)
            html = self.dl.get_result(self.delicious_login, tag, tag_titles, self.templates, start_date=last_post.date_gmt)
            if html:
                print "Sending post"
                ws.new_post(title, html, [category.id])
            else:
                print "Nothing to post"
                