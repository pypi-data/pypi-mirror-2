<%include file="header.tpl" />
<%namespace name="h" file="utils.tpl"/>

<div id="content">
    <h1>DB: <a href="/${db}">${db}</a>/${coll}</h1>

    <h2>Found ${count} ${(count==1) and 'doc' or 'docs'}, showing from ${skip} to ${skip + limit} (<a href="/${next_url}">skip</a>):</h2>
    
    <ul>
    % for doc in docs:
        <li>
            % if '_id' in doc:
            <h3>${doc.pop('_id')}</h3>
            % endif
            ${h.render(doc)}
        </li>
    % endfor
    </ul>
</div>
<%include file="footer.tpl" />

