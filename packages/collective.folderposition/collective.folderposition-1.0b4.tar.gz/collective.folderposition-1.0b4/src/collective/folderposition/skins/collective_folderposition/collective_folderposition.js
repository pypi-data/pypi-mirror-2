/* Patch folder contents with extra ordering controls */
/*jslint browser: true*/
/*global jQuery: false*/

jQuery(document).ready(function($) {
    if ($('#foldercontents-order-column').length) {
        // This is an orderable folder's folder_contents
        var form = $('form[name="folderContentsForm"]');
        if (form.find('input[name="paths:list"]').length > 1 || $('foldercontents-show-batched').length) {
            form.append(
                '<div id="collective_folderposition_controls"><br style="line-height:0.5em;" /><input class="context" type="submit" name="collective_folderposition:method" value="Up" /> / <input class="context" type="submit" name="collective_folderposition:method" value="Down" /> by <select name="delta:int" id="collective_folderposition_delta"><option>1</option></select> <input class="context" type="submit" name="collective_folderposition:method" value="Top" /> <input class="context" type="submit" name="collective_folderposition:method" value="Bottom" /><div>'
            );
            $('select#collective_folderposition_delta').focus(function(){
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
