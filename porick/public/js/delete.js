function setupDeleteClickHandlers() {
    /**
     * Assign click handlers to all delete buttons.
     */
    $('.delete').click(function() { 
        var quote_id = $(this).data('quote_id');
        var button = $(this);
        if(confirm("Do you really want to delete this quote?")) {
            delete_quote(quote_id, button, 'DELETE');
        }
    });
}

function setupDisapproveClickHandlers() {
    /**
     * Assign click handlers to all disapprove buttons.
     */
    $('.delete').click(function() { 
        var quote_id = $(this).data('quote_id');
        var button = $(this);
        delete_quote(quote_id, button, 'POST');
    });
}

function delete_quote(quote_id, button, method) {
    $.ajax({
        url: '/api/v1/delete/' + quote_id,
        type: method,
        success: function(data, status, jqXHR){
            button.addClass(data['status'] + ' deleted');
            if(data['status'] === 'success') {
                button.parent().parent().parent().parent().parent().fadeOut('slow');
            } else if(data['status'] === 'error') {
                button.parent().html(data['msg']);
            }
        }
    });
}