# vi: coding=utf-8

from euphorie.deployment.tests.functional import EuphorieTestCase


class PublicationTests(EuphorieTestCase):
    def afterSetUp(self):
        super(PublicationTests, self).afterSetUp()
        self.loginAsPortalOwner()
        self.client=self.portal.client

    def createSurvey(self):
        self.portal.sectors.nl.invokeFactory("euphorie.sector", "dining",
                title=u"Fine dining®")
        self.sector=self.portal.sectors.nl.dining
        self.sector.invokeFactory("euphorie.surveygroup", "survey", title=u"Survey")
        self.surveygroup=self.sector.survey
        self.surveygroup.invokeFactory("euphorie.survey", "version1", title=u"Version 1")
        self.survey=self.surveygroup.version1
        return self.survey

    def testPublishEmptySurvey(self):
        self.createSurvey()
        view=self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(self.client.objectIds(), ["nl"])
        self.assertEqual(self.client.nl.objectIds(), ["dining"])
        sector=self.client.nl.dining
        self.assertEqual(sector.portal_type, "euphorie.clientsector")
        self.assertEqual(sector.Title(), u"Fine dining®")
        survey=sector.survey
        self.assertEqual(survey.portal_type, "euphorie.survey")
        self.assertEqual(survey.title, u"Survey")
        self.assertEqual(survey.objectIds(), [])

    def testPublishSurveyWithQuestion(self):
        self.createSurvey()
        modid=self.survey.invokeFactory("euphorie.module", "module")
        module=getattr(self.survey, modid)
        qid=module.invokeFactory("euphorie.risk", "risk",
                title=u"Do you offer take away?")
        view=self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(self.client.nl.objectIds(), ["dining"])
        survey=self.client.nl.dining.survey
        self.assertEqual(survey.objectIds(), [modid])
        self.assertEqual(getattr(survey,modid).objectIds(), [qid])

    def testPublishRemovesExistingObject(self):
        self.createSurvey()
        self.client.invokeFactory("euphorie.clientcountry", "nl")
        self.client.nl.invokeFactory("euphorie.clientsector", "dining")
        self.client.nl.dining.invokeFactory("euphorie.survey", "survey")
        self.client.nl.dining.survey.old_object=True
        view=self.survey.restrictedTraverse("@@publish")
        view.publish()
        self.assertEqual(getattr(self.client.nl.dining, "old_object", False), False)



class PreviewTests(EuphorieTestCase):
    def testPreviewGetsCorrectUrl(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/95
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        self.loginAsPortalOwner()
        sector=createSector(self.portal)
        survey=addSurvey(sector)
        view=survey.restrictedTraverse("@@preview")
        preview=view.publish()
        self.assertEqual(preview.id, "preview")
        self.assertEqual(preview.absolute_url(), "http://nohost/plone/client/nl/sector/preview")

