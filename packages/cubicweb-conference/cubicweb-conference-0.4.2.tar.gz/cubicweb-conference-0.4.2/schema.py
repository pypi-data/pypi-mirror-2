from yams.buildobjs import EntityType, String, Date, SubjectRelation, Datetime,\
    ObjectRelation, RichString, RelationType, RelationDefinition
from yams.constraints import SizeConstraint
from cubicweb.schema import ERQLExpression, RRQLExpression, WorkflowableEntityType, RQLVocabularyConstraint
from cubicweb.schemas.base import CWUser

CWUser.add_relation(SubjectRelation('Talk', cardinality='*1', constraints=[
            RQLVocabularyConstraint('S in_group G, G name "users"')]), name='leads')

CWUser.add_relation(SubjectRelation('Talk', cardinality='**'), name='attend')

CWUser.add_relation(String(), name='representing')
CWUser.__permissions__['read'] = ('managers', 'users', 'guests')

class Conference(WorkflowableEntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    ('managers', ),
        'update': ('managers', 'owners',),
        'delete': ('managers', 'owners',),
        }
    title = String(maxsize=50, required=True, fulltextindexed=True)
    start_on = Date(default='TODAY', required=True)
    end_on = Date(default='TODAY', required=True)
    description = RichString(fulltextindexed=True)

class Track(EntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    ('managers', ),
        'update': ('managers', 'owners',),
        'delete': ('managers', 'owners',),
        }
    title = String(maxsize=50, required=True, fulltextindexed=True)
    description = RichString(fulltextindexed=True)

class Talk(WorkflowableEntityType):
    __permissions__ = {
        'read':   ('managers',
                   ERQLExpression('X owned_by U'),
                   ERQLExpression('U reviews X, X in_state ST, '
                                  'ST name in ("correction", "inreview", "rejected")'),
                   ERQLExpression('X in_state ST, ST name "accepted"'),
                   ),
        'add':    ('managers', 'users',),
        'update': ('managers', ERQLExpression('X in_state ST, ST name in ("draft", "correction"), X owned_by U')),
        'delete': ('managers', ),
        }
    title = String(maxsize=100, required=True, fulltextindexed=True)
    description = RichString(fulltextindexed=True)
    comments = ObjectRelation('Comment', cardinality='1*',)
    start_time = Datetime(__permissions__={
        'read':   ('managers', 'users', 'guests',),
        'update':    ('managers',),
        })
    end_time = Datetime(__permissions__={
        'read':   ('managers', 'users', 'guests',),
        'update':    ('managers',),
        })

class location(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests',),
        'update': ('managers',)
        }
    subject = 'Talk'
    object = 'String'
    cardinality = '?1'
    constraints=[SizeConstraint(100)]

class in_track(RelationDefinition):
     __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add':    ('managers', 'users', RRQLExpression('S owned_by U'),),
        'delete': ('managers', 'users', RRQLExpression('S owned_by U'),)
        }
     subject = 'Talk'
     object = 'Track'
     cardinality = '+*'

class has_attachments(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add':  ('managers', RRQLExpression('S owned_by U')),
        'delete':  ('managers', RRQLExpression('S owned_by U'))
        }
    subject = 'Talk'
    object = ('File','Image')
    cardinality = '*1'

class tags(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add':  ('managers', 'users'),
        'delete':  ('managers', 'users')
        }
    subject = 'Tag'
    object = 'Talk'

class in_conf(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    ('managers', 'users', RRQLExpression('S owned_by U'),),
        'delete': ('managers', 'users', RRQLExpression('S owned_by U'),)
        }
    subject = ('Track', 'Talk',)
    object = 'Conference'
    cardinality = '1*'

class reviews(RelationDefinition):
    __permissions__ = {
        'read': ('managers',),
        'add': ('managers',),
        'delete': ('managers',),
        }
    subject = ('CWUser',)
    object = 'Talk'
    cardinality = '**'

class Sponsor(EntityType):
    __permissions__ = {
        'read': ('managers', 'users', 'guests',),
        'add': ('managers',),
        'update': ('managers', 'owners',),
        'delete': ('managers', 'owners',),
        }
    title = String(maxsize=100, required=True, fulltextindexed=True)
    description = RichString(fulltextindexed=True)
    url = String(maxsize=100)

class SponsorShip(EntityType):
    __permissions__ = {
        'read': ('managers', 'users', 'guests',),
        'add': ('managers',),
        'update': ('managers', 'owners',),
        'delete': ('managers', 'owners',),
        }
    title = String(maxsize=100, required=True, fulltextindexed=True)
    level = String(vocabulary=('Gold', 'Silver', 'Bronze', 'Media'))

class sponsoring_conf(RelationType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    ('managers', RRQLExpression('S owned_by U'),),
        'delete': ('managers', RRQLExpression('S owned_by U'),)
        }
    subject = ('SponsorShip',)
    object = 'Conference'
    cardinality = '+*'

class has_logo(RelationType):
    subject = ('Sponsor',)
    object = 'Image'
    cardinality = '1*'
    composite = 'subject'

class is_sponsor(RelationType):
    subject = ('Sponsor',)
    object = ('SponsorShip',)
    cardinality = '**'
