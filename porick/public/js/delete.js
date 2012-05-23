function setupDeleteClickHandlers() {
    /**
     * Assign click handlers to all approve buttons.
     */
    $('.delete').click(function() { 
        var quote_id = $(this).data('quote_id');
        var button = $(this);
        $.ajax({
            url: '/api/v1/delete/' + quote_id,
            type: 'DELETE',
            success: function(data, status, jqXHR){
                button.addClass(data['status'] + ' deleted');
                if(data['status'] === 'success') {
                    button.parent().parent().parent().parent().parent().fadeOut('slow');
                }
            }
        });
    });
}
