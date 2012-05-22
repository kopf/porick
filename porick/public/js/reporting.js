function setupReportingClickHandlers() {
    /**
     * Assign click handlers to all favourite buttons.
     */
    $('.report').click(function() { 
    	var quote_id = $(this).data('quote_id');
        if(!($(this).hasClass('reported'))) {
        	report(quote_id, $(this));
        }
    });
}

function report(quote_id, button) {
	$.ajax({
        url: '/api/v1/report/' + quote_id,
        type: 'PUT',
        success: function(data, status, jqXHR){
            button.addClass(data['status'] + ' reported');
            if(data['status'] === 'success') {
                button.parent().parent().parent().parent().parent().fadeOut('slow');
            }
        }
    });
}