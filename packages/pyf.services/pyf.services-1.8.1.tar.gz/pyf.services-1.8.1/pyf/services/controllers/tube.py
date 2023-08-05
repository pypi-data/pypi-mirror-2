# -*- coding: utf-8 -*-
"""Crud Tube Controllers"""

from tg import expose, flash, require, request, redirect, validate
from formencode import validators
from pylons import tmpl_context

from pyf.services.model import DBSession
from pyf.services import model
from pyf.services.model import Tube
from pylons.controllers.util import abort

from sprox.tablebase import TableBase
from sprox.formbase import AddRecordForm, EditableForm
from sprox.fillerbase import EditFormFiller

from pyf.services.controllers.crud import (SecureCrudRestController, DataGrid,
                                     render_boolean, render_link_field,
                                     has_model_permission)
from pyf.services.controllers.crud import FancyTableFiller as TableFiller
from pyf.services.controllers.tubelayer import (tubelayer_table,
                                                tubelayer_table_filler)

from pyf.services.core.events import create_event_track, get_logger
from pyf.services.core.router import Router
from pyf.services.core.tasks import launch_tube
from pyf.services.versionning.base import get_repository
from pyf.services.versionning.check import check_tube

from pyf.transport import decode_packet_flow

from repoze.what.predicates import NotAuthorizedError

from operator import itemgetter
from pyf.services.controllers.widgets import TubeLauncher

from tgscheduler.scheduler import add_single_task

import simplejson

import transaction
import time

import tw.forms

from pyf.componentized import ET

class TubeController(SecureCrudRestController):
    model = Tube
    __post_to_versionning__ = True
    __order_by__ = 'name'
    __desc__ = False

    class new_form_type(AddRecordForm):
        __model__ = Tube
        __omit_fields__ = ['dispatchs', 'layers']
        __require_fields__ = ['name', 'display_name', 'payload_ini']
        
        payload = tw.forms.TextArea('payload',
                                    default="""<?xml version="1.0" encoding="UTF-8"?>
<config>
  <process name="main">
    <!-- this is if you need a source
    (if you don't, change the pluginname or do a from="code" and add a <code> inside): -->
    <node type="producer" pluginname="descriptorsource" name="source">
      <children>
        <node type="">
        </node>
      </children>
    </node>
  </process>
  <!-- Uncomment if you need a post process: -->
  <!--<postprocess>
  </postprocess>-->
</config>""")

    class edit_form_type(EditableForm):
        __model__ = Tube

    class edit_filler_type(EditFormFiller):
        __model__ = Tube

    class table_type(TableBase):
        __base_widget_type__ = DataGrid
        __model__ = Tube
        __omit_fields__ = ['id', 'payload', 'description', 'events']
        __xml_fields__ = ['actions', 'dispatchs', 'active', 'needs_source']
