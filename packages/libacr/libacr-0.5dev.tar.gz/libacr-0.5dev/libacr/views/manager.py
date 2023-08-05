from core import *
from feeds import *
from menu import *
from slice_group import *
from comments import *
from file_entry import *
from gmap import *
from form import *
from image import *
from video import *
from search import *

from libacr.model.core import DBSession
from libacr.model.content import View

class ViewsManager(object):
    def __init__(self):  
        self.views = [HTMLRenderer(), GenshiRenderer(), MenuRenderer(), 
                      LinkRenderer(), AjaxRenderer(), FeedRenderer(),
                      SliceGroupRenderer(), CommentsRenderer(), 
                      TwitterRenderer(), FileRenderer(), MapRenderer(),
                      FormRenderer(), ImageRenderer(), SearchRenderer(),
                      VideoRenderer()]

        self.forms = {}

    def __call__(self):
        return self

    def view_names(self):
        views = [v.name for v in self.views]
        views.extend((v[0] for v in DBSession.query(View.name)))
        return views

    def find_view(self, name):
        view = filter(lambda view : view.name == name, self.views)
        if not view:
            try:
                view = DBSession.query(View).filter_by(name=name).one()
                view = views.CodeRendererTemplate(view.name, view.code)
                self.views.append(view)
            except:
                return None
        else:
            view = view[0]
        return view

    def register_view(self, view):
        try:
            view_name = view.name
            view_type = view.type
        except:
            raise NameError, 'Your view is missing View.name or View.type attributes'
           
        if not self.find_view(view_name):
            self.views.append(view)
            exists = False
        
        if exists:
            raise NameError, 'A view with that name is already registered'

    def create_form(self, view, baseform):
        if not self.forms.has_key(view):
            self.forms[view] = {}

        if not self.forms[view].has_key(baseform):
            fields = baseform()
            fields.append(twf.HiddenField('view', default=view))
            fields.extend(ViewsManager.find_view(view).form_fields)
            self.forms[view][baseform] = twf.TableForm(fields=fields, submit_text="Save")

        return self.forms[view][baseform]

    def validator(self, baseform):
        class AutoDetectedViewForm(object):
            def __init__(self, baseform):
                self.baseform = baseform
                
            def validate(self, params, state):
                form = ViewsManager.create_form(params['view'], self.baseform)
                return form.validate(params, state)
        return AutoDetectedViewForm(baseform)

    def encode(self, view, dic):
        return ViewsManager.find_view(view).from_dict(dic)

    def decode(self, view, data):
        d = ViewsManager.find_view(view).to_dict(data)
        d['view'] = view
        return d
ViewsManager = ViewsManager()
