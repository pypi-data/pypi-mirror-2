# −*− coding: UTF−8 −*−

# Copyright (C) 2010 Joel Dunham
#
# This file is part of OnlineLinguisticDatabase.
#
# OnlineLinguisticDatabase is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OnlineLinguisticDatabase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OnlineLinguisticDatabase.  If not, see
# <http://www.gnu.org/licenses/>.

import re

from pylons import request, response, session, app_globals, tmpl_context as c
from pylons.controllers.util import abort, redirect

from onlinelinguisticdatabase.lib.base import BaseController, render
import onlinelinguisticdatabase.model as model
import onlinelinguisticdatabase.model.meta as meta
import onlinelinguisticdatabase.lib.helpers as h

"""
The exporter module contains Exporter objects used to create OLD export strings
which can then be saved as files.

The global variable 'exporters' is a list containing all the exporter instances
that will be imported by the export controller and thereby made available for
exporting.  To create a new export option, define a new Exporter and add it to
exporters.

Each exporter object is an instance of the Exporter class, which is a relatively
contentless class, but which requires particular attributes.  The real work of
generating the export string is accomplished by the exporter's export function,
which is defined on a per-instance basis.

The input to Exporter.export is one of the following:

1. a string of the form 'formx', where 'x' is the ID of an OLD Form that should
   be exported
2. the string 'memory', indicating that the contents of the current user's
   memory should be exported
3. the string 'lastsearch', indicating that the results of the most recent
   search (stored in the session) should be exported
4. a string of the form 'collectionformsx', where 'x' is the ID of an OLD
   Collection whose associated Forms should be exported
5. a string of the form 'collectioncontentx', where 'x' is the ID of an OLD
   Collection whose content (with embedded Forms) should be exported
"""


class Exporter(object):
    """Exporter class defines objects that can create export strings from one or
    more of the five types of input described in this module's docstring
        
    Each exporter must define the following attributes/methods:
    
    1. 'name': used to identify the exporter
    2. 'description': tells users what the exporter does
    3. 'inputTypes': a subset (python list) of the inputs listed in this
       module's docstring; indicates which kinds of inputs the exporter handles
    4. 'extension': the extension that should be given to the resultant file
    5. 'exporterFunction': function that processes the input and returns a
       result

    """

    def export(self, input):
        return self.exporterFunction(input)



################################################################################
############## Functions for getting the input as a list of Forms
################################################################################

def getFormList(input):
    """Returns a list of Forms.  The input may be one of the following four
    options:
    
    1. a string of the form 'formx', where 'x' is a Form ID
    2. a string of the form 'collectionx', where 'x' is a Collection ID
    3. the string 'memory'
    4. the string 'last search'
    """
    if input[:4] == 'form':
        return getFormListFromFormID(int(input[4:]))
    elif input[:15] == 'collectionforms':
        return getFormListFromCollectionID(int(input[15:]))
    elif input == 'memory':
        return getFormListFromMemory()
    elif input == 'lastsearch':
        return getFormListFromLastSearch()
    else:
        return None


def getFormListFromFormID(formID):
    """Return a list containing the Form with ID=formID.
    
    """
    form_q = meta.Session.query(model.Form)
    return [form_q.get(formID)]


def getFormListFromCollectionID(collectionID):
    """Return the list of Forms referenced by the Collection with
    ID=collectionID.
    
    """
    collection_q = meta.Session.query(model.Collection)
    collection = collection_q.get(collectionID)
    return collection.forms


def getFormListFromMemory():
    """Return the list of all Forms memorized by the currently logged in user.
    
    """
    user = meta.Session.query(model.User).filter(
        model.User.id==session['user_id']).first()
    return meta.Session.query(model.Form).order_by(
        model.Form.id).filter(model.Form.memorizers.contains(user)).all() 


def getFormListFromLastSearch():
    """Whenever a OLD Form search is effected, the values of the HTML Form Search
    form are stored in the session under the key 'formSearchValues'.  Use these
    values to recreate the last search and return the resultant Forms.
    
    """
    result = session['formSearchValues']
    form_q = meta.Session.query(model.Form)
    return h.filterSearchQuery(result, form_q, 'Form').order_by(
        model.Form.id).all()


