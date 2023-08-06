var last_folder_entry_action = null;
var show_animations = null;
var current_dir = null;

var focus_name = null;
var new_index_matching_focus_name = null;

var menu_focus_index = 0;
var focus_index = 0;
var num_items = 0;

var icon_urls = {
    'directory': 'htpicker://file_resource?filepath=images/nuvola/gnome-fs-directory-visiting.svg&mime_type=image/svg+xml',
    'video': 'htpicker://file_resource?filepath=images/nuvola/mplayer.svg&mime_type=image/svg+xml',
    'game': 'htpicker://file_resource?filepath=images/nuvola/gamepad.svg&mime_type=image/svg+xml'
};

// TODO: preload the background image too!

var menu_showing = false;
var fullscreen = null;

var icons = {};

var preload_images = function()
{
    for(var key in icon_urls)
    {
        var img = document.createElement('img');
        img.src = icon_urls[key];
        icons[key] = img;
    }
}

var activate = function(fullpath, type, display_name)
{
    if(type == 'directory')
    {
        if(display_name == '&#8593; Parent Folder')
            last_folder_entry_action = 'ascend';
        else
            last_folder_entry_action = 'descend';

        if(show_animations)
        {
            $('#files').hide("slide", {
                'direction': last_folder_entry_action == 'descend' ? 'left' : 'right',
                'mode': 'hide'
            }, 150);
        }

        load_files(fullpath);
    }
    else
    {
        $('#files').hide();
        $.get('htpicker://play_file?fullpath=' + fullpath);
        setTimeout(function() { $('#files').show(); }, 5000);
    }
}

var go_parent_directory = function()
{
    $('#files a').first().click();
}

var move_selection_up = function()
{
    if(menu_showing)
    {
        if(menu_focus_index > 0)
        {
            menu_focus_index--;
            focus_current_menu_item();
        }
    }
    else
    {
        if(focus_index > 0)
        {
            focus_index--;
            focus_current_index();
        }
    }
}

var move_selection_down = function()
{
    if(menu_showing)
    {
        if(menu_focus_index < 1) /* XXX */
        {
            menu_focus_index++;
            focus_current_menu_item();
        }
    }
    else
    {
        if(focus_index < num_items-1)
        {
            focus_index++;
            focus_current_index();
        }
    }
}

var show_menu = function()
{
    if(!menu_showing)
    {
        if(show_animations)
        {
            $('#menu').show("slide", { direction: "right" }, 300, function() {
                focus_current_menu_item();
            });
        }
        else
        {
            $('#menu').show();
            focus_current_menu_item();
        }
    }
    menu_showing = true;
}

var hide_menu = function()
{
    if(menu_showing)
    {
        focus_current_index();
        if(show_animations)
            $('#menu').hide("slide", { direction: "right" }, 300);
        else
            $('#menu').hide();
    }
    menu_showing = false;
}

var focus_current_menu_item = function()
{
    $('#menu a').eq(menu_focus_index).focus();
}

var focus_current_index = function()
{
    var el = $('#file-'+focus_index);
    el.focus();
    focus_name = el.attr('data-fullpath');
}

var activate_current_selection = function()
{
    $('#file-'+focus_index).click();
}

var scrollCentered = function(el, percentage, sweep_pct)
{
    var win = $(window);
    var sweep_area = win.height() * sweep_pct;

    // *0.5 because half of the buffer goes above
    // and the other half implicitly goes below
    var modifier = -(percentage * sweep_area - sweep_area/2);

    var offset = el.offset().top - win.height()/2 + el.outerHeight()/2 + modifier;
    win.scrollTop(offset);
}

var scroll_to_focus = function()
{
    var el = $('#file-'+focus_index);
    // XXX in certain unusual circumstances, like maybe when first starting up,
    // el is non-null, but el.offset() is null.  why is that?
    if(!el.offset())
        return;
    var percentage = 1.0 * focus_index / num_items;
    scrollCentered(el, percentage, 0.5);
}

