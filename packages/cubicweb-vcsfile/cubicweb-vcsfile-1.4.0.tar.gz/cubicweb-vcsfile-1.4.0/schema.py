"""entity types used to represent a version control system (vcs) content

:organization: Logilab
:copyright: 2007-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from yams.buildobjs import (DEFAULT_ATTRPERMS,
                            EntityType, RelationDefinition, SubjectRelation,
                            String, Int, Bytes)

PRIVATE_ATTRPERMS = DEFAULT_ATTRPERMS.copy()
PRIVATE_ATTRPERMS['read'] = ('managers', 'users')


class Repository(EntityType):
    """a local subversion repository which will be used as versionned content
    entity source
    """
    __permissions__ = {
        'read':   ('managers', 'users', 'guests'),
        'add':    ('managers',),
        'update': ('managers',),
        'delete': ('managers',),
        }
    title = String(description=_('optional title. If the repository has a public url, '
                                 'it may be a good idea to put it as title.'))
    type = String(required=True, vocabulary=('subversion', 'mercurial'),
                  description=_('repository\'s type'))
    path = String(required=True, unique=True,
                  description=_('path to the repository'),
                  __permissions__=PRIVATE_ATTRPERMS)
    subpath = String(description=_('if specified, only import the given subpart'
                                   ' of the repository (path relative to the '
                                   'repository root)'))
    encoding = String(default='utf-8', maxsize=20, required=True,
                      description=_('encoding used for the repository (e.g.'
                                    ' for file path and check-in comments)'))


class Revision(EntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests'),
        'add':    ('managers', 'users',),
        'update': ('managers', 'owners'),
        'delete': (),
        }
    # NOTE: creation_date will be set at revision date
    revision = Int(required=True, indexed=True,
                   description=_('revision number.'))

    description = String(description=_('comment for this revision.'))

    author = String(indexed=True, maxsize=200,
                    description=_("author of this revision."))

    changeset = String(indexed=True, maxsize=100,
                       description=_('change set identifier, when used by the '
                                     'underlying version control system.'))

    branch = String(indexed=True, maxsize=255,
                    description=_("branch of this revision."))
    # XXX tags

    parent_revision = SubjectRelation('Revision')


class VersionedFile(EntityType):
    """a file stored in a versioned source"""
    __permissions__ = {
        'read':   ('managers', 'users', 'guests'),
        'add':    ('managers', 'users',),
        'update': (),
        'delete': (),
        }
    directory = String(required=True, indexed=True,
                       description=_('directory of the file in the repository.'))
    name = String(required=True,                   description=_('name of the file in the repository.'))


class DeletedVersionContent(EntityType):
    """represent a revision where a versioned file has been deleted"""
    __permissions__ = {
        'read':   ('managers', 'users', 'guests'),
        'add':    ('managers', 'users',),
        'update': ('managers', 'owners'),
        'delete': (),
        }


class VersionContent(DeletedVersionContent):
    """actual content of a versioned file, for a given revision"""
    data = Bytes(description=_("file's data"), required=True)
    data_format = String(required=True, meta=True, maxsize=50,
                         description=_('MIME type of the file.'))
    data_encoding = String(meta=True, maxsize=20,
                           description=_('encoding of the file when it applies (e.g. text).'))


class from_repository(RelationDefinition):
    inlined = True
    subject = ('Revision', 'VersionedFile')
    object = 'Repository'
    cardinality = '1*'
    composite = 'object'

class content_for(RelationDefinition):
    inlined = True
    subject = ('DeletedVersionContent', 'VersionContent')
    object = 'VersionedFile'
    composite = 'object'
    cardinality = '1*'

class from_revision(RelationDefinition):
    inlined = True
    subject = ('DeletedVersionContent', 'VersionContent')
    object = 'Revision'
    cardinality = '1*'
    composite = 'object'

class at_revision(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests'),
        'add':    (),
        'delete': (),
        }
    subject = ('DeletedVersionContent', 'VersionContent')
    object = 'Revision'

class vc_copy(RelationDefinition):
    inlined = True
    subject = object = 'VersionContent'
    cardinality = '?*'

class vc_rename(RelationDefinition):
    inlined = True
    subject = object = 'VersionContent'
    cardinality = '?*'
