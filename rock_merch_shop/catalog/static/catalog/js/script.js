// This script is responsible for the functionality of the star rating system in the application.
$(document).ready(function(){
    /*
     Retrieve the CSRF token from the meta tag in the HTML document.
     This token is used for security purposes to protect against Cross-Site Request Forgery attacks.
     */
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    /*
     Attach a click event listener to elements with the class `rating-star`.
     This event is triggered when a star is clicked.
     */
    $('.rating-star').click(function(){
        // Retrieve the `data-value` and `data-itemid` attributes of the clicked star.
        // `data-value` represents the score associated with the clicked star.
        // `data-itemid` represents the ID of the item being rated.
        var score = $(this).data('value');
        var item_id = $(this).data('itemid');
        console.log("Star clicked: ", score);
        console.log("Item ID: ", item_id);

    // Iterate over all the stars.
    // If a star's `data-value` is less than or equal to the score of the clicked star,
    // the `selected` class is added to it. This is used to visually highlight the selected rating.
    $('.rating-star').each(function() {
        if ($(this).data('value') <= score) {
            $(this).addClass('selected');
            console.log("Adding class to: ", $(this).data('value'));
        } else {
            $(this).removeClass('selected');
        }
    });
        // This block of code is responsible for making an AJAX request to the server to submit the user's rating.
        $.ajax({
            // The URL to which the request is sent.
            url: submitRatingUrl,
            // The data to be sent to the server.
            // This includes the ID of the item being rated (`item_id`), the score given by the user (`score`),
            // and a CSRF token for security purposes (`csrfmiddlewaretoken`)
            data: {
                'item_id': item_id,
                'score': score,
                'csrfmiddlewaretoken': csrfToken
            },
            // Specifies that this is a POST request.
            type: 'POST',
            // A function that is executed if the server responds with a status of success.
            success: function(response) {
                // If the response from the server indicates success, the stars are highlighted again for immediate feedback to the user,
                // and an alert is shown thanking the user for their rating.
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
                    // If the response from the server indicates an error, an alert is shown
                    // indicating that there was an error processing the rating.
                    alert("There was an error processing your rating.");
                }
            }
        });
    });
});

