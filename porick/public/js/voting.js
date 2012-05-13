/* TODO: CLEAN THIS SHIT UP
 *
 **/ 

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
        if($(this).attr('class').indexOf('voted') >= 0) {
            annulVote(quote_id, direction, this);
        } else {
            castVote(quote_id, direction, this);
        }
    });
}

function castVote(quote_id, direction, button) {
    $.ajax({
        url: '/api/v1/vote/' + direction + '/' + quote_id,
        type: 'PUT',
        success: function(data, status, jqXHR){
            $(button).addClass(data['status'] + ' voted');
            changeScoreCount(button, direction, false);
        }
    });
}

function annulVote(quote_id, direction, button) {
    $.ajax({
        url: '/api/v1/vote/' + direction + '/' + quote_id,
        type: 'DELETE',
        success: function(data, status, jqXHR){
            $(button).removeClass('success error voted');
            changeScoreCount(button, direction, true);
        }
    });
}

function changeScoreCount(button, direction, cancelVote) {
    if(direction == 'up') {
        var scorefield = $(button).next();
        var score = parseInt(scorefield.html());
        if(cancelVote === true) {
            scorefield.html(score - 1);
            var upvotes = parseInt($(button).attr('title')) - 1 + ' upvote';
        } else {
            if($(button).next().next().attr('class').indexOf('voted') > -1) {
                // quote has already been downvoted, remove that downvote
                $(button).next().next().removeClass('voted success error');
                scorefield.html(score + 2);
            } else {
                scorefield.html(score + 1);
            }
            var upvotes = parseInt($(button).attr('title')) + 1 + ' upvote';
        }

        if(parseInt(upvotes) !== 1) {
            upvotes += 's';
        }

        $(button).attr('title', upvotes);
    } else {
        var scorefield = $(button).prev();
        var score = parseInt(scorefield.html());
        if(cancelVote === true) {
            scorefield.html(score + 1);
            var downvotes = parseInt($(button).attr('title')) - 1 + ' downvote';
        } else {
            if($(button).prev().prev().attr('class').indexOf('voted') > -1) {
                // quote has already been upvoted, remove that upvote
                $(button).prev().prev().removeClass('voted success error');
                scorefield.html(score - 2);
            } else {
                scorefield.html(score - 1);
            }
            var downvotes = parseInt($(button).attr('title')) + 1 + ' downvote';
        }

        if(parseInt(downvotes) !== 1) {
            downvotes += 's';
        }

        $(button).attr('title', downvotes);
    }

}

