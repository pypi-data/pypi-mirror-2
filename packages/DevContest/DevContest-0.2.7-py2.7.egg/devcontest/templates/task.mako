<%inherit file="/base.mako"/>

<%def name="title()">${c.task.name}</%def>

<%def name="body()">
	<a href=${h.url_for(controller="contest", action="tasks", id=c.task.contest_id)} class="back">${_('back to the contest')}</a>
	<h2>${c.task.name}</h2>
	${c.task.description | n}

	<hr style="visibility:hidden;">

	<div id="example_in"><h3>${_('Example of input')}:</h3><pre>${c.task.example_in}</pre></div>
	<div id="example_out"><h3>${_('Example of output')}:</h3><pre>${c.task.example_out}</pre></div>
<%
from devcontest.model import Contest
from devcontest.model.meta import Session
%>
% if Session.query(Contest.is_running).filter_by(id=c.task.contest_id).first()[0]:
	<hr>
	% if not c.status or request.environ.get('REMOTE_USER').admin:
	 ${h.form_start(h.url_for(param="upload"), method="post", multipart=True)}
	 ${h.field(_("Source code"), h.file(name="source"))}
	 ${h.field("", h.submit("submit", _("Submit")))}
	 ${h.form_end()}
	% endif
	% if c.status:
		<div class="success">${_('The task was solved')}</div>
	% endif

	% if c.source:
	<h3>${_('Last version')}</h3>
	<%
	from pygments import highlight
	from pygments.lexers import guess_lexer
	from pygments.formatters import HtmlFormatter
	%>
	% if c.source.errors:
	<pre>${c.source.errors}</pre>
	% endif

	${highlight(c.source.source, guess_lexer(c.source.source), HtmlFormatter(linenos=True)) | n}

	% endif
%endif
</%def>
