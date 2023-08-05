from base import getToolByName, TestCase
from config import *

from testQPloneCommentsCommenting import TestCommBase
from zExceptions import Unauthorized

USERS = {# Common Members
         'admin':{'passw': 'secret_admin', 'roles': ['Manager']},
         'owner':{'passw': 'secret_owner', 'roles': ['Owner']},
         'member':{'passw': 'secret_member', 'roles': ['Member']},
         'reviewer':{'passw': 'secret_reviewer', 'roles': ['Reviewer']},
         # Members for discussion manager group
         'dm_admin':{'passw': 'secret_dm_admin', 'roles': ['Manager']},
         'dm_owner':{'passw': 'secret_dm_owner', 'roles': ['Owner']},
         'dm_member':{'passw': 'secret_dm_member', 'roles': ['Member']},
         'dm_reviewer':{'passw': 'secret_dm_reviewer', 'roles': ['Reviewer']},
        }
COMMON_USERS_IDS = [u for u in USERS.keys() if not u.startswith('dm_')]
COMMON_USERS_IDS.append('anonym')
DM_USERS_IDS = [u for u in USERS.keys() if u.startswith('dm_')]


class TestReportAbuse(TestCommBase):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)
        self.testAnonymousReportAbuse()
        self.testAuthenticatedReportAbuse()

    def testAnonymousReportAbuse(self):
        self.login('dm_admin')
        doc_obj = getattr(self.portal, "doc_anonym")
        discussion = self.discussion.getDiscussionFor(doc_obj)
        comment = discussion._container.values()[0]
        self.logout()
        # Add abuse report on document.
        doc_obj.REQUEST.set('comment_id', comment.id)
        try:
            doc_obj.report_abuse("Anonymous Report Abuse") 
        except:
            raise "Anonymous user CAN'T report abuse in turned ON *Anonymous report abuse mode*."


    def testAuthenticatedReportAbuse(self):
        not_anonym_users = [u for u in self.all_users_id if not u=='anonym']
        failed_users = []
        for u in not_anonym_users:
            self.login('dm_admin')
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            discussion = self.discussion.getDiscussionFor(doc_obj)
            comment = discussion._container.values()[0]
            doc_obj.REQUEST.set('comment_id', comment.id)
            self.login(u)
            try:
                doc_obj.report_abuse("Anonymous Report Abuse") 
            except:
                failed_users.append(u)

        self.assert_(not failed_users, "%s - user(s) can not report abuse" % failed_users)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestReportAbuse))
    return suite
