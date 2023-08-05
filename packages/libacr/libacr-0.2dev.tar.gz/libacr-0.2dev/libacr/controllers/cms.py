# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect, tmpl_context, TGController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons.controllers.util import abort

from repoze.what import predicates

from comments import CommentsController
from rdisk import RDiskController
from libacr.plugins.controller import PluginsController

from admin.dashboard import AdminController

from libacr import model
from libacr.model.core import DBSession
from libacr.model.content import Page, Slice, Content, View, ContentData
from libacr.lib import url, get_page_from_urllist, current_user_id, language, user_can_modify
from libacr.rss import rss_for_slicegroup

from datetime import datetime

from turbomail import Message
from turbomail.control import interface

__all__ = ['AcrRootController']

class AcrRootController(TGController):
    comments = CommentsController()
    admin = AdminController()
    plugins = PluginsController()

    @expose('libacr.templates.page')
    def default(self, *args, **kwargs):
        if not args:
            args = ['index']

        page = get_page_from_urllist(args)
        if not page:
            abort(404, "Page not found")

        return dict(page=page)

    @expose('libacr.templates.page')
    def page(self, pageid, *args, **kwargs):
        try:
            page = DBSession.query(Page).filter_by(uid=pageid).one()
        except:
            redirect('/')
        return dict(page=page)

    @expose('libacr.templates.slice')
    def slice(self, sliceid):
        try:
            slice = DBSession.query(Slice).filter_by(uid=sliceid).one()
        except:
            abort(404, "Slice not found")

        page = DBSession.query(Page).filter_by(uri='default').one()
        return dict(page=page, slice=slice)
        
    @expose(content_type="application/rss+xml")
    def rss(self, sliceid):
        from libacr.views.slice_group import SliceGroupRenderer
        try:
            slice = DBSession.query(Slice).filter_by(uid=sliceid).one()
            u = slice.page.url
        except:
            abort(404, "Slice not found")
            
        if slice.view != 'slicegroup':
            abort(403, "Invalid slice type")

        return rss_for_slicegroup(slice)
        
    @expose('libacr.templates.search')
    def search(self, searchid, what):
        search_slice = DBSession.query(Slice).filter_by(uid=searchid).first()
        if not search_slice:
            abort(404, "Invalid Search")

        from libacr.views.search import SearchRenderer
        results = SearchRenderer.perform(search_slice, what)

        return dict(page=search_slice.page, what=what, results=results)

    @expose()
    @require(predicates.in_group("acr"))
    def del_slice(self, sliceid):
        try:
            slice = DBSession.query(Slice).filter_by(uid=sliceid).one()
        except:
            abort(404, "Slice not found")

        if not user_can_modify(slice.page):
           flash('You do not have permissions to edit page', 'error')
           return redirect(request.headers['Referer'])
        else:
           DBSession.delete(slice)

        return 'OK'

    @expose()
    @require(predicates.in_group("acr"))
    def move_slice(self, sliceid, value):
        try:
            slice = DBSession.query(Slice).filter_by(uid=sliceid).one()
            slice.slice_order += int(value)
        except Exception, e:
            abort(404, "Slice not found")
        return ''

    @expose()
    def sendForm_to_email(self, **kw):
        missing_value = ''
        email_address = kw['email_address']
        subject = kw['subject']

        content = '<html><body>'
        content += '<table>'

        for item in kw:
            if item != 'email_address' and item != 'subject':
               value = kw[item]
               obligatory = item.startswith('*')
               if obligatory:
                  if value == '':
                     missing_value = missing_value + item + ',  '

               copy = item.lstrip('*')

               content += '<tr>'
               content += '<td> %s </td>' % (copy)
               content += '<td> = </td>'
               content += '<td> %s </td>' % (value)
               content += '</tr>'
        content += '</table>'
        content += '</html></body>'

        if missing_value != '':
           flash('Please specify the following fields: ' + missing_value)
           return redirect(request.headers['Referer'])

        msg = Message(author="admin@acr.it",
                      to=email_address,
                      subject=subject,
                      plain="email"
                      )
        msg.rich = """%s""" % (content)
        msg.send()

        flash('Message sent')
        return redirect(request.headers['Referer'])