def getCollectionContent(input):
    """Return the content of the Collection with ID=collectionID.
    
    """
    collectionID = int(input[17:])
    collection_q = meta.Session.query(model.Collection)
    collection = collection_q.get(collectionID)
    return collection.contents


################################################################################
############## Get a Collection from an input of the form 'collectioncontentx'
##### where 'x' is the ID of a Collection
################################################################################


def getCollection(input):
    """Return the Collection with ID=collectionID.
    
    """
    collectionID = int(input[17:])
    collection_q = meta.Session.query(model.Collection)
    return collection_q.get(collectionID)


################################################################################
############## Various constants
################################################################################


formListInputTypes = lambda x: x in ['memory', 'lastsearch'] or \
    x[:4] == 'form' or x[:15] == 'collectionforms'


collectionContentInputType = lambda x: x[:17] == 'collectioncontent'


################################################################################
############## Functions that process a single Form
################################################################################


def plainTextTranscription(form):
    """Return the grammaticality followed by the transcription.

    """
    return '%s%s' % (
        form.grammaticality, h.storageToOutputTranslate(form.transcription))


def plainTextTranscriptionGlossNewline(form):
    """Return the (grammaticality + ) transcription, followed by each gloss
    (with gloss grammaticality) on its own line.

    """
    result = '%s%s' % (
        form.grammaticality, h.storageToOutputTranslate(form.transcription))
    result += '\n' + '\n'.join(['%s%s' % (
        gloss.glossGrammaticality, gloss.gloss) for gloss in form.glosses])
    return result


def plainTextIGT(form):
    """Interlinear Gloss Text: transcription, morphBreak, morphGloss, gloss
    all separated by newlines.

    """
    result = '%s%s' % (
        form.grammaticality, h.storageToOutputTranslate(form.transcription))
    if form.morphemeBreak:
        result += '\n%s' % h.storageToOutputTranslate(form.morphemeBreak, True)
    if form.morphemeGloss:
        result += '\n%s' % form.morphemeGloss
    result += '\n%s' % '\n'.join(['%s%s' % (gloss.glossGrammaticality, \
        gloss.gloss) for gloss in form.glosses])
    return result


def secondaryData(form):
    """Comments, speaker comments and an 'OLD reference' separated by newlines.
    The 'OLD reference' is the date elicited followed by the ID in parentheses.

    """
    result = u''
    if form.comments:
        result += '%s\n' % h.storageToOutputTranslateOLOnly(form.comments)
    if form.speakerComments:
        result += '%s\n' % h.storageToOutputTranslateOLOnly(form.speakerComments)
    if form.dateElicited:
        result += '\n%s (%s)' % (
            form.dateElicited.strftime('%b %d, %Y'), form.id)
    else:
        result += '(%s)' % form.id
    return result


def allTabDelimited(form):
    """All the data of a Form, tab-delimited.

    """
    formList = [
        str(form.id),
        '%s%s' % (form.grammaticality,
                  h.storageToOutputTranslate(form.transcription)),
        h.storageToOutputTranslate(form.morphemeBreak, True) or '',
        form.morphemeGloss or '',
        '; '.join(['%s%s' % (x.glossGrammaticality,
                        x.gloss.replace(';', '.')) for x in form.glosses]),
        form.comments and h.storageToOutputTranslateOLOnly(form.comments) or '',
        form.speakerComments and h.storageToOutputTranslateOLOnly(
            form.speakerComments) or '',
        form.dateElicited and form.dateElicited.strftime('%b %d, %Y') or '',
        form.datetimeEntered and form.datetimeEntered.strftime(
            '%b %d, %Y at %I:%M %p') or '',
        form.datetimeModified and form.datetimeModified.strftime(
            '%b %d, %Y at %I:%M %p') or '',
        form.syntacticCategoryString and form.syntacticCategoryString or '',
        form.elicitor and '%s %s' % (form.elicitor.firstName,
                                     form.elicitor.lastName) or '',
        form.enterer and '%s %s' % (form.enterer.firstName,
                                    form.enterer.lastName) or '',
        form.verifier and '%s %s' % (form.verifier.firstName,
                                     form.verifier.lastName) or '',
        form.speaker and '%s %s' % (form.speaker.firstName,
                                    form.speaker.lastName) or '',
        form.elicitationMethod and form.elicitationMethod.name or '',
        form.syntacticCategory and form.syntacticCategory.name or '',
        form.source and '%s (%s)' % (form.source.authorLastName,
                                     form.source.year) or '',
        form.keywords and '; '.join(
            [x.name.replace(';', '.') for x in form.keywords]) or ''
    ]
    return u'\t'.join([x.replace('\t', ' ') for x in formList])


