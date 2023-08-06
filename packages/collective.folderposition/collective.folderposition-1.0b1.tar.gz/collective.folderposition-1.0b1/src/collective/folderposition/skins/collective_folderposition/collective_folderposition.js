/* Patch folder contents with extra ordering controls */
/*jslint browser: true*/
/*global jQuery: false*/

jQuery(document).ready(function($) {
    if ($('#foldercontents-order-column').length) {
        var form = $('form[name="folderContentsForm"]');
        var max_delta = form.find('input[name="paths:list"]').length - 1;
        if (max_delta > 0) {
            var options = '';
            for (var delta=1; delta<=max_delta; delta++) {
                options = options + '<option>' + delta + '</option>';
            }
            form.append(
                '<div id="collective_folderposition_controls"><input class="context" type="submit" name="collective_folderposition:method" value="Up" /> / <input class="context" type="submit" name="collective_folderposition:method" value="Down" /> by <select name="delta:int">' + options + '</select> <input class="context" type="submit" name="collective_folderposition:method" value="Top" /> <input class="context" type="submit" name="collective_folderposition:method" value="Bottom" /><div>'
            );
        }
    }
});
