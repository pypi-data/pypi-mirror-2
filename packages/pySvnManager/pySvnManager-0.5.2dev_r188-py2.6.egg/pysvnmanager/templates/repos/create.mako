## -*- coding: utf-8 -*-
## vim: et ts=4 sw=4
<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>${_("Create repository")}</title>
</%def>

<h2>${_("Create repository")}</h2>

##<form name="main_form" method="post" action="${h.url(controller="repos", action="create_submit")}">

<form action="${h.url(controller="repos", action='create_submit')}"
  id="main_form" method="POST"
  onsubmit="showNoticesPopup();
            new Ajax.Request(
                '${h.url(controller="repos", action='create_submit')}',
                {
                 asynchronous:true, evalScripts:true, method:'post',
                 onFailure:
                    function(request)
                        {set_message_box(request.responseText, 'error');},
                 onSuccess:
                    function(request)
                        {set_message_box_json(request.responseText);},
                 onComplete:
                    function(request)
                        {hideNoticesPopup();},
                 parameters:Form.serialize(this)
                });
            return false;">

<span class="title">
  ${_("Repository name:")}
</span>
    <input type="text" name="reposname" value="" class="input-repos">
    <br>
    <input type="submit" name="submit" value="${_("Create repository")}" class="input-button">

</form>
