#!/usr/bin/env python
#  -*- mode: python; indent-tabs-mode: nil; -*- coding: utf-8 -*-

"""

GutenbergRSTParser.py

Copyright 2010 by Marcello Perathoner

Distributable under the GNU General Public License Version 3 or newer.

A slightly modified RST parser for docutils.

"""

# TODO: directive for thoughtbreaks

import re
import itertools

from docutils import nodes, transforms
from docutils.utils import unescape
import docutils.parsers.rst
from docutils.parsers.rst import Directive, directives, states, roles, frontend
from docutils.parsers.rst.directives import tables
from docutils.parsers.rst.directives import images

from epubmaker.lib.Logger import error, info, debug, warn

from epubmaker.mydocutils import nodes as mynodes
from epubmaker.mydocutils.transforms import parts

# pylint: disable=W0142, W0102

class Style (Directive):
    """ Set presentational preferences for docutils element.
    
    """

    optional_arguments = 1
    option_spec = { 'class': directives.class_option,
                    'rmclass': directives.class_option,
                    'language': directives.class_option } # FIXME a lang not a class

    def run (self):
        if self.arguments:
            self.options['selector'] = self.arguments[0]
        pending = nodes.pending (parts.StyleTransform, self.options) 
        self.state_machine.document.note_pending (pending)
        return [pending]


class VSpace (Directive):
    """
    Directive to insert vertical spacing or pagebreaks.
    """

    required_arguments = 0
    optional_arguments = 1

    def run (self):
        arg = self.arguments[0] if self.arguments else self.name

        page = mynodes.page ()
        
        if arg in ('clearpage', 'cleardoublepage', 'vfill',
                   'frontmatter', 'mainmatter', 'backmatter'):
            page['classes'].append (arg)
        else:
            try:
                arg = abs (int (arg))
            except ValueError:
                raise self.error ('Unknown argument "%s" for "%s" directive.' % (arg, self.name))

            page['classes'].append ('vspace')
            page['length'] = arg
            
        return [page]


class EndSection (Directive):
    """ Closes section. """

    def run (self):
        debug ('Endsection directive state: %s' % self.state)
        # back out of lists, etc.
        if isinstance (self.state, states.SpecializedBody):
            debug ('Backing out of list')
            self.state_machine.previous_line (2) # why do we need 2 ???
        raise EOFError


class DropCap (Directive):
    """ Puts a dropcap onto the next paragraph.

    """

    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True

    option_spec = { 'image': directives.unchanged,
                    'lines': directives.positive_int,
                    'indents': directives.unchanged, # array of tex dimen
                    'ante': directives.unchanged }

    def run (self):
        self.options['char'] = self.arguments[0]
        if len (self.arguments) >= 2:
            self.options['span'] = self.arguments[1]
        pending = nodes.pending (parts.DropCapTransform, self.options) 
        self.state_machine.document.note_pending (pending)
        return [pending]


