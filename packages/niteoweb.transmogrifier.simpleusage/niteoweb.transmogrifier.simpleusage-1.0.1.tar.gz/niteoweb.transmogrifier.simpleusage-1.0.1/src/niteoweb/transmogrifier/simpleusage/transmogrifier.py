from collective.transmogrifier.interfaces import ISectionBlueprint, ISection
from zope.interface import classProvides, implements
from collective.transmogrifier.utils import defaultMatcher


class FormatSetter(object):

    implements(ISection)
    classProvides(ISectionBlueprint)

    def __init__(self, transmogrifier, name, options, previous):
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

        # options
        self.format = options.get('format', 'text/html')

    def __iter__(self):

        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey: # not enough info
                yield item; continue
            path = item[pathkey]
        
            ob = self.context.unrestrictedTraverse(path.lstrip('/'), None)
            if ob is None:
                yield item; continue # object not found

            ob.setFormat(self.format)
            ob.setContentType(self.format)

            yield item


class PathSetter(object):

    implements(ISection)
    classProvides(ISectionBlueprint)

    def __init__(self, transmogrifier, name, options, previous):
        self.options = options
        self.previous = previous
        
        # options
        self.container = options.get('container', 'news')
        
    def __iter__(self):

        for item in self.previous:
            item['_path'] = self.container + '/' + item['id']
            yield item


class NewsItemSource(object):
    
    implements(ISection)
    classProvides(ISectionBlueprint)

    def __init__(self, transmogrifier, name, options, previous):
        self.options = options
        self.previous = previous
        
        # options
        self.type = options.get('type', 'News Item')
        self.author = options.get('author', 'admin')

    def __iter__(self):
                
        for record in self.source():

            item = dict()
            
            # set general settings
            item['_type'] = self.type
            item['creators'] = (self.author,)           
            
            # set dates
            item['creation_date'] = record['date']
            item['effectiveDate'] = record['date']
            
            # set content fields
            item['title'] = record['title']
            item['text'] = record['text']
            item['subject'] = (record['category'],)
            
            # publish news item
            item['_transitions'] = ('publish',)
            
            yield item
            
        for item in self.previous:
            yield item


    def source(self):
        """A method that parses raw data and returns results.
        You can parse data from HTML document, CSV, JSON, etc. 
        Your options are virtually limitless.
        
        Check out real-world examples can be found in /branches of this product's repository.
        """
        
        for count in range(1, 6):
            result = dict(
                           title = 'news item %i' %count,
                           category = 'category %i' %count,
                           date = '2010/01/0%i' %count,
                           text = 'bolded number: <b>%i</b>' %count,
                          )
            yield result   

 
