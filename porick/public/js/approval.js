function setupApproveClickHandlers() {
    /**
     * Assign click handlers to all approve buttons.
     */
    $('.approve').click(function() { 
        var quote_id = $(this).data('quote_id');
        var button = $(this);
        $.ajax({
            url: '/api/v1/approve/' + quote_id,
            type: 'POST',
            success: function(data, status, jqXHR){
                button.addClass(data['status'] + ' approved');
                if(data['status'] === 'success') {
                    button.parent().parent().parent().fadeOut('slow');
                }
            }
        });
    });
}

