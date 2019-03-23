/*globals $, Morris, gettext, RRule, RRuleSet*/

$(function () {
    if (!$("#seat_category_mapping").length) {
        return;
    }

    function load_mapping_form() {
        var $div = $("#seat_category_mapping");
        $div.html("<div class=\"help-block loading-indicator\"><span class=\"fa fa-cog fa-3x fa-spin\"></span></div>");
        var src = $div.attr("data-src");
        $.get(src + "?plan=" + $("#id_seating_plan").val() + location.search.replace("\?", "&"), function (data) {
            $div.html(data);
        });
    }
    load_mapping_form();
    $("#id_seating_plan").change(load_mapping_form);
});
