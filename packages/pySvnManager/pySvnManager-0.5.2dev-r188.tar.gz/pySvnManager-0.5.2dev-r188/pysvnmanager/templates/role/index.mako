## -*- coding: utf-8 -*-
## vim: et ts=4 sw=4

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>${_("Role Management")}</title>
</%def>

<%def name="body_params()"> onload="role_changed()" </%def>

<%

role_list_opts = [('...', _("Please choose...")),]

for i in c.grouplist:
    if i == '*' or i =='$authenticated' or i == '$anonymous':
        continue
    elif i[0] == '@':
        role_list_opts.append((i, _("Group:")+i[1:]))
    else:
        role_list_opts.append((i, i))
for i in c.aliaslist:
    if i[0] == '&':
        role_list_opts.append((i, _("Alias:")+i[1:]))
    else:
        role_list_opts.append((i, i))

alias_as_list_opts = [('...', _("Please choose...")),]

for id, display in c.userlist:
    if display:
        alias_as_list_opts.append((id, "%s (%s)" % (id, display)))
    else:
        alias_as_list_opts.append((id, id))

all_avail_users = []
for i in c.grouplist:
    if i == '*' or i =='$authenticated' or i == '$anonymous':
        continue
    if i[0] == '@':
        all_avail_users.append([i, _("Group:")+i[1:]])
    else:
        all_avail_users.append([i, i])
for i in c.aliaslist:
    if i[0] == '&':
        all_avail_users.append([i, _("Alias:")+i[1:]])
    else:
        all_avail_users.append([i, i])
for id, display in c.userlist:
    if display:
        all_avail_users.append([id, "%s (%s)" % (id, display)])
    else:
        all_avail_users.append([id, id])

%>


<SCRIPT LANGUAGE="JavaScript">

<%
msg = 'var all_users = { '

for user in all_avail_users:
    msg += '\n"%s": "%s",' % (user[0], user[1])
msg = msg.strip().rstrip(',')
msg +=' };\n'
context.write(msg)
%>

function show_init_form()
{
    $('role_list_box').show();

    $('group_input_box').hide();

    $('alias_input_box').hide();

    $('group_edit_box').hide();

    $('alias_edit_box').hide();

    $('action_box').hide();
}

function show_group_form()
{
    show_init_form();

    $('group_edit_box').show();

    $('action_box').show();

    disable_save_btn();
    enable_delete_btn();
}

function show_alias_form()
{
    show_init_form();

    $('alias_edit_box').show();

    $('action_box').show();

    disable_save_btn();
    enable_delete_btn();
}

function show_new_group_form()
{
    show_group_form();

    $('role_list_box').hide();

    $('group_input_box').show();

    disable_save_btn();
    disable_delete_btn();
}

function show_new_alias_form()
{
    show_alias_form();

    $('role_list_box').hide();

    $('alias_input_box').show();

    disable_save_btn();
    disable_delete_btn();
}

function add_members()
{
    member_list = document.main_form.member_list;
    not_member_list = document.main_form.not_member_list;

    addlist = new Array();
    rawinput = document.main_form.not_member_input;
    for (var i=0; i < not_member_list.options.length; i++)
    {
        if (not_member_list.options[i].selected)
        {
            addlist.push(not_member_list.options[i].value);
            if (not_member_list.options[i].value == rawinput.value)
                rawinput.value = '';
        }
    }
    if (rawinput.value)
    {
        addlist.push(rawinput.value);
        rawinput.value = '';
    }

    for (var i=0; i<addlist.length; i++)
    {
        name = all_users[addlist[i]];
        if (! name) name = addlist[i];
        member_list.options[member_list.options.length] =  new Option(name, addlist[i]);
    }

    enable_save_btn();
    disable_delete_btn();
    refresh_no_member_list();
}

function del_members()
{
    member_list = document.main_form.member_list;

    for (var i=member_list.options.length-1; i>=0; i--)
    {
        if (member_list.options[i].selected)
        {
            member_list.options[i] = null;
        }
    }

    enable_save_btn();
    disable_delete_btn();
    refresh_no_member_list();
}

function get_role_name()
{
    if ($('alias_input_box').visible())
    {
        name = document.main_form.alias_input.value
        if (name.charAt(0) != '&')
            name = '&'+name
    }
    else if ($('group_input_box').visible())
    {
        name = document.main_form.group_input.value
        if (name.charAt(0) != '@')
            name = '@'+name
    }
    else
    {
        name = document.main_form.role_list.value
    }

    return name
}

