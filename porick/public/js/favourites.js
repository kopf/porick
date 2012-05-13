function setupFavouritesClickHandlers() {
    /**
     * Assign click handlers to all favourite buttons.
     */
    $('.favourite').click(function() { 
    	var quote_id = $(this).data('quote_id');
        if($(this).hasClass('favourited')) {
        	removeFavourite(quote_id, $(this));
        } else {
        	addFavourite(quote_id, $(this));
        }
    });
}

function removeFavourite(quote_id, button) {
	$.ajax({
        url: '/api/v1/favourite/' + quote_id,
        type: 'DELETE',
        success: function(data, status, jqXHR){
            button.removeClass('success error favourited');
            button.html('O');
        }
    });
}

function addFavourite(quote_id, button) {
	$.ajax({
        url: '/api/v1/favourite/' + quote_id,
        type: 'PUT',
        success: function(data, status, jqXHR){
            button.addClass(data['status'] + ' favourited');
            button.html('N');
        }
    });
}