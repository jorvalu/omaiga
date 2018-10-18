// vote form submit
$('.voting-form').on('submit', function(event){
    event.preventDefault();
    var endpoint = $(this).attr('action');
    vote(endpoint);
});

// vote action
function vote(endpoint) {
    $.ajax({
        url : endpoint, 
        type : "POST",
        success: function(result){
        	var link = "#link-" + result.id;
        	$(link).text(result.votes);
        	var button = "#btn-" + result.id;
        	$(button).toggleState();
        },
        error: function(xhr, errmsg, err) {
        	// provide more info about the error to the console
            console.log(xhr.status + ": " + xhr.responseText); 
        },
    });
};

// toggle btn between voted and not voted
$.fn.extend({
    toggleState: function(){
    	$(this).toggleClass("active");
		if ($(this).text() == 'OMG') {
		    $(this).text('Hecho');
		} else {
			$(this).text('OMG');
		}    	
    }
});