function refresh_no_member_list()
{
    var all_users_id = new Array();
    rolename = get_role_name();
    member_list = document.main_form.member_list;
    not_member_list = document.main_form.not_member_list;
    not_member_list.options.length = 0;

    for(var id in all_users) all_users_id.push(id);
    all_users_id.sort();

    ml = new Array();
    for (var i=0; i<member_list.options.length; i++)
    {
        ml[i] = member_list.options[i].value;
    }
    ml.sort()

    for (var i=0,j=0,k=0; i<all_users_id.length; i++)
    {
        while(all_users_id[i]>ml[j] && j<ml.length-1)
            j+=1;

        if (all_users_id[i] == ml[j] || all_users_id[i] == rolename)
            continue;

        name = all_users[all_users_id[i]];
        if (!name) name=all_users_id[i];
        not_member_list.options[k] = new Option(name, all_users_id[i]);
        k+=1;
    }
}

function ajax_refresh_group_form(code)
{
    var id = new Array();
    var name = new Array();
    var members_count = 0;
    var revision = '';

    member_list = document.main_form.member_list;
    member_list.options.length = 0;

    try {
        eval(code);
        for (var i=0; i < members_count; i++)
        {
            member_list.options[i] = new Option(name[i], id[i]);
        }
        document.main_form.revision.value = revision;
    }
    catch(exception) {
        alert(exception);
    }
    refresh_no_member_list();
}

function ajax_refresh_alias_form(code)
{
    var aliasname = '';
    var username = '';
    var user_in_list = false;
    var revision = '';

    alias_as_list = document.main_form.alias_as_list;

    try {
        eval(code);
        for (var i=0; i < alias_as_list.options.length; i++)
        {
            if (alias_as_list.options[i].value == username)
            {
                alias_as_list.options[i].selected = true;
                user_in_list = true;
            }
        }
        if (!user_in_list)
        {
            alias_as_list.options[i] = new Option(username, username);
            alias_as_list.options[i].selected = true;
        }
        document.main_form.alias_as_input.value = '';
        document.main_form.revision.value = revision;
    }
    catch(exception) {
        alert(exception);
    }
}

function reset_main_form()
{
    var name = document.main_form.role_list.value;
    var params = {select:name};
    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="get_role_info")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();ajax_reset_main_form(request.responseText);},
            parameters:params
        });
}

function ajax_reset_main_form(code)
{
    var id = new Array();
    var name = new Array();
    var members_count = 0;
    var revision = '';

    role_list = document.main_form.role_list;
    role_list.options.length = 0;

    try {
        eval(code);
        for (var i=0; i < members_count; i++)
        {
            role_list.options[i] = new Option(name[i], id[i]);
        }
        document.main_form.revision.value = revision;
    }
    catch(exception) {
        alert(exception);
    }

    role_changed();
}

function role_changed()
{
    var name = document.main_form.role_list.value;
    var params = {role:name};

    showGlobalMessage();
    if (name.charAt(0) == '@')
        show_group_form();
    else if (name.charAt(0) == '&')
        show_alias_form();
    else
        show_init_form();

    if(name.charAt(0) == '@')
    {
        showNoticesPopup();
        new Ajax.Request(
            '${h.url(controller="role", action="get_role_info")}',
            {asynchronous:true, evalScripts:true, method:'post',
                onComplete:
                    function(request)
                        {hideNoticesPopup();ajax_refresh_group_form(request.responseText);},
                parameters:params
            });

    }
    else if(name.charAt(0) == '&')
    {
        showNoticesPopup();
        new Ajax.Request(
            '${h.url(controller="role", action="get_role_info")}',
            {asynchronous:true, evalScripts:true, method:'post',
                onComplete:
                    function(request)
                        {hideNoticesPopup();ajax_refresh_alias_form(request.responseText);},
                parameters:params
            });
    }
}

function save_group(form)
{
    var rolename = get_role_name();
    var members = "";
    var revision = document.main_form.revision.value;

    for (var i=0; i<form.member_list.length; i++)
    {
        members += form.member_list.options[i].value + ',';
    }

    if (form.autodrop.checked)
        autodrop = 'yes';
    else
        autodrop = '';

    var params = {rolename:rolename, members:members, autodrop:autodrop, revision:revision};

    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="save_group")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();save_group_complete(request.responseText, rolename);},
            parameters:params
        });
}

