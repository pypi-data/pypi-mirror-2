function ping(server) {
    var latency, t0 = new Date();
    var id = setTimeout(function() { ping(server) }, 60000);

    $.ajax({
        dataType: 'jsonp',
        url: server + 'jsonp/ping',
        success: function() {
            clearTimeout(id);
            latency = new Date() - t0;
            setCookie(encodeURIComponent('latency-to-' + server), latency);

            // get catalog
            $.ajax({
                dataType: 'jsonp',
                url: server + 'jsonp/catalog',
                success: function(data, textStatus, jqXHR) {
                    var path_info = document.location.href.substr( root.length+1 );  // where we are inside our app
                    var md5, path, dirname;

                    for (path in data) {
                        md5 = data[path];

                        // is this file inside path_info?
                        if (path.substr(0, path_info.length) == path_info) {
                            path = path.substr( path_info.length );
                            if (path.indexOf('/') == -1) {  
                                addFile(path, md5, server + path_info + path, latency);
                            } else {  
                                dirname = path.substr(0, path.indexOf('/')+1);
                                addDir(dirname, server + path_info + dirname);
                            }
                        }
                    }
                }
            });
        }
    });
}


function addFile(filename, md5, url, latency) {
    var node = document.getElementById(md5);
    if (node) {
        if ($(node).data('latency') > latency) {
            $(node).find('a').attr('href', url + '.html').text(filename);
            $(node).data('latency', latency);
        }
    } else {
        $('table').append(
            '<tr id="' + md5 + '" class="ui-widget-content">' +
            '<td><span class="ui-icon ui-icon-document" style="display: inline-block"></span>' +
            '<a href="' + url + '.html">' + filename + '</a></td></tr>'
        );
        $(node).data('latency', latency);
    }
}


function addDir(dirname, url) {
    var id = 'dir-' + dirname;
    var node = document.getElementById(id);
    if (!node) {
        $('table tr:first').after(
            '<tr id="' + id + '" class="ui-widget-content">' +
            '<td><span class="ui-icon ui-icon-folder-collapsed" style="display: inline-block"></span>' +
            '<a href="' + url + '">' + dirname + '</a></td></tr>'
        );
    }
}


function setCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}


$(document).ready(function(){
    $(servers).each(function(i, server) {
        ping(server);
    });
});
