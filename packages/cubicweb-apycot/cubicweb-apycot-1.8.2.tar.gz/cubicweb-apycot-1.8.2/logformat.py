# coding: utf-8
"""utilities to turn apycot raw logs into nice html reports

nn:organization: Logilab
:copyright: 2008-2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"
_ = unicode

import logging
from cubicweb.utils import make_uid


REVERSE_SEVERITIES = {
    logging.DEBUG :   _('DEBUG'),
    logging.INFO :    _('INFO'),
    logging.WARNING : _('WARNING'),
    logging.ERROR :   _('ERROR'),
    logging.FATAL :   _('FATAL')
    }


def log_to_html(req, data, w):
    """format apycot logs data to an html table

    log are encoded by the apycotbot in the following format for each record:

      encodedmsg = u'%s\t%s\t%s\t%s<br/>' % (severity, path, line,
                                             xml_escape(msg))

    """
    # XXX severity filter / link to viewcvs or similar
    req.add_js('cubes.apycot.js')
    req.add_js('jquery.tablesorter.js')
    req.add_css('cubicweb.tablesorter.css')


    req.add_onload('$("select.log_filter").val("%s").change();'
                    %  req.form.get('log_level', 'Info'))
    w(u'<form>')
    w(u'<label>%s</label>' % _(u'Messages Threshold'))
    w(u'<select class="log_filter" onchange="filter_log(this.options[this.selectedIndex].value)">')
    for level in ('Debug', 'Info', 'Warning', 'Error', 'Fatal'):
        w('<option value="%s">%s</option>' % (level, _(level)))
    w(u'</select>')
    w(u'</form>')


    w(u'<table class="listing apylog">')
    w(u'<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % (
        req._('severity'), req._('path or command'), req._('line'), req._('message')))
    for msg_idx, record in enumerate(data.split('<br/>')):
        record = record.strip()
        if not record:
            continue
        try:
            severity, path, line, msg = record.split('\t', 3)
        except:
            req.warning('badly formated apycot log %s' % record)
            continue
        severityname = REVERSE_SEVERITIES[int(severity)]
        log_msg_id = 'log_msg_%i' % msg_idx
        w(u'<tr class="log%s" id="%s">' % (severityname.capitalize(),
                                           log_msg_id))
        w(u'<td class="logSeverity" cubicweb:sortvalue="%s">' % severity)
        data = {
            'severity': req._(REVERSE_SEVERITIES[int(severity)]),
            'title': _('permalink to this message'),
            'msg_id': log_msg_id,
        }
        w(u'''<a class="internallink" href="javascript:;" title="%(title)s" '''
          u'''onclick="document.location.hash='%(msg_id)s';">&#182;</a>'''
          u'''&#160;%(severity)s''' % data)
        w(u'</td>')
        w(u'<td class="logPath">%s</td>' % (path or u'&#160;'))
        w(u'<td class="logLine">%s</td>' % (line or u'&#160;'))

        w(u'<td class="logMsg">')


        SNIP_OVER = 7

        lines = msg.splitlines()
        if len(lines) <= SNIP_OVER:
            w(u'<pre class="rawtext">%s</pre>' % msg)
        else:
            # The make_uid argument have not specific meaning here.
            div_snip_id = make_uid(u'log_snip_')
            div_full_id = make_uid(u'log_full_')
            divs_id = (div_snip_id, div_full_id)
            snip = u'\n'.join((lines[0],
                               lines[1],
                               u'  ...',
                               u'    %i more lines [click to expand]' % (len(lines)-4),
                               u'  ...',
                               lines[-2],
                               lines[-1]))


            divs = (
                (div_snip_id, snip, u'expand', "class='collapsed'"),
                (div_full_id, msg,  u'collapse', "class='hidden'")
            )
            for div_id, content, button, h_class in divs:
                text = _(button)
                js   = u"toggleVisibility('%s'); toggleVisibility('%s');" % divs_id

                w(u'<div id="%s" %s>' % (div_id, h_class))
                w(u'<pre class="raw_test" onclick="javascript: %s" '
                   'title="%s" style="display: block;">' % (js, text))
                w(u'%s' % content)
                w(u'</pre>')
                w(u'</div>')


        w(u'</td>')

        w(u'</tr>\n')
    w(u'</table>')