def xelatexCovington(form):
    """A XeLaTeX representation of a Form using the Covington package to put the
    words into IGT formatted examples.  Because non-ascii characters might occur
    in the Form, XeLaTeX (not just plain LaTeX) will be required to process the
    document. 
    
    Note: I was originally using h.capsToLatexSmallCaps to convert uppercase
    glosses to LaTeX smallcaps (\textsc{}), but the Aboriginal Serif font was
    not rendering the smallcaps, so I removed the function.  If I can figure out
    how to use XeLaTeX with a font that will render NAPA symbols AND make
    smallcaps, then the function should be reinstated...
    """
    if not form:
        return u'\t\\item WARNING: BAD FORM REFERENCE'
    else:
        # If the Form has a morphological analysis, use Covington for IGT
        if form.morphemeBreak and form.morphemeGloss:
            result = u'\t\\item'
            result += '\n\t\t\\glll %s%s' % (
                form.grammaticality, h.storageToOutputTranslate(form.transcription))
            result += '\n\t\t%s' % h.storageToOutputTranslate(form.morphemeBreak, True)
            result += '\n\t\t%s' % form.morphemeGloss
            result += '\n\t\t\\glt %s' % '\\\\ \n\t\t'.join(['`%s%s\'' % (
                gloss.glossGrammaticality, gloss.gloss) for gloss in form.glosses])
            result += '\n\t\t\\glend'
        # If no morphological analysis, just put transcr and gloss(es) on separate
        #  lines
        else:
            result = u'\t\\item'
            result += '\n\t\t%s%s \\\\' % (
                form.grammaticality, h.storageToOutputTranslate(form.transcription))
            result += '\n\t\t%s' % ' \\\\\n\t\t'.join(['`%s%s\'' % (
                gloss.glossGrammaticality, gloss.gloss) for gloss in form.glosses])
        return result


def xelatexSecondaryData(form, reference=True):
    """Return the Form's comments, speaker comments and a reference as a LaTeX
    itemized list.  Reference is 'x(yz)' where 'x' is the speaker's initials,
    'y' is the date elicited and 'z' is the id of the Form.  If reference is
    False, no reference to the Form is added.
    
    """
    result = u'\t\\begin{itemize}'
    
    if form.comments:
        result += '\n\t\t\\item %s' % h.storageToOutputTranslateOLOnly(
            form.comments)
    
    if form.speakerComments:
        result += '\n\t\t\\item %s' % h.storageToOutputTranslateOLOnly(
            form.speakerComments)

    if reference:
        
        if form.speaker:
            speaker = '%s%s ' % (
                form.speaker.firstName[0].upper(), form.speaker.lastName[0].upper())
        else:
            speaker = ''
        
        if form.dateElicited:
            dateElicited = form.dateElicited.strftime('%b %d, %Y; ')
        else:
            dateElicited = ''
        
        if form.speaker:
            result += '\n\t\t\\item %s(%s%s)' % (
                speaker, dateElicited, 'OLD ID: %s' % form.id)
        elif form.source:
            source = '%s (%s) ' % (form.source.authorLastName, form.source.year)
            result += '\n\t\t\\item %s(%s)' % (source, 'OLD ID: %s' % form.id)
        else:
            result += '\n\t\t\\item (%s%s)' % (
                dateElicited, 'OLD ID: %s' % form.id)
    result += '\n\t\\end{itemize}'

    return result


################################################################################
############## Define Exporters Here
################################################################################


e1 = Exporter()
e1.name = u'transcription only'
e1.description = u"""Plain text export.  Outputs a string of
newline-delimited Form transcriptions (prefixed with grammaticalities)."""
e1.inputTypes = formListInputTypes
e1.extension = 'txt'

def exporterFunction(input):
    formList = getFormList(input)
    return '\n'.join([plainTextTranscription(x) for x in formList])

