$(document).ready(function(){
    if ($("#button").length > 0) {
        let val = $("#button").attr("href");
        if (val == "#back") {
            $("#button").click(function(){
                history.back();
            });
        }
    }
    if ($("#button2").length > 0) {
        let val = $("#button2").attr("href");
        if (val == "#back") {
            $("#button2").click(function(){
                history.back();
            });
        }
    }
});