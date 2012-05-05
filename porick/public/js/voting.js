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
    $.ajax({
        url: '/api/vote/' + direction + '/' + quote_id,
        type: 'PUT',
        success: function(data, status, jqXHR){
            $(button).addClass(data['status']);
            incrementScoreCount(button, direction);
        }
    });
}

function incrementScoreCount(button, direction) {
    if(direction == 'up') {
        var scorefield = $(button).next();
        var score = parseInt(scorefield.html());
        scorefield.html(score + 1);

        var upvotes = parseInt($(button).attr('title')) + 1 + ' upvotes';
        $(button).attr('title', upvotes);
    } else {
        var scorefield = $(button).prev();
        var score = parseInt(scorefield.html());
        scorefield.html(score - 1);

        var downvotes = parseInt($(button).attr('title')) + 1 + ' downvotes';
        $(button).attr('title', downvotes);
    }

}
