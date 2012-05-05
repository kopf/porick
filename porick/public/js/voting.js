function setupVoteClickHandlers() {
    /**
     * Assign click handlers to all voting buttons.
     */
    $('.vote').click(function() { 
        var quote_id = $(this).data('quote_id');
        var direction = '';
        if($(this).attr('class').indexOf('down') >= 0) { 
            direction = 'down';
        } else {
            direction = 'up';
        }
        castVote(quote_id, direction, this);
    });
}

function castVote(quote_id, direction, button) {
    var postdata = {'quote_id': quote_id, 'direction': direction};
    $.ajax({
        url: '/api/vote',
        type: 'POST',
        data: postdata,
        success: function(data, status, jqXHR){
            $(button).addClass(data['status']);
        }
    });
}
