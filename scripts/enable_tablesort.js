$(document).ready(function(){
    // initialize dropdowns & radio buttons
    $('select.dropdown').dropdown();
    $('.ui.dropdown').dropdown();
    $('.ui.radio.checkbox').checkbox();
    
    // initialize sortable tables
    f = $.tablesort.defaults.compare
    g = function(a,b) {
        if (typeof a == "string" && typeof b == "string") {
            a = a.toLowerCase();
            b = b.toLowerCase();
        }
        return f(a,b)
    }
    $.tablesort.defaults.compare = g
    $('table').tablesort().each(function(){
        $(this).data('tablesort').sort($("th.default-sort"))
    });
});