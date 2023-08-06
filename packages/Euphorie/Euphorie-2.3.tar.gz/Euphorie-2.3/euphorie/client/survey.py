"""
Survey views
============
"""

import logging
import random
import Acquisition
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from zExceptions import NotFound
from five import grok
from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy
from zope.component import adapts
from zope.i18n import translate
from z3c.saconfig import Session
from sqlalchemy import sql
from plone.memoize.instance import memoize
from euphorie.content.survey import ISurvey
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client.session import SessionManager
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client import model
from euphorie.client import utils
from euphorie.client import MessageFactory as _
from ZPublisher.BaseRequest import DefaultPublishTraverse
import OFS.Traversable


log = logging.getLogger(__name__)

grok.templatedir("templates")

class PathGhost(OFS.Traversable.Traversable, Acquisition.Implicit):
    """Dummy object to fake a traversable element.

    This object is inserted into the acquisition chain by
    :py:class:`SurveyPublishTraverser` when it needs to add components
    to the acquisition chain when no corresponding object in the
    ZODB or SQL databsae exists.
    """

    def __init__(self, id):
        self.id=id

    def getId(self):
        return self.id



class View(grok.View):
    """
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("survey_sessions")
    grok.name("index_html")


    def sessions(self):
        """Return a list of all sessions for the current user. For each
        session a dictionary is returned with the following keys:

        * `id`: unique identifier for the session
        * `title`: session title
        * `modified`: timestamp of last session modification
        """
        survey=aq_inner(self.context)
        my_path=utils.RelativePath(self.request.client, survey)
        account=getSecurityManager().getUser()
        return [dict(id=session.id,
                     title=session.title,
                     modified=session.modified)
                 for session in account.sessions
                 if session.zodb_path==my_path]



    def _NewSurvey(self, info):
        """Utility method to start a new survey session."""
        survey=aq_inner(self.context)
        title=info.get("title", u"").strip()
        if not title:
            title=survey.Title()

        SessionManager.start(title=title, survey=survey)
        self.request.response.redirect("%s/start" % survey.absolute_url())



    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session=Session.query(model.SurveySession).get(info["session"])
        SessionManager.resume(session)
        survey=self.request.client.restrictedTraverse(str(session.zodb_path))
        self.request.response.redirect("%s/resume" % survey.absolute_url())


    def update(self):
        utils.setLanguage(self.request, self.context)

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            if reply["action"]=="new":
                self._NewSurvey(reply)
            elif reply["action"]=="continue":
                self._ContinueSurvey(reply)
        else:
            survey=aq_inner(self.context)
            dbsession=SessionManager.session
            if dbsession is not None and \
                    dbsession.zodb_path==utils.RelativePath(self.request.client, survey):
                self.request.response.redirect("%s/resume" % survey.absolute_url())




class Start(grok.View):
    """Survey start screen.

    This view shows basic introduction text and any extra information provided
    the sector if present. After viewing this page the user is forwarded to the
    profile page.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("start")
    grok.name("start")

    @memoize
    def has_introduction(self):
        survey=aq_inner(self.context)
        return utils.HasText(getattr(survey, "introduction", None))


    def update(self):
        survey=aq_inner(self.context)
        if self.request.environ["REQUEST_METHOD"]!="POST":
            return

        self.request.response.redirect("%s/@@profile" % survey.absolute_url())



class Resume(grok.CodeView):
    """Survey resume screen.

    This view is used when a user resumes an existing session.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("resume")

    def render(self):
        survey=aq_inner(self.context)
        dbsession=SessionManager.session
        if redirectOnSurveyUpdate(self.request):
            return

        question=FindFirstQuestion(dbsession=dbsession)
        if question is None:
            # No tree generated, so start over
            self.request.response.redirect("%s/start" % survey.absolute_url())
        else:
            self.request.response.redirect(
                    QuestionURL(survey, question, phase="identification"))



class Identification(grok.View):
    """Survey identification start page.

    This view shows the introduction text for the identification phase. This
    includes an option to print a report with all questions.
    
    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identification* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("identification")
    grok.name("index_html")

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        self.survey=survey=aq_parent(aq_inner(self.context))
        question=FindFirstQuestion()
        if question is not None:
            self.next_url=QuestionURL(survey, question, phase="identification")
        else:
            self.next_url=None



class Evaluation(grok.View):
    """Survey evaluation start page.

    This view shows the introduction text for the evaluation phase. If the
    survey allows it an optionn is given to skip the evaluation phase and
    proceed directly to the action plan phase.
    
    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *evaluation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IEvaluationPhaseSkinLayer)
    grok.template("evaluation")
    grok.name("index_html")

    question_filter = sql.or_(model.MODULE_WITH_RISK_NO_TOP5_NO_POLICY_FILTER,
                              model.RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER)

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        self.survey=survey=aq_parent(aq_inner(self.context))
        question=FindFirstQuestion(filter=self.question_filter)
        if question is not None:
            self.next_url=QuestionURL(survey, question, phase="evaluation")
        else:
            self.next_url=None


class ActionPlan(grok.View):
    """Survey action plan start page.

    This view shows the introduction text for the action plan phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *actionplan* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("actionplan")
    grok.name("index_html")

    question_filter = sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                              model.RISK_PRESENT_OR_TOP5_FILTER)

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        self.survey=survey=aq_parent(aq_inner(self.context))
        question=FindFirstQuestion(filter=self.question_filter)
        if question is not None:
            self.next_url=QuestionURL(survey, question, phase="actionplan")
        else:
            self.next_url=None



