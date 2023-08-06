/* Patch folder contents with extra ordering controls */
/*jslint browser: true*/
/*global jQuery: false, window: false*/

jQuery(document).ready(function($) {
    if ($('#foldercontents-order-column').length) {
        // This is an orderable folder's folder_contents
        var form = $('form[name="folderContentsForm"]');
        var paths = form.find('input[name="paths:list"]');
        // check any checkboxes listed in the query string
        var search = window.location.search.substring(1);
        var selected_paths = {};
        $.each(search.split('&'), function(index, param) {
            var key_value = param.split('=');
            if (key_value[0] == 'paths:list') {
                selected_paths[key_value[1]] = true;
            }
        });
        paths.each(function() {
            if (selected_paths[this.getAttribute('value')]) {
                this.setAttribute('checked', 'checked');
            }
        });
        // Add the extra controls
        if (paths.length > 1 || $('foldercontents-show-batched').length) {
            form.append(
                '<div id="collective_folderposition_controls"><br style="line-height:0.5em;" /><input class="context" type="submit" name="collective_folderposition:method" value="Up" /> / <input class="context" type="submit" name="collective_folderposition:method" value="Down" /> by <select name="delta:int" id="collective_folderposition_delta"><option>1</option></select> <input class="context" type="submit" name="collective_folderposition:method" value="Top" /> <input class="context" type="submit" name="collective_folderposition:method" value="Bottom" /><div>'
            );
            // Populate the select when focused
            $('select#collective_folderposition_delta').focus(function() {
                var select = $(this);
                var selected = select.find('option[selected]').text();
                select.empty();
                var max_delta = form.find('input[name="paths:list"]').length - 1;
                var options = [];
                for (var delta=1; delta<=max_delta; delta++) {
                    if (delta == selected) {
                        options.push('<option selected="selected">');
                    } else {
                        options.push('<option>');
                    }
                    options.push(delta);
                    options.push('</option>');
                }
                select.append(options.join(''));
            });
        }
    }
});