e1.exporterFunction = exporterFunction


e2 = Exporter()
e2.name = u'transcription and gloss'
e2.description = u"""Plain text export.  Outputs Forms as newline-separated
transcription-gloss pairs.  These pairs are separated by double newlines."""
e2.inputTypes = formListInputTypes
e2.extension = 'txt'

def exporterFunction(input):
    formList = getFormList(input)
    return '\n\n'.join([plainTextTranscriptionGlossNewline(x) for x in formList])

e2.exporterFunction = exporterFunction


e3 = Exporter()
e3.name = u'interlinear gloss text'
e3.description = u"""Plain text export.  Outputs Forms as newline-separated
quadruples consisting of: (1) transcription, (2) morpheme break, (3) morpheme
gloss and (4) gloss(es).  These quadruples are separated by double newlines."""
e3.inputTypes = formListInputTypes
e3.extension = 'txt'

def exporterFunction(input):
    formList = getFormList(input)
    return '\n\n'.join([plainTextIGT(x) for x in formList])

e3.exporterFunction = exporterFunction


e4 = Exporter()
e4.name = u'interlinear gloss text +'
e4.description = u"""Plain text export.  Outputs Forms as newline-separated
septuples consisting of: (1) transcription, (2) morpheme break, (3) morpheme
gloss, (4) gloss(es), (5) comments, (6) speaker comments (7) ID reference.  The
ID reference is the date elicited (if specified) followed by the Form ID.  These
septuples are separated by double newlines."""
e4.inputTypes = formListInputTypes
e4.extension = 'txt'

def exporterFunction(input):
    formList = getFormList(input)
    return '\n\n'.join(['%s\n%s' % (
        plainTextIGT(x), secondaryData(x)) for x in formList])

e4.exporterFunction = exporterFunction


e5 = Exporter()
e5.name = u'tab-delimited: everything'
e5.description = u"""Plain text export.  Each Form is output on its own line
with tabs delimiting each field.  This format can be opened by a spreadsheet
program like OpenOffice.org Calc or Microsoft Excel."""
e5.inputTypes = formListInputTypes
e5.extension = 'txt'

def exporterFunction(input):
    formList = getFormList(input)
    headers = u'\t'.join(
        [
            'ID',
            'transcription',
            'morpheme break',
            'morpheme gloss',
            'gloss(es)',
            'comments',
            'speaker comments',
            'date elicited',
            'date and time entered',
            'date and time modified',
            'category string',
            'elicitor',
            'enterer',
            'verifier',
            'speaker',
            'elicitation method',
            'category',
            'source',
            'keywords'
        ]
    )
    return '%s\n%s' % (headers, '\n'.join([allTabDelimited(x) for x in formList]))

e5.exporterFunction = exporterFunction


e6 = Exporter()
e6.name = u'XeLaTeX IGT (Covington)'
e6.description = u"""XeLaTeX export.  Outputs Forms in IGT format using the LaTeX
package Covington to format the interlinear gloss text so that words are nicely
aligned.  The representation of the Form contains the following fields: (1)
transcription, (2) morpheme break, (3) morpheme gloss and (4) gloss(es). (Note:
XeLaTeX is just like LaTeX except that it recognizes unicode characters.  The
file generated using this option is, like all others, encoded as UTF-8.  Also,
this option assumes the user has the Aboriginal Serif font installed.  If you,
do not have this font, change the '\setmainfont{Aboriginal Serif}' declaration
so that it references a font you do have and which will render the characters
of your language's orthography.)"""
e6.inputTypes = formListInputTypes
e6.extension = 'tex'

def exporterFunction(input):
    formList = getFormList(input)
    result = '\\documentclass{article}\n\n%s' % h.xelatexCovingtonPreamble
    result += u'\n\n\\begin{document}\n\n\\title{OLD Export}\n\\author{' + \
            session['user_firstName'] + u' ' + session['user_lastName'] + \
            '}\n\\maketitle\n\n'
    result += u'\n\n'.join(['\\begin{examples}\n%s\n\\end{examples}' % \
                            xelatexCovington(x) for x in formList])
    result += u'\n\n\\end{document}'
    return result

e6.exporterFunction = exporterFunction


