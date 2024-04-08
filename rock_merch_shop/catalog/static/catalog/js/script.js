$(document).ready(function(){

    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    $('.rating-star').click(function(){
        var score = $(this).data('value');
        var item_id = $(this).data('itemid');
        console.log("Star clicked: ", score);
        console.log("Item ID: ", item_id);

    // Highlight all the stars that should be selected
    $('.rating-star').each(function() {
        if ($(this).data('value') <= score) {
            $(this).addClass('selected');
            console.log("Adding class to: ", $(this).data('value'));
        } else {
            $(this).removeClass('selected');
        }
    });

        $.ajax({
            url: submitRatingUrl,
            data: {
                'item_id': item_id,
                'score': score,
                'csrfmiddlewaretoken': csrfToken
            },
            type: 'POST',
            success: function(response) {
                if(response.success){
                    // Highlight the stars again here for immediate feedback
                    $('.rating-star').each(function() {
                        if ($(this).data('value') <= score) {
                            $(this).addClass('selected');
                        } else {
                            $(this).removeClass('selected');
                        }
                    });
                    alert("Thank you for your rating!");
                } else {
                    alert("There was an error processing your rating.");
                }
            }
        });
    });
});