#        __field_order__ = ['__actions__', 'active', 'name', 'display_name',
#                           'needs_source', 'variants',
#                           'last_run_date', 'dispatchs', 'tasks']
    
    class table_filler_type(TableFiller):
        __model__ = Tube
        
        #layers = render_link_field('/tubelayers/%s/edit', 'layers', 'display_name')
        def layers(self, object):
            variant_names = list()
            for layer in object.layers:
                if not layer.variant_name in variant_names:
                    variant_names.append(layer.variant_name)
            variant_names.sort()
            return ', '.join(variant_names)
            
        dispatchs = render_link_field('/dispatchs/%s', 'dispatchs', 'display_name')
        active = render_boolean('active')
        needs_source = render_boolean('needs_source')
    
    @has_model_permission('view')
    @expose('pyf.services.templates.tube.get_one')
    @expose('json')
    def get_one(self, tube_id, action=None, **kwargs):
        if action:
            return getattr(self, action)(tube_id, **kwargs)
        
        tmpl_context.widget = tubelayer_table
        
        tube = DBSession.query(Tube).get(tube_id)
        
        tmpl_context.launcher = TubeLauncher(tube_id)
        
        layers_value = tubelayer_table_filler.get_value(tube=tube)
        return dict(tube=tube, value=tube, layers_value=layers_value)
    
    @has_model_permission('view')
    @expose('pyf.services.templates.tube.get_one')
    @expose('json')
    def by_name(self, name):
        tube = DBSession.query(Tube).filter(Tube.name==name).first()
        if tube is None:
            abort(404, comment="There is no tube with name %s" % name)
        return self.get_one(tube.id)
    
    @has_model_permission('edit')
    @expose('pyf.services.templates.tube.edit')
    def edit(self, *args, **kwargs):
        return SecureCrudRestController.edit(self, *args, **kwargs)
    
    @has_model_permission('create')
    @expose('pyf.services.templates.tube.edit')
    def new(self, *args, **kwargs):
        return SecureCrudRestController.new(self, *args, **kwargs)
    
    @has_model_permission('launch')
    @expose()
    @expose('json')
    @validate(validators={
            'tube_id': validators.Int(not_none=True),
            'packets': validators.FieldStorageUploadConverter()
    })
    def launch(self, tube_id, variant=None, options=None, packets=None, **kwargs):
        user_name = request.identity['repoze.who.userid']
        
        # Trying to see if there is a newer version on the repo...
        repository = get_repository()
        tube = DBSession.query(Tube).get(tube_id)
        check_tube(repository, tube, variant=variant)
        
        if options is not None:
            options = simplejson.loads(options)
            
        if kwargs is not None:
            if options is not None:
                options.update(kwargs)
            else:
                options = kwargs
        
        if options is not None:
            valid_options = tube.get_valid_options()
            
            for key in options:
                if key not in valid_options:
                    raise NotAuthorizedError, "You can't set option %s" % key
                
        if packets is not None:
            packets = decode_packet_flow(packets.file)
                
        if variant == "no_variant":
            variant = None
                
        event_track_id = launch_tube(tube_id,
                                     user_name=user_name,
                                     variant=variant,
                                     defered=True,
                                     options=options,
                                     source=packets)
    
        time.sleep(1)
        
        if request.response_type == 'application/json':
            return dict(event_track_id=event_track_id)
        
        redirect('/events/%s' % event_track_id)
        
    @has_model_permission('view')
    @expose('json')
    def get_parameters(self, tube_id):
        tube = DBSession.query(Tube).get(tube_id)
        return dict(value=tube.get_parameters())
        
    @has_model_permission('view')
    @expose('json')
    def graph(self, tube_id):
        tube = DBSession.query(Tube).get(tube_id)
        
        tube_dict = dict(name=tube.display_name,
                         id="tube_%s" % tube.id,
                         data=dict(type="tube"),
                         children=list())
        
        variant_names = tube.variant_names
        
        tube_dict['children'].append(dict(
            name="default",
            id="var_default",
            data=dict(type="variant"),
            children=[tube.get_graph()]
        ))
        
        for name in variant_names:
            tube_dict['children'].append(dict(
                name=name,
                id="var_%s"%name,
                data=dict(type="variant"),
                children=[tube.get_graph(variant=name)]
            ))
        
        return tube_dict
    
    @expose('pyf.services.templates.tube.design')
    def design(self, tube_id):
        tube = DBSession.query(Tube).get(tube_id)
        
        return dict(tube=tube)
    
    @has_model_permission('view')
    @expose()
    def design_info(self, tube_id, jsonp=""):
        tube = DBSession.query(Tube).get(tube_id)
        
        infos = tube.get_network_graph(full_tree=False,
                                       all_infos=True,
                                       compute_position=False)
        
        nodes = infos.get('nodes')
        links = infos.get('links')
        
        modules = list()
        name_to_module_id = dict()
        wires = list()
        
        for node in nodes:
            item_id = len(modules)
            module_type = "%s %s" % (node.get('type'),
                                     node.get('source','plugin'))
                
            modules.append(dict(name=module_type, 
                                value=dict(name=node.get('name'),
                                           plugin=node.get('pluginname'),
                                           code=node.get('code'),
                                           content=node.get('content')),
                                config=dict(
                                    position=[node.get('x', 0),
                                              node.get('y', 0)]
                                )
                               )
                           )
            name_to_module_id[node.get('name')] = item_id
            
        for parent, child in links:
            wires.append(dict(src=dict(moduleId=name_to_module_id[parent],
                                       terminal="out"),
                              tgt=dict(moduleId=name_to_module_id[child],
                                       terminal="in")))
        
        return_content = dict(modules=modules,
                              wires=wires)
        
        if jsonp:
            return "%s = %s;" % (jsonp, simplejson.dumps(return_content))
        else:
            return simplejson.dumps(return_content)
#        return dict(tube=tube)

    @has_model_permission('edit')
    @expose('json')
    def save_graph(self, tube_id, payload=None):
        payload = simplejson.loads(payload)
        tube = DBSession.query(Tube).get(tube_id)
        
        from lxml import etree
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.fromstring(tube.payload, parser=parser)
        
        process = tree.find('process')
        
        for node in list(process.findall('node')) + list(process.findall('comment')):
            process.remove(node)
            
        nodes = list()
        links = list()
        
        for module in payload['modules']:
            if module.get('name') == "comment":
                el = etree.SubElement(process, 'comment',
                                   position = ','.join(map(str,
                                                           module.get('config').get('position'))))
                el.text = module['value']['comment']
                continue
                
            module_type, module_source = module.get('name').split(' ')
            module_values = module.get('value')
            el = etree.SubElement(process, 'node', **{'from': module_source,
                                                   'type': module_type,
                                                   'name': module_values.get('name'),
                                                   'position': ','.join(map(str, module.get('config').get('position')))})
            
            if module_source == 'plugin':
                el.set('pluginname', module_values.get('plugin'))
            elif module_source == 'code':
                code_el = etree.SubElement(el, 'code')
                code_el.text = etree.CDATA(module_values.get('code'))
            
            if module_values.get('content'):
                try:
                    for enode in etree.fromstring('<content>%s</content>' % module_values.get('content'), parser=parser):
                        el.append(enode)
                except SyntaxError:
                    return dict(status="error",
                                reason="bad formed xml in node %s" % module_values.get('name'))
            
            nodes.append(el)
            
        for wire in payload['wires']:
            if wire.get('src').get('terminal') == 'out':
                src = wire.get('src').get('moduleId')
                tgt = wire.get('tgt').get('moduleId')
            else:
                src = wire.get('tgt').get('moduleId')
                tgt = wire.get('src').get('moduleId')
            
            children_node = nodes[src].find('children')
            if children_node is None:
                children_node = etree.SubElement(nodes[src], 'children')
            
            links.append(etree.SubElement(children_node, 'link', name=nodes[tgt].get('name')))
            
        tube.payload = etree.tostring(tree)
        DBSession.add(tube)
        DBSession.flush()
        
        get_repository().store_item(tube, user=request.identity['user'].user_name)
        
        return dict(status="success")
