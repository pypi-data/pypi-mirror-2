var CURRENT_OVERLAY = null;
var OVERLAYS = [];
/**
 * Cookie plugin
 *
 * Copyright (c) 2006 Klaus Hartl (stilbuero.de)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 * http://plugins.jquery.com/files/jquery.cookie.js.txt
 */
jQuery.cookie = function(name, value, options) {
    if (typeof value != 'undefined') { // name and value given, set cookie
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
        }
        // CAUTION: Needed to parenthesize options.path and options.domain
        // in the following expressions, otherwise they evaluate to undefined
        // in the packed version for some reason...
        var path = options.path ? '; path=' + (options.path) : '';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else { // only name given, get cookie
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};


(function($){    
$(document).ready(function(){
    
    var spinner = $("#kss-spinner");
    var nortstar_container = $("#northstar-container");
    
    var is_advanced_mode = function(){
        return $.cookie("northstar-advanced") == "true";
    }
    
    var set_advanced_mode = function(advanced){
        if(advanced){
            $(".advanced").show();
            $.cookie("northstar-advanced", true, { expires : 365 });
        }else{
            $(".advanced").hide();
            $.cookie("northstar-advanced", null);
        }
    }
    
    //display our status message in a pretty way.
    var status_message = function(msg){
        var status = $('#status-messages');
        status.html(msg);
        status.fadeIn('slow', function(){
            setTimeout("jQuery('#status-messages').fadeOut('slow');", 3000);
        });
    }

    //returns the url for a given workflow
    var get_url = function(){
        var url = $('base').attr('href') + "@@uwosh-northstar";
        var ele = jq("input[name='selected-workflow']");
        if(ele.size() > 0){
            url = url + "?selected-workflow=" + ele.val();
        }
        return url;
    }
    
    //get the variables encoded in a url
    var get_url_vars = function(url){
        var vars = {}, hash;
        var hashes = url.slice(url.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars[hash[0]] = hash[1];
        }
        return vars;
    }
    
    // goes directly to a state or transition
    // the state or transition are encoded in
    // the url with ?selected-state=foobar
    var goto_item = function(url){
        var vars = get_url_vars(url);
        
        var transitions_button = $("a#fieldsetlegend-transitions");
        var states_button = $("a#fieldsetlegend-states");
        var transitions = $("#fieldset-transitions");
        var states = $('#fieldset-states');
        
        if(CURRENT_OVERLAY != null && CURRENT_OVERLAY.isOpened()){
            CURRENT_OVERLAY.close();
        }
        
        var prefix = "#";
        
        if(vars['selected-state'] != undefined){
            prefix += "state-" + vars['selected-state'];
            if(!states_button.hasClass('selected')){
                states.show();
                transitions.hide();
                states_button.addClass('selected');
                transitions_button.removeClass('selected');
            }
        }else if(vars['selected-transition'] != undefined){
            prefix += "transition-" + vars['selected-transition'];
            if(!transitions_button.hasClass('selected')){
                transitions.show();
                states.hide();
                transitions_button.addClass('selected');
                states_button.removeClass('selected');
            }
        }else{
            return;
        }
    
        var obj = $(prefix);
        
        if(obj.hasClass('collasped')){
            obj.find('.hidden-content').slideDown();
            show_item(obj);
        }
        
        var offset = obj.offset().top - 50;
        $('html,body').animate({scrollTop: offset}, 1000);
    }
    
    var has_dirty_items = function(){
        var dirty_items = $("div.workflow-item.dirty");
        return dirty_items.size() > 0;
    }
    
    var strip_vars = function(url){
        return url.substring(0, url.lastIndexOf("?"));
    }

    // Our overlay settings that automatically load remote content
    // and clear it out when it closes
    var overlay_settings = {    
        onBeforeLoad: function() { 
            spinner.show();
            CURRENT_OVERLAY = this;
            var wrap = $('#contentWrap');
            var trigger = this.getTrigger();
            var url = trigger.attr("href");
            var data = get_url_vars(url);
            data['ajax'] = true;
            
            url = strip_vars(url);
            
            if(trigger.hasClass('save-first') && has_dirty_items() && confirm("You have unsaved changes. Would you like to save them before you preceed?")){
                save(function(){
                    status_message("The workflow been successfully updated.");
                });
            }
            wrap.load(url, data, function(){
                $(this).find('div.dialog-box').addClass(CURRENT_OVERLAY.getTrigger().attr('class'));
                spinner.hide();
            });
        },
        expose: { 
            color: '#333', 
            opacity: 0.7,
            maskId : 'overlay-mask'
        },
        top : 0,
        closeOnClick: false,
        onClose : function(){
            $('#contentWrap').html(""); //clear it out
        }
    };

    var setup_overlays = function(){
        OVERLAYS = [];
        $('a.dialog-box').each(function(){
            OVERLAYS[OVERLAYS.length] = $(this).overlay(overlay_settings);
        });
    }

    var retrieve_selected_workflow = function(){
        return $("#selected-workflow").val();
    }

    var retrieve_form_data = function(form){
        form = $(form);

        var input_tags = form.find('input');
        var data = {};

        for(var i=0; i < input_tags.length; i++){
            var input = $(input_tags[i]);
            
            var type = input[0].type;
            if(type != undefined){
                if(type.toLowerCase() == 'checkbox'){
                    if(input[0].checked){
                        data[input.attr('name')] = input.val();
                    }
                }else if(type == "text" || type == "hidden"){
                    data[input.attr('name')] = input.val();
                }
            }
        }
        
        var option_tags = form.find('select');
        
        for(var i=0; i < option_tags.size(); i++){
            var tag = option_tags.eq(i);
            var options = tag.find('option:selected');
            var res = '';
            
            for(var j=0; j < options.size(); j++){
                var option = options.eq(j);
                res += option.attr('value') + ',';
            }
            
            if(res.length > 0){
                res = res.substring(0, res.length-1); //remove comma
                data[tag.attr('name')] = res;
            }
            
        }
        
        var textarea_tags = form.find('textarea')
        for(var i=0; i < textarea_tags.size(); i++){
            var tag = textarea_tags.eq(i);
            data[tag.attr('name')] = tag.val();
        }

        if(data['selected-workflow'] == undefined){
            data['selected-workflow'] = retrieve_selected_workflow();
        }
        
        data['ajax'] = 'true';
        return data;
    }
    
    var show_item = function(obj){
        obj = $(obj);
        obj.find('.arrow').html('&#x2191;');
        obj.removeClass('collasped');
        obj.addClass('expanded');
    }
    
    var hide_item = function(obj){
        obj = $(obj);
        obj.find('.arrow').html('&#x2193;');
        obj.removeClass('expanded');
        obj.addClass('collasped');
    }
    
    var parse_data = function(data){
        if(typeof data == "string"){
            try{//try to parse if it's not already done...
                data = $.parseJSON(data);
            }catch(e){
                try{
                    data = eval("(" + data + ")");
                }catch(e){
                    //do nothing
                }
            }
        }
        return data
    }
    
    var handle_actions = function(data){
        data = parse_data(data)
        if(data.status != undefined){
            
            if(data.status == 'slideto'){
                goto_item(data.url);
            }
        }
    }
    
    var reload = function(data){
        $.ajax({
            url : '@@uwosh-northstar-content',
            data : {'selected-workflow' : retrieve_selected_workflow()},
            type : 'POST',
            complete : function(request, textStatus){
                var items = $('.workflow-item');
                var expanded_ids = [];
                var collasped_ids = [];
                
                for(var i = 0; i < items.length; i++){
                    var item = items.eq(i);
                    var id = item.attr('id');
                    
                    if(id.length > 0){
                        if(item.hasClass('expanded')){
                            expanded_ids[expanded_ids.length] = id;
                        }else{
                            collasped_ids[collasped_ids.length] = id;
                        }
                    }
                }

                $('#workflow-content').replaceWith(request.responseText);
                setup_overlays();
                
                if(!is_advanced_mode()){
                    $('.advanced').hide();
                }
                
                for(var i = 0; i < expanded_ids.length; i++){
                    var obj = $("#" + expanded_ids[i]);
                    obj.find('.hidden-content').css('display', 'block');
                    show_item(obj);
                }
                for(var i = 0; i < collasped_ids.length; i++){
                    var obj = $("#" + collasped_ids[i]);
                    obj.find('.hidden-content').css('display', 'none');
                    hide_item(obj);
                }
                
                //for .workflow-item that are neither shown or collasped
                //but shown by default because that's how they come from
                //the server, just show
                jq('div.collasped.workflow-item div.hidden-content:visible').each(function(){
                    var obj = $(this).parent('div.workflow-item');
                    show_item(obj);
                });
                
                var transitions = $("#fieldset-transitions");
                var transitions_button = $("a#fieldsetlegend-transitions");
                var states = $("#fieldset-states");
                var states_button = $("a#fieldsetlegend-states");
                
                if(transitions_button.hasClass('selected')){
                    states.css('display', 'none');
                }else{
                    transitions.css('display', 'none');
                }
                
                handle_actions(data);
                $("#unsaved-warning").fadeOut();
            }
        });
    }
    
    var save = function(finish){
        var dirty_items = $("div.workflow-item.dirty");
        
        var request_count = 0;
        for(var i=0; i < dirty_items.length; i++){
            var item = dirty_items.eq(i);
            var form = item.find('form');
            var data = retrieve_form_data(form);
            $.ajax({
                url : form.attr('action'),
                data : data,
                type: 'POST',
                success : function(data){
                    request_count += 1;
                    if(request_count == dirty_items.length){
                        reload(data);
                        finish(data);
                    }
                }
            });
        }
        
        if(dirty_items.length == 0){
            //clear it out even if nothing is saved...
            spinner.hide();
            $("#unsaved-warning").hide();
        }
    }
    
    $('.workflow-item h3.header span.arrow').live('click', function(e){
        var obj = $(this).parent().parent();
        if(obj.hasClass('collasped')){
            obj.find('.hidden-content').slideDown();
            show_item(obj);
        }else{
            obj.find('.hidden-content').slideUp();
            hide_item(obj);
        }
        return e.preventDefault();
    });

    $("a#fieldsetlegend-states").live('click', function(e){
        
        var transitions = $("#fieldset-transitions");
        var transitions_button = $("a#fieldsetlegend-transitions");
        var states = $("#fieldset-states");
        var states_button = $(this);
        
        if(transitions_button.hasClass('selected')){
            transitions_button.removeClass('selected');
            nortstar_container.css('height', nortstar_container.height());
            transitions.fadeOut('fast', function(){
                states.fadeIn('fast', function(){
                    nortstar_container.css('height', '');
                });
                states_button.addClass('selected');
            });
        }else if(!states_button.hasClass('selected')){
            states.fadeIn('fast');
            states_button.addClass('selected');
        }
        return e.preventDefault();;
    });
    
    $("a#fieldsetlegend-transitions").live('click', function(e){
        
        var transitions = $("#fieldset-transitions");
        var transitions_button = $(this);
        var states = $("#fieldset-states");
        var states_button = $("a#fieldsetlegend-states");
        
        if(states_button.hasClass('selected')){
            states_button.removeClass('selected');
            nortstar_container.css('height', nortstar_container.height());
            states.fadeOut('fast', function(){
                transitions.fadeIn('fast', function(){
                    nortstar_container.css('height', '');
                });
                transitions_button.addClass('selected');
            });
        }else if(!transitions_button.hasClass('selected')){
            transitions.fadeIn('fast');
            transtiions_button.addClass('selected');
        }
        return e.preventDefault();;
    });

    $('#save-all-button,input.save-all').live('click', function(e){
        spinner.show();
        
        save(function(){
            status_message("The workflow been successfully updated.");
            spinner.hide();
        });
        
        return e.preventDefault();
    });
    
    var ajax_form = function(form, e, callback){
        var data = retrieve_form_data(form);

        $.ajax({
            url : form.attr('action'),
            context : form,
            data : data,
            success : function(data){
                var form = this;
                data = parse_data(data);
                
                if(data.status == undefined){
                    callback(data);
                }else if(data.status == 'error'){
                    form.find('div.fieldErrorBox').remove();
                    form.find('div.field.error').removeClass('error');
                    
                    for(var i = 0; i < data.errors.length; i++){
                        var error_obj = data.errors[i];
                        var input_name = error_obj[0];
                        var error_msg = error_obj[1];
                        
                        var input = form.find("input[name='" + input_name + "'],textarea[name='" + input_name + "']");
                        
                        if(!input.parent().hasClass('error')){
                            input.before('<div class="fieldErrorBox">' + error_msg + '</div>');
                            input.parent().addClass('error');
                        }
                    }
                    status_message("You have errors that you need to correct.");
                    spinner.hide();
                }else if(data.status == 'redirect'){
                    window.location = data.location;
                }else if(data.status == 'load'){
                    $.ajax({
                        url : data.url,
                        complete : function(request, textStatus){
                            $('#contentWrap').html('');//clear it first
                            $('#contentWrap').wrapInner($(request.responseText).find('#content'));
                            spinner.hide();
                        }
                    });
                }else{
                    if(data.message != undefined){
                        status_message(data.message);
                    }
                    callback(data);
                }
            }
        });
    }
    
    $("div.dialog-box form input[type='submit'],#content form fieldset div input[type='submit']").live('click', function(e){
        var submit = $(this);
        var form = submit.parents('form');
        var hidden_value = form.find('input.submitvalue');
        if(hidden_value.size() == 0){
            form.append('<input type="hidden" class="submitvalue" />');
            hidden_value = form.find('input.submitvalue');
        }
        
        hidden_value.attr('name', submit.attr('name'));
        hidden_value.attr('value', submit.attr('value'));
        
        spinner.show();
        ajax_form(form, e, function(data){
            if(CURRENT_OVERLAY == null){
                window.location = get_url();
                return;
            }
            CURRENT_OVERLAY.close();
            
            reload(data);
            spinner.hide();
        });
        return e.preventDefault();
    });
    
    $('a.goto-link').live('click', function(e){
        var link = $(this);
        goto_item(link.attr('href'));
        return e.preventDefault();
    });
    
    $('input.one-or-the-other').live('change', function(){
        if(this.checked){
            $(this).siblings('input.the-other').eq(0)[0].disabled = true;
        }else{
            $(this).siblings('input.the-other').eq(0)[0].disabled = false;
        }
    });
    
    
    //all the initial page load stuff goes here.
    var init = function(){
        setup_overlays();    
        $('div.hidden-content').css('display', 'none'); // since we don't hide it by default for js disable browsers
        $("#fieldset-transitions").css('display', 'none');
        $("a#fieldsetlegend-states").addClass('selected');

        // check if the user wanted to go directly to a certain
        // state or transition    
        goto_item(window.location.href);

        //enable advanced mode on page load
        //so it isn't available for non-js users--oh well.
        var toppanel = $("#tabs-menu ul.formTabs");
        toppanel.append('<div id="advanced-mode" class="widget"><input type="checkbox" name="advanced-mode" class="checkboxType"><label for="advanced-mode">Advanced mode</label></div>');
        
        toppanel.find("div#advanced-mode input").change(function(){
            set_advanced_mode(this.checked);
        });

        if(is_advanced_mode() && toppanel.size() == 1){
            $("#tabs-menu ul.formTabs div#advanced-mode input")[0].checked = true;
        }else{
            $(".advanced").hide();
        }

        //Content change listeners to mark things as dirty and needing to be saved...
        $("div.workflow-item input[type=text],div.workflow-item input[type=checkbox],div.workflow-item textarea,div.workflow-item select").live('change', function(){
            var obj = $(this);
            obj.parents('div.workflow-item').addClass('dirty');
            $("#unsaved-warning").fadeIn();
        });

        //Set some things up only if js is enabled here
        $("#save-all-button").css('display', 'inline');
        $("#tabs-menu ul.formTabs").addClass('enabled');
        
        //do some css fixes based on theme installed
        //I know--kind of weird to do it this way....
        var resources = $('link');
        var is_sunburst = false;
        for(var i=0; i < resources.length; i++ ){
            if(resources.eq(i).attr('href').indexOf('Sunburst') != -1){
                is_sunburst = true;
                break;
            }
        }

        if(is_sunburst){
            $("#northstar-container input").css('padding', '2px');
        }else{
            $("#northstar-container input").css('background-color', 'white');
        }
            
        $(window).scroll(function(e){
            var menu_container = $('div#tabs-menu');
            var container_offset = menu_container.offset();
            
            var tabs_menu = menu_container.find("ul.formTabs");
            var offset = tabs_menu.offset();
            
            if(window.pageYOffset > container_offset.top){
                if(tabs_menu.css('position') != 'fixed'){
                    tabs_menu.css('position', 'fixed');
                    tabs_menu.css('width', '97%');
                }
            }else{
                if(tabs_menu.css('position') == 'fixed'){
                    tabs_menu.css('position', 'inherit');
                    tabs_menu.css('width', '');
                }
            }
            
        });
        
    }
    
    init();
    
}); 
})(jQuery);
