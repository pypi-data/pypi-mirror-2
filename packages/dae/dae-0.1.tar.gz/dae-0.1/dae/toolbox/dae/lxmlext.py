# -*- coding: utf-8 -*-
from __future__ import with_statement
from lxml import etree
import os
import cherrypy
import re

from copy import deepcopy

### xslt extensions
class DaCssElement(etree.XSLTExtension):
    def execute(self, context, da_node, document, output_parent):
        p = os.path.join(os.path.dirname(cherrypy.response.template),
                         da_node.attrib['src'])
        e = etree.Element('style')
        with open(p) as f:
            e.text = f.read()

        output_parent.append(e)


class DaJsElement(etree.XSLTExtension):
    def execute(self, context, da_node, document, output_parent):
        p = os.path.join(os.path.dirname(cherrypy.response.template),
                         da_node.attrib['src'])
        e = etree.Element('script')
        with open(p) as f:
            e.text = f.read()

        output_parent.extend([e])


class DaFormElement(etree.XSLTExtension):
    def execute(self, context, da_node, document, output_parent):
        document = deepcopy(document).xpath(da_node.attrib.get('xpath', '//document'))[0]
        print etree.tostring(document)
        form = etree.Element('form')
        def _execute():
            for node in da_node:
                if node.tag == 'password':
                    yield self.type_password(node, document)
                elif node.tag == 'submit':
                    yield self.type_submit(node, document)
                else:
                    yield getattr(self, 'type_'+node.attrib['type'])(node, document)
        form.extend(_execute())
        output_parent.extend([form])

    def hidden(self, node, document):
        return self.type_hidden(node, document)
    
    def type_hidden(self, node, document):
        e = etree.Element('input')
        e.attrib['type'] = 'hidden'
        e.attrib['name'] = node.tag
        val = document.find(node.tag)
        if val is not None:
            e.attrib['value'] = val.text
        return e
        
    def type_id(self, node, document):
        pass

    def type_password(self, node, document):
        return self.type_text(node, document, t='password')

    def type_submit(self, node, document):
        e = etree.Element('input')
        e.attrib['type'] = 'submit'
        e.attrib['value'] = node.attrib.get('value', 'Submit')
        return e
    
    def type_text(self, node, document, t='text'):
        span = etree.Element('span')
        
        label = etree.Element('label')
        label.attrib['for'] = node.tag
        label.text = ' '.join(node.tag.split('_')).title()
        
        inp = etree.Element('input')
        inp.attrib['type'] = t
        inp.attrib['name'] = node.tag
        inp.attrib['id'] = node.tag

        span.extend([label, inp, etree.Element('br')])
        return span


dacss = DaCssElement()
dajs = DaJsElement()
daform = DaFormElement()

extensions = {('dasa.cc', 'css'): dacss, ('dasa.cc', 'js'): dajs, ('dasa.cc', 'form'): daform}
###

### xpath extensions
def search(context, pattern, string):
    if isinstance(string, list) and len(string) > 0:
        string = string[0]
    else:
        string = ''
    
    if isinstance(string, etree._Element):
        string = string.text
    
    r = re.search(pattern, '%s' % string)
    if r is not None:
        return r.group(0)
    return ''

def sub(context, pattern, repl, string):
    if isinstance(string, list) and len(string) > 0:
        string = string[0]
    else:
        string = ''
    
    if isinstance(string, etree._Element):
        string = string.text

    return re.sub(pattern, repl, string)

ns = etree.FunctionNamespace('dasa.cc')
ns.prefix = 'da'
ns['search'] = search
ns['sub'] = sub