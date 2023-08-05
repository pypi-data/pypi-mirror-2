from datetime import datetime
from tg import expose, flash, require, request, redirect, tmpl_context, TGController
from libacr.plugins.base import AdminEntry, AcrPlugin, plugin_expose
from libacr.controllers.admin.base import _create_node, BaseAdminController
from libacr.model.core import DBSession
from libacr.model.content import Tag, Page, Slice, Content, ContentData
from libacr.lib import url, current_user_id, language, icons, user_can_modify
from repoze.what import predicates
from tw.api import WidgetsList
import tw.forms as twf

class GalleryController(BaseAdminController):
    @plugin_expose('create')
    @require(predicates.in_group("acr"))
    def create(self):
        class CreateGalleryForm(WidgetsList):
            page = twf.SingleSelectField(label_text="Page:", options=[(p.uid, p.title) for p in DBSession.query(Page)])
            tag = twf.SingleSelectField(label_text="Members Tag:", options=[(t.uid, t.name) for t in DBSession.query(Tag)])
        gallery_form = twf.TableForm(fields=CreateGalleryForm(), submit_text="Create")
            
        return dict(form=gallery_form)

    @expose()
    @require(predicates.in_group("acr"))
    def save(self, page, tag):
        tag = DBSession.query(Tag).filter_by(uid=tag).first()
        slicegroup_id = 'gallery_%s-%s' % (tag.name, datetime.now().strftime('%y%m%d%H%M%S'))

        node_args = {}
        node_args['page'] = page
        node_args['name'] = slicegroup_id
        node_args['zone'] = 'main'
        node_args['order'] = 0
        node_args['tags'] = []
        node_args['view'] = 'slicegroup'
        node_args['data'] = """[group]
filter_tag=%s
preview=1""" % tag.name
        _create_node(**node_args)

        node_args['name'] += '_script'
        node_args['view'] = 'genshi'
        node_args['data'] = """

<script>
jQuery(document).ready(function() {
    jQuery('.%s .acr_group_%s_entries a').each(function(){

          jQuery(this).attr('href',jQuery(this).attr('name'));
    });
    jQuery('.%s .acr_group_%s_entries a').lightBox({imageLoading:'%s',
                                            imageBtnPrev:'%s',
                                            imageBtnNext:'%s',
                                            imageBtnClose:'%s',
                                            imageBlank:'%s'});
});
</script>""" % (slicegroup_id, tag.name, slicegroup_id, tag.name, icons['loading'].link,
                icons['prev'].link, icons['next'].link,
                icons['close'].link, icons['blank'].link)
        _create_node(**node_args)
        flash('Gallery successfully created')
        return redirect(url('/admin'))

class PhotoGallery(AcrPlugin):
    uri = 'gallery'

    def __init__(self):
        self.admin_entries = [AdminEntry(self, 'Create Gallery', 'create', section="Templates")]
        self.controller = GalleryController()
