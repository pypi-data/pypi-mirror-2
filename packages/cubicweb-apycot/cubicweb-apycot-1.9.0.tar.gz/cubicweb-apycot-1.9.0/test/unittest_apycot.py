from utils import ApycotBaseTC

from apycotbot.writer import DataWriter
from apycotbot.utils import ConnectionHandler

from cubes.apycot.logformat import log_to_html


CW_NAMESPACE_DIV = '<div xmlns:cubicweb="http://www.logilab.org/2008/cubicweb">%s</div>'

class ApycotTC(ApycotBaseTC):

    def setUp(self):
        super(ApycotBaseTC, self).setUp()
        cnx = self.login('apycotbot', password='apycot')
        cnxh = ConnectionHandler(self.config.appid, cnxinfo={})
        cnxh.cnx = cnx
        cnxh._cu = cnx.cursor()
        cnxh.cw = cnxh._cu.req
        writer = DataWriter(cnxh, self.lgc.eid)
        writer.start_test(u'default')
        writer.start_check(u'pylint', {})
        writer.raw('pylint_version', '0.18.1', type=u'version')
        writer.debug('hip', path='/tmp/something', line=12)
        writer.info('hop', path='/tmp/something')
        writer.warning('''momo\n\n<br/>''')
        writer.end_check(u'success')
        writer.start_check(u'lintian', {'option': 'value'})
        writer.raw('lintian_version', '1.0')
        writer.error('bouh')
        writer.fatal('di&d')
        writer.end_check(u'failure')
        writer.end_test(u'failure')
        self.checks = self.execute('Any X, N ORDERBY N WHERE X is CheckResult, X name N')

    def test_writer_log_content(self):
        checks = self.checks
        self.assertEquals(len(checks), 2)
        self.assertTextEquals(checks.get_entity(0, 0).log, '''\
40\t\t\tbouh<br/>
50\t\t\tdi&amp;d<br/>''')
        self.assertTextEquals(checks.get_entity(1, 0).log, '''\
10\t/tmp/something\t12\thip<br/>
20\t/tmp/something\t\thop<br/>
30\t\t\tmomo

&lt;br/&gt;<br/>''')

    def test_log_formatting_first_check(self):
        stream = []
        log_to_html(self.request(), self.checks.get_entity(0, 0).log, stream.append)
        log_html = '\n'.join(stream)
        self.assertXMLStringWellFormed(CW_NAMESPACE_DIV % log_html)
        for pattern, count in (
                ('<table class="listing apylog">', 1),
                ('<tr class="logError"', 1),
                ('<tr class="logFatal"', 1),
                ('<td class="logSeverity"', 2),
                ('<td class="logPath"',  2),
                ('<td class="logMsg"',   2),
                ('<pre class="rawtext"', 2),
                ('bouh', 1),
                ('di&amp;d',1),
            ):
            self.assertIn(pattern, log_html)
            self.assertEquals(log_html.count(pattern), count)

    def test_log_formatting_second_check(self):
        stream = []
        log_to_html(self.request(), self.checks.get_entity(1, 0).log, stream.append)
        log_html = '\n'.join(stream)
        self.assertXMLStringWellFormed(CW_NAMESPACE_DIV % log_html)
        for pattern, count in (
                ('<table class="listing apylog">', 1),
                ('<tr class="logDebug"', 1),
                ('<tr class="logInfo"', 1),
                ('<tr class="logWarning"', 1),
                ('<td class="logSeverity"', 3),
                ('<td class="logPath"',  3),
                ('<td class="logMsg"',   3),
                ('<pre class="rawtext"', 3),
                ('hip', 1),
                ('hop', 1),
                ('momo', 1),
            ):
            self.assertIn(pattern, log_html)
            self.assertEquals(log_html.count(pattern), count)
