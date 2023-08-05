<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>${c.title}</title>
    <style type="text/css">
    th {text-align: left; padding:0.25em 0;}
    </style>
    % if h.url.current().endswith('privindex'):
    <style type="text/css">
    th {background-color: #fee;}
    </style>
    % else:
    <style type="text/css">
    th {background-color: #eef;}
    </style>
    % endif

</head>
<body>
    
    <h4>Users</h4>
    <table style="width:100%;padding:0 1em; font-size:75%">
        <tr>
            <th>name</th>
            <th>email</th>
            <th>created</th>
            <th>lastlogin</th>
        </tr>
        % for u in c.users:
        <tr>
            <td>${u.displayname}</td>
            <td>${u.email}</td>
            <td>${u.created}</td>
            <td>${u.last_login}</td>
        </tr>
        % endfor
    </table>

    <h4>Groups</h4>
    <table style="width:100%;padding:0 1em; font-size:75%">
        <tr>
            <th>name</th>
            <th>description</th>
            <th>created</th>
            <th>active</th>
            <th>users</th>
            <th>permissions</th>
        </tr>
        % for g in c.groups:
        <tr>
            <td>${g.name}</td>
            <td>${g.description}</td>
            <td>${g.created}</td><td>${g.active}</td>
            <td>${', '.join([u.displayname for u in g.users])}</td>
            <td>${', '.join([p.name for p in g.permissions])}</td>
        </tr>
    % endfor
    </table>

    <h4>Permissions</h4>
    <table style="width:100%;padding:0 1em; font-size:75%">
        <tr>
            <th>name</th>
            <th>description</th>
            <th>groups</th>
        </tr>
        % for p in c.permissions:
        <tr><td>${p.name}</td><td>${p.description}</td>
        <td>${', '.join([group.name for group in p.groups])}</td>
        </tr>
    % endfor
    </table>
    <p><a href="/demo/index">Public</a> :: <a href="/demo/privindex">Private</a></p>
    <p>
        % if session.get('logged_in'):
            Logged in as <span style="color:green">${session['displayname']}</span>
            ${h.link_to('Logout', url=url('account_logout'))}
        % else:
        Welcome <span style="color:red">Anonymous</span> ${h.link_to('Login', url=url('account_login'))}
        % endif
    </p>

</body>
</html>