e7 = Exporter()
e7.name = u'XeLaTeX IGT (Covington) +'
e7.description = u"""XeLaTeX export.  Same as 'XeLaTeX IGT (Covington)'
except that the comments and speaker comments fields (if present) are
included as items of a list beneath each Form."""
e7.inputTypes = formListInputTypes
e7.extension = 'tex'

def exporterFunction(input):
    formList = getFormList(input)
    result = '\\documentclass{article}\n\n%s' % h.xelatexCovingtonPreamble
    result += u'\n\n\\begin{document}\n\n\\title{OLD Export}\n\\author{' + \
            session['user_firstName'] + u' ' + session['user_lastName'] + \
            '}\n\\maketitle\n\n'
    result += u'\n\n'.join(['\\begin{examples}\n%s\n%s\n\\end{examples}' % (
        xelatexCovington(x), xelatexSecondaryData(x, False)) for x in formList])
    result += u'\n\n\\end{document}'
    return result

e7.exporterFunction = exporterFunction


e8 = Exporter()
e8.name = u'XeLaTeX IGT (Covington) ++'
e8.description = u"""XeLaTeX export.  Same as 'XeLaTeX IGT (Covington) +'
except that beneath any comments or speaker comments items is a an item
containing a reference to the Form.  This reference is the speaker's initials
followed by the date elicited and the Form's ID.  If there is no speaker, but
there is a source, then a reference to the source takes the place of the
speaker's initials."""
e8.inputTypes = formListInputTypes
e8.extension = 'tex'

def exporterFunction(input):
    formList = getFormList(input)
    result = '\\documentclass{article}\n\n%s' % h.xelatexCovingtonPreamble
    result += u'\n\n\\begin{document}\n\n\\title{OLD Export}\n\\author{' + \
            session['user_firstName'] + u' ' + session['user_lastName'] + \
            '}\n\\maketitle\n\n'
    result += u'\n\n'.join(['\\begin{examples}\n%s\n%s\n\\end{examples}' % (
        xelatexCovington(x), xelatexSecondaryData(x)) for x in formList])
    result += u'\n\n\\end{document}'
    return result

e8.exporterFunction = exporterFunction


e9 = Exporter()
e9.name = u'XeLaTeX Report'
e9.description = u"""XeLaTeX export.  Assumes the input is reStructuredText.
Uses docutils.core to convert the RST to LaTeX."""
e9.inputTypes = collectionContentInputType
e9.extension = 'tex'

def exporterFunction(input):
    
    def getFormFromListOfForms(formsList, matchObj):
        """Input is a list of Forms and a re Match object.  (The formId will be
        recoverable as the first backreference of the Match object.)  The output
        is the Form in the list whose ID is the ID extracted from the matchObj
        
        """
        formId = int(matchObj.group(1))
        try:
            return [x for x in formsList if x.id == formId][0]
        except IndexError:
            return None
    
    # Get the Collection's contents data
    collection = getCollection(input)
    content = collection.contents
    
    # Convert to LaTeX (actually, a hacky XeLaTeX-processable document)
    content = h.rst2latex(content)
    
    # Insert a title into the (Xe)LaTeX string
    dateModified = collection.datetimeModified.strftime('%b %d, %Y')
    title = '\\title{%s}\n\\author{\\textit{entered by:} %s \\\\ \n \
        \\textit{exported by:} %s} \n\\date{%s}\n\\maketitle' % (
            collection.title,
            '%s %s' % (collection.enterer.firstName, collection.enterer.firstName),
            '%s %s' % (session['user_firstName'], session['user_lastName']),
            dateModified
        )
    content = content.replace('\\begin{document}', '\\begin{document}\n\n%s' % \
                              title)

    # Replace Form references with Covington-styled IGT examples
    patt = re.compile('form\{\[\}([0-9]+)\{\]\}')
    return patt.sub(lambda x: '\n\n\\begin{examples}\n%s\n\\end{examples}' \
        % xelatexCovington(getFormFromListOfForms(collection.forms, x)), content)

e9.exporterFunction = exporterFunction


################################################################################
############## Global exporters variable
######## This is imported by the export controller
################################################################################


exporters = [e1, e2, e3, e4, e5, e6, e7, e8, e9]