class Example (Directive):
    """
    Builds a literal block with the example source followed by a rendered block.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    option_spec = { 'norender': directives.flag }

    def run(self):
        literal = nodes.literal_block ('', '\n'.join (self.content))
        literal['classes'].append ('example-source')

        nodelist = [ literal ]
        
        if 'norender' not in self.options:
            container = nodes.container ()
            container['classes'].append ('example-rendered')
            self.state.nested_parse (self.content, self.content_offset,
                                     container)
            nodelist.append (container)
        
        if len (self.arguments) >= 1:
            nodelist.extend (nodes.caption ('', self.arguments[0]))

        return nodelist


def LoXtarget (X, id_):
    id_ = nodes.make_id (id_)
    X['ids'].append (id_)
    return X


class Table (tables.RSTTable):
    
    align_table_values = ('left', 'center', 'right')
    align_cell_values  = ('left', 'center', 'right', 'justify')
    valign_cell_values = ('top',  'middle', 'bottom')
    
    def align (argument):
        # This is not callable as self.align.  We cannot make it a
        # staticmethod because we're saving an unbound method in
        # option_spec below.
        return directives.choice (argument, Table.align_table_values)

    def align_list (argument):
        """
        Checks for a space-separated list of alignment values.
        Raises ValueError for bogus values.
        """
        entries = argument.split ()
        for e in entries:
            directives.choice (e, Table.align_cell_values)
        return entries

    def valign_list (argument):
        """
        Checks for a space-separated list of alignment values.
        Raises ValueError for bogus values.
        """
        entries = argument.split ()
        for e in entries:
            directives.choice (e, Table.valign_cell_values)
        return entries


    option_spec = {
        'align': align,
        'width': directives.length_or_percentage_or_unitless,
        'widths': directives.positive_int_list,
        'aligns': align_list,
        'vertical-aligns': valign_list,
        'summary': directives.unchanged,
        'tabularcolumns': directives.unchanged,
        'class': directives.class_option
        }
    
    table_count = 0

    def run (self):
        res = tables.RSTTable.run (self)
        table = res[0]

        Table.table_count += 1
        target = LoXtarget (table, 'table-%d' % Table.table_count)
        self.state_machine.document.note_implicit_target (target, target)
        
        table['align']   = self.options.get ('align',   'center')
        table['summary'] = self.options.get ('summary', 'no summary')
        table['width']   = self.options.get ('width',   '100%')
        table['tabularcolumns'] = self.options.get ('tabularcolumns')

        # HTML doesn't recognize align in colspec ???
        widths  = self.options.get ('widths', [])
        aligns  = self.options.get ('aligns', [])
        valigns = self.options.get ('vertical-aligns', [])
        if widths or aligns or valigns:
            iter_ = itertools.izip_longest (widths, aligns, valigns, fillvalue = None)
            for colspec in table.traverse (nodes.colspec):
                w, a, v = iter_.next ()
                colspec['colwidth'] = w or 10
                colspec['align']    = a or 'justify'
                colspec['valign']   = v or 'middle'
        
        return res
    
    
class Figure (images.Figure):

    figure_count = 0
    
    def run (self):
        res = images.Figure.run (self)
        figure = res[0]

        Figure.figure_count += 1
        target = LoXtarget (figure, 'figure-%d' % Figure.figure_count)
        self.state_machine.document.note_implicit_target (target, target)

        return res
    
    
class TocEntry (Directive):
    """ Directive to inject TOC entry.

    This directive changes the next header, so we can choose the
    text of the TOC entry.

    The 'depth' option changes toc gathering level.

    We insert a pending node that gets transformed in later stages of processing.

    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = { 'depth': directives.nonnegative_int }

    def run (self):
        details = {}
        if 'depth' in self.options:
            details['toc_depth'] = self.options['depth']
        if self.arguments:
            details['toc_entry'] = self.arguments[0]

        pending = nodes.pending (parts.TocEntryTransform, details) 
        self.state_machine.document.note_pending (pending)
        return [pending]


def option_check_backlinks (arg): # pylint: disable=E0213
    """ Argument checker function. """
    value = directives.choice (arg, ('top', 'entry', 'none'))
    return None if value == 'none' else value


class GeneratedSection (Directive):
    """ Base class for generated sections (Contents, Footnotes, Citations, etc.). """

    required_arguments = 0   # the section name: required if not :local:
    optional_arguments = 1
    final_argument_whitespace = True
    
    option_spec = { 'class': directives.class_option,
                    'local': directives.flag,
                    'backlinks': option_check_backlinks,
                    'page-numbers': directives.flag }
    
    def run (self, pending_class, extraclasses = []):
        ## if not (self.state_machine.match_titles
        ##         or isinstance (self.state_machine.node, nodes.sidebar)):
        ##     raise self.error ('The "%s" directive may not be used within '
        ##                       'topics or body elements.' % self.name)
        
        document = self.state_machine.document
            
        if 'local' in self.options:
            container = nodes.container ()
            container['classes'] = ['local']
            container['classes'] += map (lambda x: 'local-' + x, extraclasses)
        else:
            if len (self.arguments) != 1:
                raise self.error ('The "%s" directive must have either an argument '
                                  'or the option :local: specified.' % self.name)
            container = nodes.section ()
            container['classes'] += extraclasses
            
        container['classes'] += self.options.get ('class', [])

        if 'depth' in self.options:
            container['toc_depth'] = self.options['depth']

        if self.arguments:
            title_text = self.arguments[0]
            text_nodes, dummy_messages = self.state.inline_text (title_text,
                                                          self.lineno)
            title = nodes.title (title_text, '', *text_nodes)
            title['toc_entry'] = None
            container += title
        
        document.note_implicit_target (container)

        pending = nodes.pending (pending_class, self.options)
        document.note_pending (pending)

        container += pending
        return [container]


