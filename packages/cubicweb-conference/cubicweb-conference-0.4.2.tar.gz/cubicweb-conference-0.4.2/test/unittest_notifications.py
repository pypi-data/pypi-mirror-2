from datetime import date
from logilab.common.testlib import unittest_main
from cubicweb.devtools.testlib import CubicWebTC, MAILBOX

class TalkNotification(CubicWebTC):
    def setup_database(self):
        self.vreg.config['default-recipients-mode'] = 'users'
        self.create_user(u'test_user')
        self.create_user(u'test_reviewer')
        self.create_user(u'test_admin')
        self.execute('INSERT EmailAddress E: E address "test_user@logilab.fr",'
                           'U use_email E WHERE U login "test_user"')
        self.execute('INSERT EmailAddress E: E address "test_reviewer@logilab.fr",'
                           'U use_email E WHERE U login "test_reviewer"')
        self.execute('INSERT EmailAddress E: E address "test_admin@logilab.fr",'
                           'U use_email E WHERE U login "test_admin"')
        self.conf = self.request().create_entity(u'Conference',
                                                 title = u'conference test',
                                                 start_on = date(2010,3,1).strftime('%Y/%m/%d'),
                                                 end_on = date(2010,3,5).strftime('%Y/%m/%d'),
                                                 description = u'short description')
        self.track = self.request().create_entity(u'Track',
                                                  title = u'track test',
                                                  description = u'short track description',
                                                  in_conf = self.conf)
        self.commit()

    def test_add_talk(self):
        MAILBOX[:] = []
        self.talk = self.request().create_entity(u'Talk',
                                                 title = u'Test talk title',
                                                 in_track = self.track)
        self.commit()
        self.assertEquals(len(MAILBOX), 0)
        self.execute('SET X in_group N WHERE X is CWUser, X login "test_admin", N name "managers"')
        self.talk2 = self.request().create_entity(u'Talk',
                                                 title = u'Test talk title 2',
                                                 in_track = self.track)
        self.commit()
        self.assertEquals(len(MAILBOX), 1)
        self.assertEquals(MAILBOX[0].recipients, ['test_admin@logilab.fr'])
        self.assertEquals(MAILBOX[0].subject, '[conference test] a talk was added.')

    def test_update_talk(self):
        MAILBOX[:] = []
        self.talk = self.request().create_entity(u'Talk',
                                                 title = u'Test talk title',
                                                 in_track = self.track)
        self.commit()
        self.assertEquals(len(MAILBOX), 0)
        self.execute('SET X title "new title 1" WHERE X eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.commit()
        self.assertEquals(len(MAILBOX), 0)
        self.execute('SET X in_group N WHERE X is CWUser, X login "test_admin", N name "managers"')
        self.execute('SET X title "new title 2" WHERE X eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.commit()
        self.assertEquals(len(MAILBOX), 1)
        MAILBOX[:] = []
        self.execute('SET X reviews Y WHERE X is CWUser, X login "test_reviewer", Y eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.execute('SET X leads Y WHERE X is CWUser, X login "test_user", Y eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.execute('SET X title "new title 3" WHERE X eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.commit()
        self.assertEquals(len(MAILBOX), 3)
        MAILBOX.sort(key=lambda x: x.recipients)
        self.assertEquals([i.recipients[0] for i in MAILBOX[0:3]], ['test_admin@logilab.fr',
                                                                 'test_reviewer@logilab.fr',
                                                                 'test_user@logilab.fr'])
    def test_status_talk(self):
        MAILBOX[:] = []
        self.talk = self.request().create_entity(u'Talk',
                                                 title = u'Test talk title',
                                                 in_track = self.track)
        self.execute('SET X in_group N WHERE X is CWUser, X login "test_admin", N name "managers"')
        self.execute('SET X reviews Y WHERE X is CWUser, X login "test_reviewer", Y eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.execute('SET X leads Y WHERE X is CWUser, X login "test_user", Y eid %(eid)s',
                     {'eid': self.talk.eid, })
        self.commit()
        self.talk.change_state('draft')
        self.commit()
        rset = self.execute('Any X, S WHERE X eid %(eid)s, X in_state S',
                            {'eid': self.talk.eid, })
        MAILBOX[:] = []
        self.talk.fire_transition('draft')
        self.commit()
        rset = self.execute('Any X, S WHERE X eid %(eid)s, X in_state S',
                            {'eid': self.talk.eid, })
        self.assertEquals(MAILBOX[0].message.get('Subject'),
                          '[conference test] talk status was updated')
        self.assertEquals(len(MAILBOX), 3)