function save_group_complete(message, rolename)
{
    if (message)
    {
        message = '${_("Update group failed:")}' + message;
        alert(message);
        error_msg(message);
    }
    else
    {
        message = '${_("Update group successfully.")}';
        info_msg(message);
        if (document.main_form.role_list.value == rolename)
        {
            role_changed();
        }
        else
        {
            reset_main_form();
        }
    }
}

function delete_group(form)
{

    var rolename = get_role_name();
    var revision = document.main_form.revision.value;
    var message = "\n\n\n" +
        "_________________________________________________\n\n" +
        "${_('Are you sure to delete group:')} " + rolename + " ?\n" +
        "_________________________________________________\n\n\n"   +
        "${_('Click Ok to proceed, or click cancel')}";

    if (!confirm(message)) return;

    var params = {role:rolename, revision:revision};

    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="delete_group")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();delete_group_complete(request.responseText,rolename);},
            parameters:params
        });
}

function delete_group_complete(message, rolename)
{
    if (message)
    {
        message = '${_("Delete group failed:")}' + message;
        error_msg(message);
    }
    else
    {
        message = '${_("Delete group successfully.")}';
        info_msg(message);
        reset_main_form();
    }
}


function save_alias(form)
{
    aliasname = get_role_name();
    username =  form.alias_as_input.value;
    if (username == '')
    {
        username =  form.alias_as_list.value;
    }

    var params = {aliasname:aliasname, username:username};

    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="save_alias")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();save_alias_complete(request.responseText, aliasname);},
            parameters:params
        });
}

function save_alias_complete(message, aliasname)
{
    if (message)
    {
        message = '${_("Update alias failed:")}' + message;
        error_msg(message);
    }
    else
    {
        message = '${_("Update alias successfully.")}';
        info_msg(message);
        if (document.main_form.role_list.value == aliasname)
        {
            role_changed();
        }
        else
        {
            reset_main_form();
        }
    }
}

function delete_alias(form)
{

    var aliasname = get_role_name();
    var message = "\n\n\n" +
        "_________________________________________________\n\n" +
        "${_('Are you sure to delete alias:')} " + aliasname + " ?\n" +
        "_________________________________________________\n\n\n"   +
        "${_('Click Ok to proceed, or click cancel')}";

    if (!confirm(message)) return;

    var params = {aliasname:aliasname};

    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="delete_alias")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();delete_alias_complete(request.responseText,aliasname);},
            parameters:params
        });
}

function delete_alias_complete(message, aliasname)
{
    if (message)
    {
        message = '${_("Delete alias failed:")}' + message;
        error_msg(message);
    }
    else
    {
        message = '${_("Delete alias successfully.")}';
        info_msg(message);
        reset_main_form();
    }
}

function update_users()
{
    showNoticesPopup();
    new Ajax.Request(
        '${h.url(controller="role", action="update_users")}',
        {asynchronous:true, evalScripts:true, method:'post',
            onComplete:
                function(request)
                    {hideNoticesPopup();update_users_notifier(request.responseText);}
        });
}

function update_users_notifier(message)
{
    info_msg(message);
}

function new_group()
{
    show_new_group_form();

    document.main_form.member_list.options.length = 0;
    document.main_form.group_input.value = '';
    document.main_form.group_input.focus();
    refresh_no_member_list();
}

function new_alias()
{
    show_new_alias_form();

    document.main_form.alias_input.value = '';
    document.main_form.alias_as_list.value = '...';
    document.main_form.alias_input.focus();
}

function do_save(form)
{
    if ($('alias_edit_box').visible())
        save_alias(form);
    else if ($('group_edit_box').visible())
        save_group(form);
    else
        alert("Action not implement.")
}

function do_delete(form)
{
    if ($('alias_edit_box').visible())
        delete_alias(form);
    else if ($('group_edit_box').visible())
        delete_group(form);
    else
        alert("Action not implement.")
}

function enable_save_btn()
{
% if c.is_super_user:
    document.main_form.save_btn.disabled = false;
% else:
    ;
% endif
}

function disable_save_btn()
{
    document.main_form.save_btn.disabled = true;
}

function enable_delete_btn()
{
% if c.is_super_user:
    document.main_form.delete_btn.disabled = false;
% else:
    ;
% endif
}

function disable_delete_btn()
{
    document.main_form.delete_btn.disabled = true;
}

</SCRIPT>


