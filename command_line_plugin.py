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

class CommandLinePlugin(Plugin):
    def __init__(self, site):

        if os.path.isdir('cache'):
            shutil.rmtree('cache')
        os.mkdir('cache')

        Plugin.__init__(self, site)
        self.index = []

        self.globals = {'command_line_help': self.command_line_help,
                        'page_header': self.page_header}

    SECTION_TAG = '<div class="method-section"><div class="method-description">{%filter markdown%}'
    EXAMPLE_TAG = '{%endfilter%}</div><div class="method-example">{%filter markdown%}'
    END_SECTION_TAG = '{%endfilter%}</div></div>'

    def expand_sections(self, text):
        text = re.sub('{%\W*section\W*%}', self.SECTION_TAG, text)
        text = re.sub('{%\W*example\W*%}', self.EXAMPLE_TAG, text)
        text = re.sub('{%\W*endsection\W*%}', self.END_SECTION_TAG, text)

        return text

    USERDEFINED = (r'#userdefined{(.+?)}', r'<span class="userdefined">\1</span>')

    POST_REPLACEMENT_MACROS = [USERDEFINED]

    def text_resource_complete(self, resource, text):
        for pattern, repl in self.POST_REPLACEMENT_MACROS:
            text = re.sub(pattern, repl, text)
        return Plugin.text_resource_complete(self, resource, text)

    def page_header(self, template, resource, title):
        result = resource.add_index(title)
        filename = template._TemplateReference__context.name

        repo = self.site.config.context.data.repo
        branch = self.site.config.context.data.get('branch', 'master')

        url = '%s/edit/%s/content/%s' % (repo, branch, filename)
        result += '<h2>%s' % title
        result += '<small class="pull-right"><a href="%s">' % url
        result += '<span class="glyphicon glyphicon-pencil"><span>edit</a>'
        result += '</small></h2>'
        return result


    def begin_text_resource(self, resource, text):
        text = self.expand_sections(text)

        def acall(*args, **kwargs):
            print args
            print kwargs
        resource.pdb = acall


        resource.xindex = []

        def r_add_index(title):
            anchor = make_anchor(title)
            resource.xindex.append([title, anchor, []])
            return '<a id="%s"  href="#%s" name="%s" class="section-anchor">&nbsp;</a>' % (anchor, anchor, title)
        resource.add_index = r_add_index

        def r_add_subindex(title):
            if resource.xindex:
                sub_index = resource.xindex[-1][-1]
                anchor = make_anchor(title)
                sub_index.append([title, anchor, []])
                return '<a id="%s"  href="#%s" name="%s" class="section-anchor">&nbsp;</a>' % (anchor, anchor, title)

        resource.add_subindex = r_add_subindex

        def r_add_subsubindex(title):
            if resource.xindex:
                sub_index = resource.xindex[-1][-1]
                subsub_index = sub_index[-1][-1]
                anchor = make_anchor(title)
                subsub_index.append([title, anchor, []])
                return '<a id="%s" href="#%s" name="%s" class="section-anchor">&nbsp;</a>' % (anchor, anchor, title)

        resource.add_subsubindex = r_add_subsubindex

        self.template.env.globals.update(self.globals)

        return Plugin.begin_text_resource(self, resource, text)

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
