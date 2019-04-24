$(document).ready(function(){
    function showOld() {
        $("div#record_old").find($("input, select")).attr("required", true)
        $("div#record_new").find($("input, select")).attr("required", false)
        $("div#record_new").hide();
        $("div#record_old").show();
    }
    function showNew() {
        $("div#record_old").find($("input, select")).attr("required", false)
        $("div#record_new").find($("input, select")).attr("required", true)
        $("div#record_old").hide();
        $("div#record_new").show();
    }
    if ($("input[type='radio']#hasrecord-yes").checked) {
        showOld()
    }
    else if ($("input[type='radio']#hasrecord-no").checked) {
        showNew()
    }
    else {
        $("input[type='radio']#hasrecord-yes").trigger("select");
        showOld()
    }
    $("input[type='radio'][name='hasrecord']").change(function(){
        var val = $(this).val()
        if (val == "1") {
            showOld()
        }
        else if (val == "0") {
            showNew()
        }
    });
});