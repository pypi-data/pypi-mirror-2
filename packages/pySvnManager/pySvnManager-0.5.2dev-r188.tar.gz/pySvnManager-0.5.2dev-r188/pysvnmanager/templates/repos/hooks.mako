## -*- coding: utf-8 -*-
## vim: et ts=4 sw=4
<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>${_("Repos management")}</title>
</%def>

<%def name="body_params()">    onload="init_repos_list()" </%def>

<SCRIPT LANGUAGE="JavaScript">

// Display repos list only.
function show_init_form()
{
    $('repos_list_box').show();

    $('uninstall_hook_box').hide();

    $('hook_setting_box').hide();

    $('installed_hook_box').show();
}


function init_repos_list()
{
    showGlobalMessage();
    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="repos", action="init_repos_list")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();ajax_init_repos_list(request.responseText);}
        });
}

function ajax_init_repos_list(code)
{
    var id = new Array();
    var name = new Array();
    var total = 0;

    repos_list = document.main_form.repos_list;
    repos_list.options.length = 0;

    try {
        eval(code);
        for (var i=0; i < total; i++)
        {
            repos_list.options[i] = new Option(name[i], id[i]);
        }
    }
    catch(exception) {
        alert(exception);
    }

    repos_changed();
}

function repos_changed()
{
    var name = document.main_form.repos_list.value;
    var params = {select:name};

    if (name=='...'||name=='')
    {
        $('installed_hook_form_contents').innerHTML = "";
        show_init_form();
    }
    else
    {
        showNoticesPopup();
        new Ajax.Request(
            '${h.url(controller="repos", action="get_plugin_list")}',
            {asynchronous:true, evalScripts:true, method:'post',
                onFailure:
                    function(request)
                        {set_message_box(request.responseText, 'error');},
                onSuccess:
                    function(request)
                        {ajax_repos_changed(request.responseText);},
                onComplete:
                    function(request)
                        {hideNoticesPopup();},
                parameters:params
            });

        new Ajax.Updater(
            'installed_hook_form_contents',
            '${h.url(controller="repos", action="get_installed_hook_form")}',
            {asynchronous:true, evalScripts:true, method:'post',
                onFailure:
                    function(request)
                        {set_message_box(request.responseText, 'error');},
                onComplete:
                    function(request)
                        {hideNoticesPopup();},
                parameters:params
            });
    }
}

function ajax_repos_changed(code)
{
    var id = new Array();
    var name = new Array();
    var total = 0;

    unset_plugin_list = document.main_form.unset_plugin_list;
    unset_plugin_list.options.length = 0;

    try {
        eval(code);
        if (total==1)
        {
            $('uninstall_hook_box').hide();
            $('hook_setting_box').hide();
        }
        else
        {
            $('uninstall_hook_box').show();
            for (var i=0; i < total; i++)
            {
                unset_plugin_list.options[i] = new Option(name[i], id[i]);
            }
        }
    }
    catch(exception) {
        alert(exception);
    }

    select_unset_hook_list();
}

function select_unset_hook_list()
{
    var pluginname = document.main_form.unset_plugin_list.value;

    if (pluginname=='...'||pluginname=='')
    {
        $('hook_setting_form_contents').innerHTML = "";
        $('hook_setting_box').hide();
    }
    else
    {
        show_hook_config_form(pluginname);
    }
}

function show_hook_config_form(hookid)
{
    var reposname  = document.main_form.repos_list.value;
    var params = {repos:reposname, plugin:hookid};

    $('hook_setting_box').show();
    showNoticesPopup();
    new Ajax.Updater(
        {success:'hook_setting_form_contents'},
        '${h.url(controller="repos", action="get_hook_setting_form")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onFailure:
                function(request)
                    {set_message_box(request.responseText, 'error');},
            onComplete:
                function(request)
                    {hideNoticesPopup();},
            parameters:params
        });
}

function installed_hook_form_submit(form)
{
    var reposname  = document.main_form.repos_list.value;
    if (reposname=="..."||reposname=="")
    {
        alert("Bad repository or plugin name");
        return false;
    }
    form._repos.value = reposname;
}

</SCRIPT>


<h2>${_("Repos management")}</h2>

<form name="main_form" method="post">
<DIV class=gainlayout>

<DIV id="repos_list_box" class=gainlayout>
<span class="title">
  ${_("Repository:")}
</span>
    <select name="repos_list" size="1" onChange='repos_changed()' class="select-repos">
    </select>
% if c.is_super_user:
    <a href="${h.url(controller="repos", action="create")}"><img
        src="${h.url("/img/add.png")}"  title="${_("Add repository")}" alt="(+)"></a>
        ${_("Add repository")}&nbsp;&nbsp;
    <a href="${h.url(controller="repos", action="remove")}"><img
        src="${h.url("/img/delete.png")}"  title="${_("Remove blank repository")}" alt="(-)"></a>
        ${_("Remove blank repository")}
% endif
</DIV>

<DIV id="uninstall_hook_box" class=gainlayout>
<hr>
<span class="title">
  ${_("Uninstalled hooks:")}
</span>
    <select name="unset_plugin_list" size="1" onChange='select_unset_hook_list()' class="select-plugin">
    </select>
</form>
</DIV>
<DIV id="hook_setting_box" class=gainlayout>
## <form name="hook_setting_form" method="post" action="${h.url(controller="repos", action='setup_hook')}">
<br>

<form action="${h.url(controller="repos", action='setup_hook')}"
  id="hook_setting_form" method="POST"
  onsubmit="showNoticesPopup();
            new Ajax.Request(
                '${h.url(controller="repos", action='setup_hook')}',
                {
                 asynchronous:true, evalScripts:true, method:'post',
                 onFailure:
                    function(request)
                        {set_message_box(request.responseText, 'error');},
                 onComplete:
                    function(request)
                    {hideNoticesPopup();set_message_box_json(request.responseText);repos_changed();},
                 parameters:Form.serialize(this)
                });
            return false;">

    <table class='hidden' width='99%'>
      <tr>
        <td>
          <div id="hook_setting_form_contents"></div>
        </td></tr>
      <tr>
        <td align='center'>
          <input type="submit" name="apply" value="${_("Install this plugin")}" class="input-button">
        </td>
      </tr>
    </table>
</form>
</DIV>

<hr>

<DIV id="installed_hook_box" class=gainlayout>
## <form name="installed_hook_form" method="post" action="${h.url(controller="repos", action='remove_hook')}"
##         onSubmit="installed_hook_form_submit(this)">

<form action="${h.url(controller="repos", action='uninstall_hook')}"
  id="installed_hook_form" method="POST"
  onsubmit="installed_hook_form_submit(this); showNoticesPopup();
            new Ajax.Request(
                '${h.url(controller="repos", action='uninstall_hook')}',
                {
                 asynchronous:true, evalScripts:true, method:'post',
                 onFailure:
                    function(request)
                        {set_message_box(request.responseText, 'error');},
                 onComplete:
                    function(request)
                    {hideNoticesPopup();set_message_box_json(request.responseText);repos_changed();},
                 parameters:Form.serialize(this)
                });
            return false;">

    <input type='hidden' name='_repos' class="input-button">
    <div id="installed_hook_form_contents"></div>
</DIV>

</DIV>

