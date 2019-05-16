$(document).ready(function(){
    $('.ui.button.approve_modal').each(function(){
        let modal_id = $(this).data("modal-id");
        $(this).click(function(){
            $("#"+modal_id).modal('show');
        });
        console.log("approve:"+modal_id);
    });
    
    $('.ui.button.cancel_modal').each(function(){
        let modal_id = $(this).data("modal-id");
        $(this).click(function(){
            $("#"+modal_id).modal('hide');
        });
        console.log("cancel:"+modal_id);
    });
});