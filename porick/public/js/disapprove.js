function setupDisapproveClickHandlers() {
    /**
     * Assign click handlers to all disapprove buttons.
     */
    $('.disapprove').click(function() { 
        var quote_id = $(this).data('quote_id');
        var button = $(this);
        disapprove_quote(quote_id, button);
    });
}

function disapprove_quote(quote_id, button) {
    $.ajax({
        url: '/api/v1/disapprove/' + quote_id,
        type: 'POST',
        success: function(data, status, jqXHR){
            button.addClass(data['status'] + ' disapproved');
            if(data['status'] === 'success') {
                button.parent().parent().parent().parent().parent().fadeOut('slow');
            } else if(data['status'] === 'error') {
                button.parent().html(data['msg']);
            }
        }
    });
}