class Contents (GeneratedSection):
    """ Table of contents. """

    option_spec = GeneratedSection.option_spec.copy ()
    option_spec.update ( {'depth': directives.nonnegative_int } )
    
    def run (self):
        return GeneratedSection.run (self, parts.ContentsTransform, ['contents'])


class LoF (GeneratedSection):
    """ List of Figures. """

    def run (self):
        return GeneratedSection.run (self, parts.ListOfFiguresTransform, ['lof'])


class LoT (GeneratedSection):
    """ List of Tables. """

    def run (self):
        return GeneratedSection.run (self, parts.ListOfTablesTransform, ['lot'])


class Footnotes (GeneratedSection):
    """ Footnote section. """

    option_spec = GeneratedSection.option_spec.copy ()
    option_spec.update ( {'backlinks': directives.flag } )
    
    def run (self):
        return GeneratedSection.run (self, parts.HTMLFootnotesTransform, ['footnotes'])


# roles

def mk_pageno_target (text, options = {}):
    """ Create and initialize a target node. """
    
    id_ = nodes.make_id ('page-%s' % text)
    target = nodes.target ('', '')
    target['ids'].append (id_)
    target['classes'].append ('pageno')
    if 'classes' in options:
        target['classes'].extend (options['classes'])
    target['pageno'] = text
    target['html_attributes'] = {'title' : text}
    target['refid'] = None # avoid transform moving this target into next section
    return target


class Role:
    """
    Base class for our roles.
    """

    def __init__ (self, options = {}, content = []):
        self.options = { 'class': directives.class_option }
        self.options.update (options)

    def __call__ (self, role, rawtext, text, lineno, inliner, options={}, content=[]):
        """ return [nodelist], [messagelist] """
        roles.set_classes (options)
        inline = nodes.inline (rawtext, unescape (text), **options)
        inline['classes'].append (role)
        return [ inline ], [] 


## class LineBreakRole (Role):
##     """ A text with a forced line break. """
    
##     def __init__ (self, options={}, content=[]):
##         Role.__init__ (self, options, content)
##         self.options.update ({'before': directives.flag })
    
##     def __call__ (self, role, rawtext, text, lineno, inliner, options={}, content=[]):
##         roles.set_classes (options)
##         res, msgs = Role.__call__ (
##             self, role, rawtext, text, lineno, inliner, options, content)

##         pos = 0 if 'before' in options else len (res)
##         res.insert (pos, mynodes.newline ())
##         return res, msgs


class PageNumberRole (Role):
    """ A page number marker. """
    
    def __call__ (self, role, rawtext, text, lineno, inliner, options={}, content=[]):
        roles.set_classes (options)
        target = mk_pageno_target (text, options)
        inliner.document.note_implicit_target (target)
        return [target], [] 


class PageReferenceRole (Role):
    """ A page number reference. """

    def __call__ (self, role, rawtext, text, lineno, inliner, options={}, content=[]):
        roles.set_classes (options)
        id_ = nodes.make_id ('page-%s' % text)
        reference = nodes.reference (rawtext, unescape (text))
        reference['refid'] = id_
        return [reference], []


class Inliner (states.Inliner):
    """ Inliner that recognizes [pg n] page numbers. """

    re_pageno = re.compile (states.Inliner.start_string_prefix +
                            r"(\[pg!?\s*(?P<pageno>[ivxlc\d]+)\])" +
                            states.Inliner.end_string_suffix + r'\s*', re.IGNORECASE)
    re_pageref = re.compile (states.Inliner.start_string_prefix +
                            r"(\[pg\s*(?P<pageno>[ivxlc\d]+)\]_)" +
                            states.Inliner.end_string_suffix, re.IGNORECASE)

    def __init__ (self):
        states.Inliner.__init__ (self)
        

    def init_customizations (self, settings):
        """ Setting-based customizations; run when parsing begins. """

        if settings.page_numbers:
            # pylint: disable=E1101
            self.implicit_dispatch.append ((self.re_pageno, self.pageno_target))
            self.implicit_dispatch.append ((self.re_pageref, self.pageno_reference))
        
        
    def pageno_target (self, match, dummy_lineno):
        """ Makes [pg 99] into implicit markup for page numbers. """
        
        text = match.group (0)
        if text.startswith ('[pg'):
            target = mk_pageno_target (match.group ('pageno'))
            if '!' in text:
                target['classes'].append ('invisible')
            self.document.note_implicit_target (target) # pylint: disable=E1101
            return [target]
        else:
            raise states.MarkupMismatch

        
    def pageno_reference (self, match, dummy_lineno):
        """ Makes [pg 99]_ into implicit markup for page reference. """
        
        text = match.group (0)
        if text.startswith ('[pg'):
            text = match.group ('pageno')
            id_ = nodes.make_id ('page-%s' % text)
            reference = nodes.reference ('', unescape (text))
            reference['refid'] = id_
            return [reference]
        else:
            raise states.MarkupMismatch


