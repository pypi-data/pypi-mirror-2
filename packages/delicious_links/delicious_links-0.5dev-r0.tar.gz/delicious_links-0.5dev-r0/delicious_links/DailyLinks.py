import datetime
import cgi
import json
from DeliciousQuery import DeliciousQuery 

class DailyLinks:
    
    def process(self, delicious_login, filter_tag, tag_titles, start_date=None, end_date=None):
        dq = DeliciousQuery(delicious_login.username, delicious_login.password)
        links = dq.get_links(filter_tag, start_date=start_date, end_date=end_date)
        filtered_links = links.filter_by_tag(filter_tag)
        if(start_date): filtered_links = filtered_links.filter_by_start_date(start_date)
        if(end_date): filtered_links = filtered_links.filter_by_end_date(end_date)
        grouped_links = filtered_links.group_by_tag()
        
        if(grouped_links.has_key(filter_tag)):
            del grouped_links[filter_tag]
        
        output_links = {}

        for tag in grouped_links.keys():
            if(tag in (tag_titles).keys()):
                output_links[tag_titles[tag]] = (tag_titles[tag], grouped_links[tag])
        
        titles = output_links.keys()
        titles.sort()
        sorted_links = []
        for title in titles: sorted_links.append(output_links[title])

        return sorted_links
    
    def get_result(self, delicious_login, filter_tag, tag_titles, templates, start_date=None, end_date=None):
        links = self.process(delicious_login, filter_tag, tag_titles, start_date=start_date, end_date=end_date)
        if(links == []):
            return None
        else:
            return self.format_html(links, templates)
    
    def format_html(self, output_links, templates):

        #head
        result = templates["head"] % { "published_date": datetime.datetime.utcnow() }

        # tag
        for link in output_links:

            result += (templates["tag"] % { 
                "title": link[0] 
            }).encode("UTF-8")

            # item
            for link in sorted(link[1], key=lambda link: link.title):
                result += (templates["item"] % { 
                    "title": cgi.escape(link.title),
                    "url": cgi.escape(link.url),
                    "description": cgi.escape(link.description),
                    "tags": cgi.escape(json.dumps(link.tags)),
                    "datetime": cgi.escape(link.datetime.strftime("%Y-%m-%d") )
                }).encode("UTF-8")

            result += (templates["tag_end"])
        return result
