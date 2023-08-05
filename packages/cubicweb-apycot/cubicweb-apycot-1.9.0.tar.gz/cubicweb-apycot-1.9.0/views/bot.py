"""this module contains views related to bot status and activity

:organization: Logilab
:copyright: 2009-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

from logilab.common.tasksqueue import REVERSE_PRIORITY
from logilab.mtconverter import xml_escape

from cubicweb import UnknownEid, tags
from cubicweb.selectors import match_kwargs
from cubicweb.view import StartupView, View

from cubes.apycot.entities import bot_proxy

class ApycotHelpView(StartupView):
    __regid__ = 'apycotdoc'

    def page_title(self):
        return self._cw._('apycot documentation')

    def call(self):
        _ = self._cw._
        self.w(u'<h1>%s</h1>' % self.page_title())
        bot = bot_proxy(self._cw.vreg.config, self._cw.data)
        self.w(u'<p>%s</p>' % _(
            'First notice that you may miss some information if you\'re using '
            'some plugin not loaded by the apycot bot.'))
        self.section('checkers')
        headers = [_('checker'), _('need preprocessor'), _('description')]
        data = [(defdict['id'], defdict['preprocessor'], xml_escape(defdict['help']))
                 for defdict in bot.available_checkers()]
        self.wview('pyvaltable', pyvalue=data, headers=headers)
        self.section('preprocessors')
        headers = [_('preprocessor'), _('description')]
        data = [(defdict['id'], xml_escape(defdict['help']))
                 for defdict in bot.available_preprocessors()]
        self.wview('pyvaltable', pyvalue=data, headers=headers)
        self.section('options')
        headers = [_('option'), _('required'), _('type'), _('description')]
        data = [(defdict.get('id', defdict['name']),
                 defdict.get('required') and _('yes') or _('no'),
                 defdict['type'], xml_escape(defdict['help']))
                 for defdict in bot.available_options()]
        self.wview('pyvaltable', pyvalue=data, headers=headers)

    def section(self, name):
        self.w(u'<h2>%s</h2><a name="%s"/>' % (self._cw._(name), name))


class BotStatusView(StartupView):
    """This view displays pending and running tasks when the bot is
       available, otherwise displays error message explaining why
       the bot is unavailable.
    """
    __regid__ = 'botstatus'
    title = _('Apycot bot status')

    def call(self):
        req = self._cw
        _ = req._
        # bot availability
        if not 'vtitle' in req.form:
            self.w(u'<h1>%s</h1>' % _(self.title))
        full_pyro_id = ':%(pyro-ns-group)s.%(pyro-instance-id)s' % req.vreg.config
        try:
            bot = bot_proxy(req.vreg.config, req.data)
            pending, running = bot.pending_tasks(full_pyro_id)
        except Exception, ex:
            msg = _(u'Bot is not available for the following reason:')
            self.w(u'<p>%s %s</p>' % (msg, ex))
            return
        self.w(u'<p>%s</p>' % _('Bot is up and available.'))
        # pending and running tasks
        headers = [_('TestConfig'), _('priority'), _('vcs_branch')]
        self.w(u'<h2>%s</h2>' % _('%i Running tasks') % len(running))
        if running:
            self.wview('pyvaltable',
                       pyvalue=table_from_tasks(req, running),
                       headers=headers)
        else:
            self.w(u'<p>%s</p>' % _(u'No running task'))
        self.w(u'<h2>%s</h2>' % _('%i Pending tasks') % len(pending))
        if pending:
            self.wview('pyvaltable',
                       pyvalue=table_from_tasks(req, reversed(pending)),
                       headers=headers)
        else:
            self.w(u'<p>%s</p>' % _(u'No pending task'))


def table_from_tasks(req, tdicts):
    data = []
    for tdict in tdicts:
        if tdict is None:
            data.append( (u'<i>%s</i>' % req._('task from another instance'),
                          u'', u'')
                         )
            continue
        try:
            # don't specify etype so we detect if entity has been deleted
            tc = req.entity_from_eid(tdict['eid'])
        except UnknownEid:
            continue
        data.append( (tags.a(tc.dc_title(),
                             href=tc.absolute_url(tab='tc_execution')),
                      # XXX sortvalue
                      req._(REVERSE_PRIORITY[tdict['priority']]),
                      xml_escape(tdict['branch'] or u''))
                     )
    return data


