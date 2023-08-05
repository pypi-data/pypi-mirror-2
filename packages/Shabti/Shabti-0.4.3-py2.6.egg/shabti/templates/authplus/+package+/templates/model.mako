# -*- coding: utf-8 -*-
# Miruku information
<%! from datetime import datetime %>
<%inherit file="layout.mako"/>
<%def name="header()">
<title>${c.title if hasattr(c, 'title') and \
            c.title else 'Miruku info'|n}</title>
</%def>
<%def name="body()">
<style type="text/css">
h1 {margin-left: 1em; margin-bottom:0; font-size:130%;}
h1 span.opt {color: #22c;}
h1 span.name {color: #f33;}
table.minfo {width:100%; padding:1em; border:1px solid #aaa;}
div.meta { font-size: 100%; font-family: monospace; 
           padding: 0.33em 1em; border: 1px solid #bbb;
           min-height: 5em; margin: 1.66em;}
tr.colh { font-weight: bold; background: #ccc;} 
tr.row { background: #eee }
tr.row td a {text-decoration: none;}
td.bool {align: center;}
div.metadlabel {float: left; color: #a66; width:25%;}
div.metadval {float: right; font-style:italic; 
              color: #0c0; width:75%;}
span.tname {color:#22c;}
span.accept {height:16px; width:16px;
    /* Do replace this link with one of your own */
    background: url(
        'http://www.famfamfam.com/lab/icons/silk/icons/accept.png'
            ) no-repeat;}
span.delete {height:16px; width:16px;
    /* Do replace this link with one of your own */
    background: url(
        'http://www.famfamfam.com/lab/icons/silk/icons/delete.png'
        ) no-repeat;}
span.delete em, span.accept em {visibility: hidden;}
div#snavd {border:1px solid #bbb;padding:0; 
           margin:1em 1.66em 0 1.66em; 
           min-height:1.33em;}
div#info {margin:-2em 0.5em 0.5em 0.5em; padding: 1em;}
div.inpctl {float:left;margin-left:2em;}
</style>

<h1>Miruku metadata report for: 
    <span class="opt">${c.opt}</span>  
    <span class="name">${c.name|n}</span> </h1>

<div id="snavd">
    <div class="inpctl">
    <form name="info" id="info" action="${h.url('miruku_report', opt='info')}" method="post">
        <input type="submit" value="info"/></form>
    </div>
    <div class="inpctl">
    <form name="check" id="check" action="${h.url('miruku_report', opt='check')}" method="post">
        <input type="submit" value="check"/></form>
    </div>
    <div class="inpctl" style="margin-left:4em">
    <form name="upgrade" id="upgrade" action="${h.url('miruku_report', opt='upgrade')}" method="post"
        onsubmit="javascript:return(confirm('Really upgrade the database?'))"
        ><input type="submit" value="upgrade"/></form>
    </div>
    <div class="inpctl" style="margin-left:6em">
    <form name="create" id="create" action="${h.url('miruku_report', opt='create')}" method="post" 
        onsubmit="javascript:return(confirm('Really create new metadata?'));"
        ><input type="submit" value="create"/></form>
    </div>
    <div class="inpctl" style="margin-left:6em">
    <form name="drop" id="drop" action="${h.url('miruku_report', opt='drop')}" method="post" 
        onsubmit="javascript:return(confirm('Really drop the metadata?'));"
        ><input type="submit" value="drop"/></form>
    </div>
</div>
% if not c.content:

    <div class="meta">
        <h3>The database is not associated with miruku.</h3>
        <p>Please run the "miruku create" command first.</p>
    </div>

% elif isinstance(c.content, basestring):

    <div class="meta">
        <p>${c.content.replace("`",'"')|n}</p>
    </div>

% elif isinstance(c.content, list):

    <div class="meta">
        <div style="margin: 0.5em; padding: 1em;">
        % for i in c.content:
        <p>${i.replace("`",'"')|n}</p>
        % endfor
        </div>
    </div>

% else:

    <div class="meta">
        <div>
        % for idx, i in enumerate(zip(['Metadata name','Persistence URL', \
                        'Created on','Last updated'], c.content[c.name][0])):
            <div class="metadlabel">${i[0]}:</div>
            <div class="metadval">
                ${i[1].strftime("%a, %b %d %Y %H:%M:%S") \
                  if isinstance(i[1], datetime) else i[1]|n}</div>
            % if idx == 1:
            </div>
            <div>
            % endif
        % endfor
        </div>
    </div>
    <div id="info">
    % for i in c.content[c.name][1:]:
        <h3>Table: <span class="tname">${i[0]}</span></h3>
        <table class="minfo">
        <tr class="colh">
            % for idx, j in enumerate(['Column Name', 'Type', \
                                       'Primary Key?', 'Nullable?', \
                                       'Index?']):
            <td style="width:20%"
                ${'align="center"' if idx > 1 else ''|n}
            >${j}</td>
            % endfor
        </tr>
        % for j in i[1]:
            <tr class="row">
            % for idx, k in enumerate(j):
                <td ${'align="center"' if k in ['True', 'False'] else ''|n}
                    >${'<span class="%s"><em>t/f</em></span>' % \
                        dict(True='accept',False='delete').get(k,'help') \
                            if k in ['True', 'False'] \
                            else '<a href="http://www.sqlalchemy.org/' + \
                                 'docs/reference/sqlalchemy/types.html'+\
                                 '#sqlalchemy.types.%s">%s</a>' % \
                                 (k, k) if idx else k \
                            |n}</td>
            % endfor
            </tr>
        % endfor
        </table>
    % endfor
    </div>

% endif
</%def>
<%def name="lhcolumn()">
</%def>
<%def name="rhcolumn()">
</%def>