class IdentificationReport(grok.View):
    """Generate identification report.

    The identification report lists all risks and modules along with their identification
    and evaluation results. It does not include action plan information.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identifcation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("report_identification")
    grok.name("report")

    download = None

    def random(self):
        return random.choice([True, False])


    def report_title(self):
        return SessionManager.session.title


    def title(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return node.title
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return zodbnode.problem_description
        return node.title


    def risk_status(self, node, zodbnode):
        if node.postponed or not node.identification:
            return "unanswered"
        elif node.identification in [u"n/a", u"yes"]:
            return "not-present"
        elif node.identification=="no":
            return "present"


    def show_negate_warning(self, node, zodbnode):
        """Check if the risk is present but does not have a problem description.
        In that case the user interface must show a special warning."""
        if node.type!="risk" or node.identification in [u"n/a", u"yes", None]:
            return False
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return False
        return True


    def imageUrl(self, node):
        if getattr(node, "image", None):
            return "%s/@@download/image/%s" % \
                    (node.absolute_url(), node.image.filename)


    def getZodbNode(self, treenode):
        try:
            return self.request.survey.restrictedTraverse(
                    treenode.zodb_path.split("/"))
        except KeyError:
            log.error("Caught reference in session for %s to missing node %s",
                    "/".join(self.request.survey.getPhysicalPath()),
                    treenode.zodb_path)
            return None


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        session=Session()
        dbsession=SessionManager.session
        query=session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==dbsession)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .order_by(model.SurveyTreeItem.path)
        self.nodes=query.all()


    def publishTraverse(self, request, name):
        """Check if the user wants to download this report by checking for a
        ``download`` URL entry. This uses a little trick: browser views
        implement `IPublishTraverse`, which allows us to catch traversal steps.
        """

        if self.download is not None:
            raise NotFound(self, name, request)

        if name=="download":
            self.download=True
            dbsession=SessionManager.session
            filename = _("filename_identification_report",
                         default=u"Identification ${title}.doc",
                         mapping=dict(title=dbsession.title))
            filename=translate(filename, context=self.request)
            self.request.response.setHeader("Content-Disposition",
                                "attachment; filename=\"%s\"" % filename.encode("utf-8"))
            self.request.response.setHeader("Content-Type", "application/msword")
            return self
        else:
            self.download=False
            raise NotFound(self, name, request)



class ReportView(grok.View):
    """Intro page for report phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identifcation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report")
    grok.name("index_html")

    def update(self):
        self.session=SessionManager.session

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            self.session.report_comment=reply.get("comment")
            url="%s/report/company" % self.request.survey.absolute_url()
            self.request.response.redirect(url)
            return



class ActionPlanReportView(grok.View):
    """Generate action report.

    The action plan report lists all present risks, including their action plan
    information.

    This view is registered for :obj:`PathGhost` instead of :obj:`ISurvey`
    since the :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report_actionplan")
    grok.name("view")

    download = False

    def random(self):
        return random.choice([True, False])


    def report_title(self):
        return SessionManager.session.title


    def title(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return node.title
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return zodbnode.problem_description
        return node.title


    def risk_status(self, node, zodbnode):
        if node.postponed or not node.identification:
            return "unanswered"
        elif node.identification in [u"n/a", u"yes"]:
            return "not-present"
        elif node.identification=="no":
            return "present"


    def show_negate_warning(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return False
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return False
        return True


    def imageUrl(self, node):
        if getattr(node, "image", None):
            return "%s/@@download/image/%s" % \
                    (node.absolute_url(), node.image.filename)


    def getZodbNode(self, treenode):
        return self.request.survey.restrictedTraverse(
                treenode.zodb_path.split("/"))

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        session=Session()
        self.session=SessionManager.session
        if self.session.company is None:
            self.session.company=model.Company()
        query=session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        self.nodes=query.all()



class ActionPlanReportDownload(ActionPlanReportView):
    """Generate and download action report.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report_actionplan")
    grok.name("download")

    def update(self):
        ActionPlanReportView.update(self)

        filename=_("filename_actionplan_report",
                   default=u"Action plan ${title}.doc",
                   mapping=dict(title=self.session.title))
        filename=translate(filename, context=self.request)
        self.request.response.setHeader("Content-Disposition",
                            "attachment; filename=\"%s\"" % filename.encode("utf-8"))
        self.request.response.setHeader("Content-Type", "application/msword")
        return self



