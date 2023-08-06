<%!
from pymongo.objectid import ObjectId
%>

<%def name="render(doc)">
    <li>
        % if '_id' in doc:
        <h3>${doc.pop('_id')}</h3>
        % endif
        ${render_content(doc) | h}
    </li>
</%def>

<%def name="render_content(d)">
    % if isinstance(d, dict):
    <dl>
        <dt>{</dt><dd>&nbsp;</dd>
        % for k, v in d.items():
        <dt>${k}</dt>
            <dd>${render_value(v) | h}</dd>
        % endfor
        <dt>}</dt><dd>&nbsp;</dd>
    </dl>

    % elif isinstance(d, list):
    <ol><li>[</li>
        % for v in d:
        <li>${render_value(v) | h}</li>
        % endfor
        <li>]</li>
    </ol>
    % endif
</%def>

<%def name="render_value(v)">
    % if isinstance(v, (dict, list)):
        ${render_content(v) | h}
    % elif isinstance(v, ObjectId):
        <a href="/guess/${db}/${v}">${v}</a>
    % else:
        ${v or '&nbsp;'}
    % endif
</%def>

