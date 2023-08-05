from tg import expose, flash, require, url, request, redirect, tmpl_context, validate, config, TGController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons.controllers.util import abort
from repoze.what import predicates

from libacr.lib import rdisk_url as url
from libacr.lib import admin_css
from libacr import acr_zones
from libacr.forms import order_values
from libacr.model.core import DBSession
from libacr.model.content import Content, Tag, Slice
from libacr.controllers.admin.base import _create_node

from libacr.views.video import VideoRenderer

from datetime import datetime

from tw.api import WidgetsList
import tw.forms as widgets
from tw.tinymce import TinyMCE, MarkupConverter
from formencode import validators
import os, re, shutil, errno

import mimetypes
from libacr.mediaWorker import convert_video
import tempfile 
from libacr.model.content import  Page

rdisk_root = config.get('public_dir') + os.sep + 'rdisk'

def from_url_to_path(p):
    return cleanup_path(rdisk_root+os.sep+p)

def cleanup_path(p):
    r = re.compile('/+')
    return r.sub('/', os.path.normpath(p))

def from_path_to_url(p):
    return cleanup_path(p[len(rdisk_root):])

def get_root_tree(): 
    path_dirs = []
    base_path = rdisk_root

    path_dirs.append(('/', '/'))
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            cur_p = from_path_to_url(root+os.sep+d)[1:]
            path_dirs.append( (cur_p, cur_p) )
    path_dirs.sort()
    
    return path_dirs

def get_parent_of_url(p):
    p = cleanup_path(p)
    p = '/'.join(p.split('/')[:-1])
    if not p:
        p = '/'
    return p

def split_path_in_walk(path):
    """Splits a string path to a list of directories"""
    directories = []
    split = os.path.split(path)
    while split[0] and split[0] != os.sep:
        path = split[0]
        directories.append(split[1])
        split = os.path.split(path)

    if (split[1]):
        directories.append(split[1])

    directories.reverse()
    return directories

def make_directories(dir_list):
    """Create all the directories in a list as a path"""
    path = ''
    for d in dir_list:
        path = path + os.sep + d
        try:
            os.mkdir(path)
        except OSError, err:
            if err.errno != errno.EEXIST:
                raise
            
class UploadForm(WidgetsList):
    document = widgets.FileField(label_text="File:", validator=validators.FieldStorageUploadConverter(not_empty=True))
    page = widgets.SingleSelectField(label_text="Page:", options=lambda : [(None, '----------')] + \
                                                                          [(p.uid, p.title) for p in DBSession.query(Page)])
    path = widgets.SingleSelectField(label_text="Path:", options=get_root_tree, validator=validators.NotEmpty(), attrs={'style':'width:400px'})
    title = widgets.TextField(label_text="Title:", attrs={'style':'width:400px'})
    tags = widgets.MultipleSelectField(label_text='Tags:', options=lambda : (p.name for p in DBSession.query(Tag)), attrs={'style':'width:400px'})
    desc = widgets.TextArea(label_text="Description:", attrs={'style':'width:400px'})
    choose_type = widgets.SingleSelectField(label_text="Type:", options=['Image','Video','File'], attrs={'style':'width:400px'})
upload_form = widgets.TableForm(fields=UploadForm(), submit_text="Upload" )

class MkdirForm(WidgetsList):
    path = widgets.HiddenField()
    subdir = widgets.TextField(label_text="Directory Name:", validator=validators.NotEmpty(), attrs={'style':'width:400px'})
mkdir_form = widgets.TableForm(fields=MkdirForm(), submit_text='Create')

