$(document).ready(function(){
    var val = $("#button").attr("href");
    if (val == "#back") {
        $("#button").click(function(){
            history.back();
        });
    }
});