class Status(grok.View):
    """Show survey status information.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("status")

    query = """SELECT SUBSTRING(path FROM 1 FOR 3) AS module,
                      CASE WHEN EXISTS(SELECT *
                                       FROM tree AS parent_node
                                       WHERE tree.session_id=%(sessionid)d AND
                                             tree.depth>parent_node.depth AND
                                             tree.path LIKE parent_node.path || '%%' AND
                                             parent_node.skip_children)
                                   THEN 'ignore'
                           WHEN postponed
                                   THEN 'postponed'
                           WHEN type='module' AND skip_children='f'
                                   THEN 'ignore'
                           WHEN type='module' AND postponed IS NOT NULL
                                   THEN 'ok'
                           WHEN type='risk' AND (SELECT identification
                                                 FROM risk
                                                 WHERE risk.id=tree.id) IN ('yes', 'n/a')
                                   THEN 'ok'
                           WHEN type='risk' AND (SELECT identification
                                                 FROM risk
                                                 WHERE risk.id=tree.id)='no'
                                   THEN 'risk'
                           ELSE 'todo'
                      END AS status,
                      COUNT(*) AS count
               FROM tree
               WHERE session_id=%(sessionid)d
               GROUP BY module, status;"""


    def getStatus(self):
        # Note: Optional modules with a yes-answer are not distinguishable
        # from non-optional modules, and ignored.
        session_id=SessionManager.id
        query=self.query % dict(sessionid=session_id)
        session=Session()
        result=session.execute(query).fetchall()

        modules={}
        base_url="%s/identification" % self.request.survey.absolute_url()
        for row in result:
            module=modules.setdefault(row.module, dict())
            if "url" not in module:
                module["url"]="%s/%s" % (base_url, int(row.module))
            module["path"]=row.module
            if row.status!="ignore":
                module["total"]=module.get("total", 0) + row.count
            module[row.status]=dict(count=row.count)

        titles=dict(session.query(model.Module.path, model.Module.title)\
                .filter(model.Module.session_id==session_id)\
                .filter(model.Module.path.in_(modules.keys())))
        for module in modules.values():
            module["title"]=titles[module["path"]]
            for status in ["postponed", "ok", "risk"]:
                if status in module:
                    module[status]["width"]=int(570*(float(module[status]["count"])/module["total"]))


        self.status=modules.values()
        self.status.sort(key=lambda m: m["path"])


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return
        self.getStatus()



class SurveyPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the survey skin layers.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent sine in Zope 2 that is only fired for site objects.
    """
    adapts(ISurvey, IClientSkinLayer)

    phases=dict(identification=IIdentificationPhaseSkinLayer,
                evaluation=IEvaluationPhaseSkinLayer,
                actionplan=IActionPlanPhaseSkinLayer,
                report=IReportPhaseSkinLayer)

    def findSqlContext(self, session_id, session_timestamp, zodb_path):
        """Find the closest SQL tree node for a candidate path.

        The path has to be given as a list of path entries. The session
        timestamp is only used as part of a cache key for this method.

        The return value is the id of the SQL tree node. All consumed
        entries will be removed from the zodb_path list.
        """
        # Pop all integer elements from the URL
        path=""
        head=[]
        while zodb_path:
            next=zodb_path.pop()
            if len(next)>3:
                zodb_path.append(next)
                break

            try:
                path+="%03d" % int(next)
                head.append(next)
            except ValueError:
                zodb_path.append(next)
                break

        # Try and find a SQL tree node that matches our URL
        query=Session.query(model.SurveyTreeItem.id).\
                filter(model.SurveyTreeItem.session_id==session_id).\
                filter(model.SurveyTreeItem.path==sql.bindparam("path"))
        while path:
            node=query.params(path=path).first()
            if node is not None:
                return node[0]

            path=path[:-3]
            zodb_path.append(head.pop())



    def setupContext(self, tree_id):
        """Build an acquisition context for a tree node.
        """
        node=Session.query(model.SurveyTreeItem).get(tree_id)

        tail=self.context
        path=node.path
        while len(path)>3:
            id=str(int(path[:3]))
            path=path[3:]
            tail=PathGhost(id).__of__(tail)
        
        return node.__of__(tail)


    def hasValidSession(self, request):
        """Check if the user has an active session for the survey.
        """
        dbsession=SessionManager.session
        if dbsession is None:
            return False
        if dbsession.zodb_path!=utils.RelativePath(request.client, self.context):
            return False
        return True



    def publishTraverse(self, request, name):
        request.survey=self.context
        utils.setLanguage(request, self.context, self.context.language)

        if name not in ["view", "index_html"] and not self.hasValidSession(request):
            request.response.redirect(
                    aq_parent(aq_parent(self.context)).absolute_url(), lock=True)
            return self.context

        if name not in self.phases:
            return super(SurveyPublishTraverser, self).publishTraverse(request, name)

        # Decorate the request with the right skin layer and add to the aq path
        directlyProvides(request, self.phases[name],
                         *directlyProvidedBy(request))
        self.context=PathGhost(name).__of__(self.context)

        session=SessionManager.session
        tree_id=self.findSqlContext(session.id, session.created, request["TraversalRequestNameStack"])
        if tree_id is not None:
            return self.setupContext(tree_id)

        # No SQL based traversal possible, return the existing context with the
        # new skin layer applied
        return self.context