class RDiskController(TGController):
    @expose('libacr.templates.rdisk.index')
    @require(predicates.in_group("acr"))
    def default(self, *args, **kwargs):
        admin_css.inject()
        
        node = '/' + '/'.join(args)
        parent = '/' + '/'.join(args[:-1])
        node_path = rdisk_root + node

        if not os.path.exists(node_path):
            abort(404, "Path not found")
        
        entries = []
        for entry in os.listdir(node_path):
            entry_path = node_path + os.sep + entry
            entries.append( {'node':node, 'entry':entry, 'path':from_path_to_url(entry_path), 'type':os.path.isdir(entry_path) and 'D' or 'F'} )
    
        return dict(entries=entries, node=node, parent=parent,
                     section_title="Remote Disk")

    @expose('libacr.templates.rdisk.form')
    @require(predicates.in_group("acr"))
    def upload(self, **kw):
        admin_css.inject()
        return dict(title='File Upload', form=upload_form, values=kw,
                     section_title="Upload a file",action=url("/add_res"))

    @expose()
    @validate(upload_form, error_handler=upload)
    @require(predicates.in_group("acr"))
    def add_res(self, document, path, title, desc, choose_type, page, tags=[]):
        def copy_file_to_dest(doc, dest):
            data = doc.file.read()
            f = open(dest, 'w')
            f.write(data)
            f.close()
        
        rel_path = os.sep + path + os.sep
        full_path = from_url_to_path(rel_path)
        web_file_path = url(cleanup_path(rel_path + os.sep + document.filename))

        cur_entry = cleanup_path(rel_path + os.sep + document.filename)
        title = title and title or document.filename
        desc = desc and desc or ''
       
        if choose_type=='File':
            entry_data = "%s\n%s\n%s" % (web_file_path, title, desc)
            try:
                cur_entry = DBSession.query(Slice).filter_by(name=cur_entry).one()
                cur_entry.content.all_data[0].value = entry_data
            except:
                _create_node(name=cur_entry, zone='main', order=0, tags=tags, view='file',
                             data=entry_data, page=page, skip_permission=True)
        else:
            if choose_type=='Image':
                entry_data = """
[image]
path = %(path)s
title = %(title)s
size=auto
show_title=None
description=%(desc)s
""" % dict(path=web_file_path, title=title, desc=desc)
                view = 'image'
            elif choose_type=='Video':
                name = os.path.splitext(document.filename)[0]
                convert_video(name, document.file)
                VideoRenderer.thumbnail(document.filename, document.file)

                entry_data = """
[video]
path = %(path)s
title = %(title)s
size=auto
show_title=None
description=%(desc)s
""" % dict(path=web_file_path, title=title, desc=desc)
                view ='video'


            try:
                cur_entry = DBSession.query(Slice).filter_by(name=cur_entry).one()
                cur_entry.content.all_data[0].value = entry_data
            except:
                _create_node(name=cur_entry, zone='main', order=0, tags=tags, view=view,
                             data=entry_data, page=page, skip_permission=True)
        
        disk_file_path = cleanup_path(full_path + os.sep + document.filename)

        directories = split_path_in_walk(full_path)
        make_directories(directories)
        
        copy_file_to_dest(document, disk_file_path)
        
        flash('Resource successfully loaded')
        return redirect(url(rel_path))
    
    @expose('libacr.templates.rdisk.form')
    @require(predicates.in_group("acr"))
    def mkdir(self, where, **kw):
        admin_css.inject()
        values={}
        values['path'] = where
        return dict(title="Make Directory", form=mkdir_form, values=values,
                     section_title="Create a directory",action=url('/do_mkdir'))
    
    @expose()
    @validate(mkdir_form, error_handler=mkdir)
    @require(predicates.in_group("acr"))
    def do_mkdir(self, path, subdir):
        path = cleanup_path(os.sep + path)
        rel_path = path + os.sep + subdir
        full_path = from_url_to_path(rel_path)
        
        directories = split_path_in_walk(full_path)
        try:
            make_directories(directories)
            flash('Path successfully created')
        except Exception, e:
            flash('Failed to create path: %s' % str(e), 'warning')        
        
        return redirect(url('/'+path))

    @expose()
    @require(predicates.in_group("managers"))
    def del_res(self, what):
        
        def erase_meta(p):
            cur_entry = p
            try:
                cur_entry = DBSession.query(Slice).filter_by(name=cur_entry).one()
                DBSession.delete(cur_entry)
            except:
                flash('Failed to delete content entry')
            
        def rm_file(p):
            if os.path.isdir(p):
                for root, dirs, files in os.walk(p, topdown=False):
                    for name in files:
                        f = os.path.join(root, name)
                        meta_f = from_path_to_url(f)                   
                        erase_meta(meta_f)
                        os.remove(f)
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(p)
            else:
                os.remove(p)
                erase_meta(from_path_to_url(p))
                       
        full_path = from_url_to_path(what)
        rm_file(full_path)
        
        return redirect(url('/'+get_parent_of_url(what)))
