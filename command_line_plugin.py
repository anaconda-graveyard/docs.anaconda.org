# -*- coding: utf-8 -*-
"""
Contains classes and utilities related to meta data in hyde.
"""

from subprocess import check_output, CalledProcessError, STDOUT
from hyde.plugin import Plugin
import re
import os
import pipes
import shutil

def make_anchor(s):
    anchor = re.sub('\W', ' ', s).title().replace(' ', '')
    return anchor

def link(anchor):
    return '<a id="%s"  href="#%s" name="%s" class="section-anchor">&nbsp;</a>' % (anchor, anchor, anchor)

class CommandLinePlugin(Plugin):
    def __init__(self, site):

        if os.path.isdir('cache'):
            shutil.rmtree('cache')
        os.mkdir('cache')

        Plugin.__init__(self, site)
        self.index = []

        self.globals = {'command_line_help': self.command_line_help,
                        'json_command_line_help': self.json_command_line_help,
                        'page_header': self.page_header,
                        'edit': self.edit}

    SECTION_TAG = '<div class="method-section"><div class="method-description">{%filter markdown%}'
    EXAMPLE_TAG = '{%endfilter%}</div><div class="method-example">{%filter markdown%}'
    END_SECTION_TAG = '{%endfilter%}</div></div>'

    def expand_sections(self, text):
        text = re.sub('{%\W*section\W*%}', self.SECTION_TAG, text)
        text = re.sub('{%\W*example\W*%}', self.EXAMPLE_TAG, text)
        text = re.sub('{%\W*endsection\W*%}', self.END_SECTION_TAG, text)

        return text

    USERDEFINED = (r'[#\~]userdefined[{:\(](.+?)[}:\)]', r'<span class="userdefined">\1</span>')

    POST_REPLACEMENT_MACROS = [USERDEFINED]

    def text_resource_complete(self, resource, text):
        for pattern, repl in self.POST_REPLACEMENT_MACROS:
            text = re.sub(pattern, repl, text)
        return Plugin.text_resource_complete(self, resource, text)

    def edit(self, template):
        filename = template._TemplateReference__context.name
        repo = self.site.config.context.data.repo
        branch = self.site.config.context.data.get('branch', 'master')

        url = '%s/blob/%s/content/%s' % (repo, branch, filename)

        result = '<a title="Edit on Github" href="%s">' % url
        result += '<span class="glyphicon glyphicon-pencil"></span></a>'

        return result

    def page_header(self, template, resource, title, h=2):
        result = resource.add_index(title)
        filename = template._TemplateReference__context.name

        repo = self.site.config.context.data.repo
        branch = self.site.config.context.data.get('branch', 'master')

        url = '%s/edit/%s/content/%s' % (repo, branch, filename)
        result += '<h%i>%s' % (h, title)
        result += '<small class="pull-right">%s' % self.edit(template)
        result += '</small></h%i>' % h
        return result


    def begin_text_resource(self, resource, text):
        text = self.expand_sections(text)

        def acall(*args, **kwargs):
            print args
            print kwargs
        resource.pdb = acall


        resource.xindex = []

        def r_add_index(title, level=1):
            anchor = make_anchor(title)
            xindex = resource.xindex
            while level > 1:
                xindex = xindex[-1][-1]
                level -= 1
            xindex.append([title, anchor, []])
            return link(anchor)

        resource.add_index = r_add_index
        resource.add_subindex = lambda title: r_add_index(title, 2)
        resource.add_subsubindex = lambda title: r_add_index(title, 3)

        self.template.env.globals.update(self.globals)

        return Plugin.begin_text_resource(self, resource, text)

    def json_command_line_help(self, shell):
        try:
            import json
            output = check_output(shell, shell=True, stderr=STDOUT)
            return json.loads(output)
        except CalledProcessError as err:
            output = err.output
        return output

    def command_line_help(self, shell):
        if not os.path.isdir('cache'):
            os.mkdir('cache')

        fn = os.path.join('cache', shell)

        if os.path.exists(fn):
            return open(fn).read()

        try:
            output = check_output(shell, shell=True, stderr=STDOUT)
            open(fn, 'w').write(output)
        except CalledProcessError as err:
            output = err.output
        return output

    def template_loaded(self, template):

        self.template = template

        self.template.env.globals.update(self.globals)