var load_files = function(path) {
    if(path)
        current_dir = path;
    else
        last_folder_entry_action = 'load';

    $.getJSON('htpicker://list_files?directory=' + encodeURIComponent(current_dir), function(data) {
        var files = data['files'];
        $('#files').html('');
        new_index_matching_focus_name = null;
        num_items = files.length;
        for(var i = 0; i < num_items; i++)
        {
            var focusin_cb = function(i, num_items) {
                return function(ev) {
                    focus_index = i;
                    $('#files').show();
                    $('#file-'+focus_index).addClass("ui-state-active");
                    scroll_to_focus();
                };
            }(i, num_items);

            var focusout_cb = function(i) {
                return function(ev) {
                    $('#file-'+i).removeClass("ui-state-active");
                };
            }(i);

            var icon_name = files[i]['icon'];
            var icon_url = icon_name ? icons[icon_name].src : '';

            var item = (
                $('<a>')
                    .attr('id', 'file-'+i)
                    .attr('class', 'ui-widget-header item')
                    .focusin(focusin_cb)
                    .focusout(focusout_cb)
                    .attr('href', '#')
                    .attr('data-fullpath', files[i]['fullpath'])
                    .click(function(file) {
                        return function(ev) {
                            activate(file['fullpath'], file['type'], file['display_name']);
                        };
                    }(files[i]))
                    .html('<img src="' + icon_url + '"> <span>' + files[i]['display_name'] + '</span>')
            );

            if(files[i]['fullpath'] == focus_name)
                new_index_matching_focus_name = i;

            $('#files').append(item);
        }

        if(show_animations && (last_folder_entry_action == 'ascend' || last_folder_entry_action == 'descend'))
        {
            // ascend/descend
            focus_index = 0;
            $('#files').show("slide", {
                'direction': last_folder_entry_action == 'descend' ? 'right' : 'left',
                'mode': 'show'
            }, 250, function() { $('#files > a')[0].focus(); });
        }
        else
        {
            if(path)
            {
                // initial load
                focus_index = 0;
                focus_current_index();
            }
            else
            {
                // refresh
                if(new_index_matching_focus_name != null)
                    focus_index = new_index_matching_focus_name;
                focus_current_index();
                scroll_to_focus();
            }
        }
    });
}

$(function() {
    preload_images();

    $('#fullscreen-toggle').click(function(ev) {
        if(fullscreen)
        {
            $('#fullscreen-checkbox').html('');
            $.get('htpicker://disable_fullscreen');
        }
        else
        {
            $('#fullscreen-checkbox').html('&#x2714;');
            $.get('htpicker://enable_fullscreen');
        }
        fullscreen = !fullscreen;
    });

    $('#exit').attr('href', 'htpicker://exit');

    $('#menu a').focusin(function(ev) {
        $(this).parent().addClass("ui-state-hover");
    });

    $('#menu a').focusout(function(ev) {
        $(this).parent().removeClass("ui-state-hover");
    });

    $(document).keydown(function(ev) {
        if(ev.which == $.ui.keyCode.DOWN)
        {
            move_selection_down();
            return false;
        }
        if(ev.which == $.ui.keyCode.UP)
        {
            move_selection_up();
            return false;
        }
        if(ev.which == $.ui.keyCode.RIGHT)
        {
            show_menu();
            return false;
        }
        if(ev.which == $.ui.keyCode.LEFT)
        {
            hide_menu();
            return false;
        }
    });

    $(window).resize(function () { scroll_to_focus(); });
});

// run this at .load() so preloaded images are guaranteed to be loaded.
$(window).load(function() {
    $.ajax({
        'url': 'htpicker://get_startup_config',
        'dataType': 'json',
        'async': false,
        'success': function(data) {
            show_animations = data['show_animations'];
            fullscreen = data['fullscreen'];
            $('#fullscreen-checkbox').html(fullscreen ? '&#x2714;' : '');
            load_files(data['initial_dir']);
        }
    });
});
