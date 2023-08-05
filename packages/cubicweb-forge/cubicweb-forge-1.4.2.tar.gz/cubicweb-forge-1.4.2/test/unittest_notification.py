"""Forge hooks tests"""
import re

from cubicweb.devtools.testlib import MAILBOX
from cubes.tracker.testutils import TrackerBaseTC

class NotificationTC(TrackerBaseTC):

    def setUp(self):
        super(NotificationTC, self).setUp()
        # XXX should be done in devtools
        assert self.execute('INSERT EmailAddress E: E address "admin@cwo", U primary_email E '
                            'WHERE U login "admin"')

    def test_notifications(self):
        p = self.create_project('hop').get_entity(0, 0)
        b = self.create_ticket('one more', pname='hop').get_entity(0, 0)
        self.execute('INSERT Comment X: X content "duh? explain", X comments B '
                     'WHERE B title "one more"')
        b.set_attributes(priority=u'important')
        self.commit()
        self.assertEquals([re.sub('#\d+', '#EID', e.subject) for e in MAILBOX],
                          ['[data] New Project: hop',
                           '[data] New Project: hop', # see below
                           '[hop] New Ticket #EID: one more',
                           '[hop] new comment for ticket #EID: one more',
                           ])
        # test that for new project, recipients are the nosy list (eg creator)
        # *and* default recipients
        self.assertEquals(MAILBOX[0].recipients, ['admin@cwo'])
        self.assertEquals(MAILBOX[1].recipients, self.config['default-dest-addrs'])
        # but only nosy list for tickets / comments
        self.assertEquals(MAILBOX[2].recipients, ['admin@cwo'])
        self.assertEquals(MAILBOX[3].recipients, ['admin@cwo'])
        # check that other notification when project isn't being created are
        # using regulary nosy list recipients
        MAILBOX[:] = ()
        p.fire_transition('temporarily stop development')
        self.commit()
        self.assertEquals([re.sub('#\d+', '#EID', e.subject) for e in MAILBOX],
                          ['[hop] project is now in state "asleep"',
                           ])
        self.assertEquals(MAILBOX[0].recipients, ['admin@cwo'])

    def test_nosy_list_propagation(self):
        self.create_user('logilabien')
        self.execute('INSERT EmailAddress X: X address "logilabien@logilab.org", U primary_email X WHERE U login "logilabien"')
        self.execute('SET U interested_in X WHERE X name "cubicweb", U login "logilabien"')
        self.commit()
        ticket = self.create_ticket('ticket').get_entity(0, 0)
        self.commit()
        self.assertEquals(len(MAILBOX), 2)
        MAILBOX.sort(key=lambda x: x.recipients)
        self.assertEquals(MAILBOX[0].subject, '[cubicweb] New Ticket #%s: ticket' % ticket.eid)
        self.assertEquals(MAILBOX[0].recipients, ['admin@cwo'])
        self.assertEquals(MAILBOX[1].subject, '[cubicweb] New Ticket #%s: ticket' % ticket.eid)
        self.assertEquals(MAILBOX[1].recipients, ['logilabien@logilab.org'])


