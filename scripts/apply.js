$(document).ready(function(){
    $("input[type='radio']#hasrecord-yes").trigger("select");
    $("div#record_old").find($("input, select")).attr("required", true)
    $("div#record_new").find($("input, select")).attr("required", false)
    $("div#record_old").show();
    $("div#record_new").hide();
    $("input[type='radio'][name='hasrecord']").change(function(){
        var val = $(this).val()
        if (val == "1") {
            $("div#record_old").find($("input, select")).attr("required", true)
            $("div#record_new").find($("input, select")).attr("required", false)
            $("div#record_new").hide();
            $("div#record_old").show();
        }
        else if (val == "0") {
            $("div#record_new").find($("input, select")).attr("required", true)
            $("div#record_old").find($("input, select")).attr("required", false)
            $("div#record_old").hide();
            $("div#record_new").show();
        }
    });
});