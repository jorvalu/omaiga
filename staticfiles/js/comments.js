//  vote positive submit
$('.points-form').on('submit', function(event){
    event.preventDefault();
    var endpoint = $(this).attr('action');
    var value = $(this).find('#value').val();
    point(endpoint, value);
});

// vote positive action
function point(endpoint, value) {
    $.ajax({
        url : endpoint, 
        type : "POST",
        data: {value : value},
        success: function(result) {
            console.log(result); 
            // give feedback
            var feedback = "#comment-" + result.id + "-actions";
            if (value == 1) {
                $(feedback).text("POSITIVO · ");
            } else {
                $(feedback).text("NEGATIVO · ");
            }
            // update scores
            var scoreboard = "#comment-" + result.id + "-scores";
            var score = "total " + result.total + " · " + "karma " + result.karma;
            $(scoreboard).text(score);
        },
        error: function(xhr, errmsg, err) {
            // provide more info about the error to the console
            console.log(xhr.status + ": " + xhr.responseText); 
        },
    });
};
