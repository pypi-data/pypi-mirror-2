<%include file="header.tpl" />
<%namespace name="h" file="utils.tpl"/>

<div id="content">
    <h1>DB: <a href="/${db}">${db}</a></h1>

    <h2>Found ${count} ${(count==1) and 'doc' or 'docs'}:</h2>
    
    <ul>
    % for coll, doc in docs.items():
        <li>
            <h3><a href="/${db}/${coll}">${coll}</a>/${doc['_id']}</h3>
            ${h.render(doc)}
        </li>
    % endfor
    </ul>
</div>
<%include file="footer.tpl" />

