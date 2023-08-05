# Copyright (c) 2009 Assembly Organizing
# See also LICENSE.txt

import asm.cms.interfaces
import datetime
import grok
import pytz
import zope.component
import zope.event


WORKFLOW_PUBLIC = 'workflow:public'
WORKFLOW_DRAFT = 'workflow:draft'

WORKFLOW_LABELS = {WORKFLOW_PUBLIC: 'Public',
                   WORKFLOW_DRAFT: 'Draft'}


class WorkflowLabels(grok.GlobalUtility):

    zope.interface.implements(asm.cms.interfaces.IEditionLabels)
    grok.name('workflow')

    def lookup(self, tag):
        return WORKFLOW_LABELS[tag]


class Prefixes(object):

    zope.interface.implements(asm.cms.interfaces.IExtensionPrefixes)

    prefixes = set(['workflow'])


def publish(current_edition, publication_date=None):
    draft = current_edition.parameters.replace(WORKFLOW_PUBLIC, WORKFLOW_DRAFT)
    draft = current_edition.page.getEdition(draft)
    public = draft.parameters.replace(WORKFLOW_DRAFT, WORKFLOW_PUBLIC)
    public = draft.page.getEdition(public, create=True)
    public.copyFrom(draft)
    public.modified = (
        publication_date or datetime.datetime.now(tz=pytz.UTC))
    zope.event.notify(asm.workflow.interfaces.PublishedEvent(draft, public))
    # And now remove the draft after publication.
    del draft.__parent__[draft.__name__]
    return public


def select_initial_parameters():
    return set([WORKFLOW_DRAFT])


class CMSEditionSelector(object):

    zope.interface.implements(asm.cms.IEditionSelector)
    zope.component.adapts(asm.cms.IPage, asm.cms.ICMSSkin)

    def __init__(self, page, request):
        self.preferred = []
        self.acceptable = []
        for edition in page.editions:
            if WORKFLOW_DRAFT in edition.parameters:
                self.preferred.append(edition)
            else:
                self.acceptable.append(edition)


class RetailEditionSelector(object):

    zope.interface.implements(asm.cms.IEditionSelector)
    zope.component.adapts(
        asm.cms.IPage,
        asm.cms.interfaces.IRetailSkin)

    acceptable = ()

    def __init__(self, page, request):
        self.preferred = []
        for edition in page.editions:
            if WORKFLOW_PUBLIC in edition.parameters:
                self.preferred.append(edition)


class PublishMenuItem(grok.Viewlet):
    grok.viewletmanager(asm.cms.PageActionGroups)
    grok.context(asm.cms.IEdition)

    def current_version(self):
        for candidate in self.context.parameters:
            if candidate.startswith('workflow:'):
                return WORKFLOW_LABELS[candidate]

    def is_draft(self):
        return WORKFLOW_DRAFT in self.context.parameters

    def is_public(self):
        return WORKFLOW_PUBLIC in self.context.parameters

    def has_draft(self):
        try:
            draft = self.context.parameters.replace(
                'workflow:*', WORKFLOW_DRAFT)
            self.context.page.getEdition(draft)
        except KeyError:
            return False
        return True

    def has_public(self):
        try:
            draft = self.context.parameters.replace(
                'workflow:*', WORKFLOW_PUBLIC)
            self.context.page.getEdition(draft)
        except KeyError:
            return False
        return True

    def hints(self):
        hints = ''
        public_p = self.context.parameters.replace(
            'workflow:*', WORKFLOW_PUBLIC)
        try:
            public = self.context.page.getEdition(public_p)
        except KeyError:
            hints += 'No public version available. '
        else:
            try:
                draft = self.context.page.getEdition(
                    public_p.replace('workflow:*', WORKFLOW_DRAFT))
            except KeyError:
                pass
            else:
                if draft is self.context:
                    hints += 'Public version available. '
                if draft.modified > public.modified:
                    hints + 'Draft is newer.'
        return hints

    def list_versions(self):
        for status in [WORKFLOW_DRAFT, WORKFLOW_PUBLIC]:
            p = self.context.parameters.replace('workflow:*', status)
            version = {}
            version['class'] = ''
            version['label'] = WORKFLOW_LABELS[status]
            try:
                version['edition'] = self.context.page.getEdition(p)
            except KeyError:
                continue

            if version['edition'] is self.context:
                version['class'] = 'selected'

            yield version


class Publish(asm.cms.ActionView):

    grok.context(asm.cms.IEdition)

    def update(self):
        self.context = publish(self.context)
        self.redirect(self.url(self.context, '@@edit'))
        self.flash(u"Published draft.")


class DeletePublic(asm.cms.ActionView):

    grok.context(asm.cms.IEdition)
    grok.name('delete-public')

    def update(self):
        page = self.context.page
        public = self.context.parameters.replace(
            WORKFLOW_DRAFT, WORKFLOW_PUBLIC)
        try:
            public = page.getEdition(public)
        except KeyError:
            self.flash(u"No public version to delete.")
            return

        draft = self.context.parameters.replace(
            WORKFLOW_PUBLIC, WORKFLOW_DRAFT)
        try:
            draft = page.getEdition(draft)
        except KeyError:
            self.flash(u"Can not delete public version without draft.")
            return

        del public.__parent__[public.__name__]
        self.flash(u'Deleted public version.')
        self.redirect(self.url(draft, '@@edit'))


class DeleteDraft(asm.cms.ActionView):

    grok.context(asm.cms.IEdition)
    grok.name('delete-draft')

    def update(self):
        page = self.context.page
        draft = self.context.parameters.replace(
            WORKFLOW_PUBLIC, WORKFLOW_DRAFT)
        try:
            draft = page.getEdition(draft)
        except KeyError:
            self.flash(u"No draft version to delete.")
            return

        public = self.context.parameters.replace(
            WORKFLOW_DRAFT, WORKFLOW_PUBLIC)
        try:
            public = page.getEdition(public)
        except KeyError:
            self.flash(u"Can not delete draft without public version.")
            return

        del draft.__parent__[draft.__name__]
        self.flash(u'Deleted draft version.')
        self.redirect(self.url(public, '@@edit'))


class CreateDraft(asm.cms.ActionView):
    """Create (or update) a draft by copying the current state of the published
    edition to the draft object.

    This action view can be applied either on the draft or the public copy with
    the same result.

    """

    grok.context(asm.cms.IEdition)
    grok.name('create-draft')

    def update(self):
        page = self.context.page
        public = self.context.parameters.replace(
            WORKFLOW_DRAFT, WORKFLOW_PUBLIC)
        try:
            public = page.getEdition(public)
        except KeyError:
            self.flash(u"Cannot revert because no public edition exists.")
            return

        draft = public.parameters.replace(WORKFLOW_PUBLIC, WORKFLOW_DRAFT)
        draft = page.getEdition(draft, create=True)
        draft.copyFrom(public)
        self.flash(u"Copied data from public version to draft.")
        self.redirect(self.url(draft, '@@edit'))
