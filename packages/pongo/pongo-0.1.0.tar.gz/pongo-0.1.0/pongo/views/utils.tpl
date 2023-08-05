<%!
from pymongo.objectid import ObjectId
%>

<%def name="render(d)">

    % if isinstance(d, dict):
    <dl>
        % if not d:
            {}
        % endif
        % for k, v in d.items():
        <dt>${k}</dt>
            <dd>
            % if isinstance(v, (dict, list)):
                ${render(v)}
            % elif isinstance(v, ObjectId):
                <a href="/guess/${db}/${v}">${v}</a>
            % else:
                ${v or '&nbsp;'}
            % endif
            </dd>
        % endfor
    </dl>
    % elif isinstance(d, list):
    <ol>
        % if not d:
            []
        % endif
        % for v in d:
        <li>
            % if isinstance(d, (dict, list)):
                ${render(v)}
            % elif isinstance(v, ObjectId):
                <a href="/guess/${db}">${v}</a>
            % else:
                ${v or '$nbsp;'}
            % endif
        </li>
        % endfor
    </ol>
    % endif
</%def>

