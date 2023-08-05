<%include file="header.tpl" />
<div id="content">
    <h1>Welcome</h1>
    
    <h2>Database list:</h2>
    
    <ul>
    % for db in dbs:
        <li><a href="/${db}">${db}</a></li>
    % endfor
    </ul>
</div>
<%include file="footer.tpl" />