class Body (states.Body):
    """ Body class with fix for line block indentation. """

    def nest_line_block_level (self, block, block_level, indent_map):
        """ Recursive part of nest_line_block_segment. """
        
        line_block = nodes.line_block ()
        while len (block):
            item_level = indent_map[block[0].indent]
            if item_level < block_level:
                break # end recursion
            if item_level > block_level:
                line_block.append (self.nest_line_block_level (block, block_level + 1, indent_map))
                continue
            # item_level == block_level
            line_block.append (block.pop (0))
        return line_block
        

    def nest_line_block_segment (self, block):
        """
        Replacement for docutils.states.Body.nest_line_block_segment
        with fix for correct indentation.
        """
        
        indents = [item.indent for item in block]

        # map leading space count to indent steps
        indent_map = dict (itertools.izip (
            [k for k, g in itertools.groupby (sorted (indents))],
            itertools.count ()
            ))

        new_block = self.nest_line_block_level (block, 0, indent_map)
        block.replace_self (new_block)
    
        
class Parser (docutils.parsers.rst.Parser):
    """ Slightly modified rst parser. """

    def __init__ (self):
        self.settings_spec = (
            'PG reStructuredText Parser Options', 
            None,
            self.settings_spec[2] + 
            (('Recognize page numbers and page references (like "[pg n] and [pg n]_").',
             ['--page-numbers'],
             {'action': 'store_true', 'validator': frontend.validate_boolean}),))

        directives.register_directive ('contents',        Contents) # replaces standard directive
        directives.register_directive ('lof',             LoF)
        directives.register_directive ('lot',             LoT)
        directives.register_directive ('table',           Table)    # replaces standard directive
        directives.register_directive ('figure',          Figure)   # replaces standard directive
        directives.register_directive ('toc-entry',       TocEntry)
        directives.register_directive ('footnotes',       Footnotes)
        directives.register_directive ('dropcap',         DropCap)
        directives.register_directive ('example',         Example)
        directives.register_directive ('style',           Style)
        
        directives.register_directive ('endsection',      EndSection)

        directives.register_directive ('vspace',          VSpace)
        directives.register_directive ('vfill',           VSpace)
        directives.register_directive ('clearpage',       VSpace)
        directives.register_directive ('cleardoublepage', VSpace)
        directives.register_directive ('frontmatter',     VSpace)
        directives.register_directive ('mainmatter',      VSpace)
        directives.register_directive ('backmatter',      VSpace)

        self.register_local_role ('page-number',    PageNumberRole)
        self.register_local_role ('page-reference', PageReferenceRole) 
        ## self.register_local_role ('line-break',     LineBreakRole) 

        docutils.parsers.rst.Parser.__init__ (self)
        self.inliner = Inliner ()


    def register_local_role (self, name, role):
        """ Helper """
        
        r = role ()
        r.role_name = name
        roles.register_local_role (name, r) 
        
        
    def get_transforms (self):
        tfs = docutils.parsers.rst.Parser.get_transforms (self)
        return tfs + [parts.PageNumberMoverTransform,
                      parts.TocPageNumberTransform,
                      parts.CharsetTransform,
                      parts.TextTransform,
                      parts.NewlineTransform,
                      parts.DefaultPresentation,
                      parts.AlignTransform,
                      parts.ImageWrapper,
                      parts.TitleLevelTransform,
                      parts.FirstParagraphTransform,
                      parts.Lineblock2VSpace]


# horrible hack, substitute our bug-fixed Body class
states.state_classes = (Body, ) + states.state_classes[1:]

