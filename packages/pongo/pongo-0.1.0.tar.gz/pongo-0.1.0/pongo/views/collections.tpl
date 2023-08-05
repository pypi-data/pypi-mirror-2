<%include file="header.tpl" />
<div id="content">
    <h1>DB: ${db}</h1>

    <h2>Collections list:</h2>
    
    <ul>
    % for coll in colls:
        <li><a href="/${db}/${coll}">${coll}</a></li>
    % endfor
    </ul>
</div>
<%include file="footer.tpl" />