<h2>${_("Role Management")}</h2>

<form name="main_form" method="post">
<input type="hidden" name="revision" value="${c.revision}">
<DIV class=gainlayout>

<div id='role_list_box' class=gainlayout>
<span class="title">
  ${_("Select a role name:")}
</span>
    ${h.select("role_list", "", role_list_opts, onChange='role_changed()', Class="select-fix1")}
% if c.is_super_user:
    <a href="#" onclick='new_group()'><img
        src="${h.url('/img/group.png')}" title="${_("New Group")}" alt="${_("New Group")}"></a>
        ${_("New Group")} &nbsp;&nbsp;
    <a href="#" onclick='new_alias()'><img
        src="${h.url('/img/alias.png')}" title="${_("New Alias")}" alt="${_("New Alias")}"></a>
        ${_("New Alias")} &nbsp;&nbsp;
% if c.ldap_enabled:
    <a href="#" onclick='update_users()'><img
        src="${h.url('/img/ldap_sync.png')}" title="${_("Users update from LDAP")}" alt="${_("Users update from LDAP")}"></a>
        ${_("Users update from LDAP")}
% endif
% endif
</div>

<div id='group_input_box' class=gainlayout>
<span class="title">
  ${_("New group name:")}
</span>
<input type='text' name='group_input' onChange="enable_save_btn()" class="input-fix2">
</div>

<div id='alias_input_box' class=gainlayout>
<span class="title">
  ${_("New alias name:")}
</span>
<input type='text' name='alias_input' onChange="enable_save_btn()" class="input-fix2">
</div>

</DIV>

<DIV class=gainlayout>

<!-- begin: group_edit_box -->
<div id='group_edit_box' class=gainlayout>
<table class="list" width="80%">
<tr class=list width="45%">
  <th align='center'>
  ${_("Members list")}
  </th>
  <th class="hide" width="10%">
  </th>
  <th align='center' width="45%">
  ${_("Other users")}
  </th>
</tr>
<tr>
  <td class="right">
    <select name="member_list" size="10" class="select-col1" multiple></select>
  </td>
  <td class="button">
    <a href='#' onClick='add_members()'><img src="${h.url("/img/left.png")}" title="${_("Add membership")}" alt="${_("Add membership")}"></a>
    <br>
    <a href='#' onClick='del_members()'><img src="${h.url("/img/right.png")}" title="${_("Remove membership")}" alt="${_("Remove membership")}"></a>
    <br>
  </td>
  <td class="left">
    <select name="not_member_list" size="10" class="select-col2" multiple></select><br>
    <img src="${h.url("/img/edit.png")}" title="${_("Manual input")}" alt="${_("Manual input")}">
    <input type="text" name="not_member_input" size="10" maxlength="50" class="input-role">
  </td>
</tr>
<tr>
  <td colspan='3' align='center'>
      <input type="checkbox" name="autodrop" value="yes">
    ${_("Ignore recursive")}
  </td>
</tr>
</table>
</div>
<!-- end: group_edit_box -->

<!-- begin: alias_edit_box -->
<div id='alias_edit_box' class=gainlayout>
<table class="hidden">
<tr>
  <th valign='top'>
    ${_("User name:")}
  </th>
  <td>
    ${h.select("alias_as_list", "", alias_as_list_opts, onChange="enable_save_btn();disable_delete_btn()", Class="select-role")}
    <br>
    &nbsp;&nbsp;
    <img src="${h.url("/img/edit.png")}" title="${_("Manual input")}" alt="${_("Manual input")}">
    <input type="text" name="alias_as_input" size="10" maxlength="50" onChange="enable_save_btn();disable_delete_btn()" class="input-role">
  </td>
</tr>
</table>
</div>
<!-- end: alias_edit_box -->

</DIV>

<!-- begin: action_box -->
<div id='action_box' class=gainlayout>
  <input type="hidden" name="rolename">
  <input type="button" class="input-button" name="save_btn"   value='${_("Save")}'  onClick="do_save(this.form)" ${c.is_super_user or "DISABLED"}>
  <input type="button" class="input-button" name="delete_btn" value='${_("Delete")}' onClick="do_delete(this.form)" ${c.is_super_user or "DISABLED"}>
  <input type="button" class="input-button" name="cancel_btn" value='${_("Cancel")}' onClick="role_changed()" ${c.is_super_user or "DISABLED"}>
</div>
<!-- end: action_box -->

</DIV>

</form>
