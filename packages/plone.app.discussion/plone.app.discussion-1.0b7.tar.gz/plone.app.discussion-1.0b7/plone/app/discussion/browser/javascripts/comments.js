/**************************************************************************
 * Remove all error messages and field values from the form that is passed
 * to the function.
 **************************************************************************/
function clearForm(form_div) {
    form_div.find(".error").removeClass("error");
    form_div.find(".fieldErrorBox").remove();
    form_div.find("input[type='text']").attr("value", "");
    form_div.find("textarea").attr("value", "");
    /* XXX: Clean all additional form extender fields. */
}


/**************************************************************************
 * Create a reply-to-comment form right beneath the form that is passed to
 * the function. We do this by copying the regular comment form and 
 * adding a hidden in_reply_to field to the form.
 **************************************************************************/
function createReplyForm(comment_div) {

    var comment_id = comment_div.attr("id");

    var reply_button = comment_div.find(".reply-to-comment-button");

    /* Clone the reply div at the end of the page template that contains
     * the regular comment form.
     */
    var reply_div = $("#commenting").clone(true);

    /* Remove the ReCaptcha JS code before appending the form. If not
     * removed, this causes problems
     */
    reply_div.find("#formfield-form-widgets-captcha")
             .find("script")
             .remove();

    /* Insert the cloned comment form right after the reply button of the
     * current comment.
     */
    reply_div.appendTo(comment_div).css("display", "none");

    /* Remove id="reply" attribute, since we use it to uniquely
       the main reply form. */
    reply_div.removeAttr("id");

    /* Hide the reply button (only hide, because we may want to show it
     * again if the user hits the cancel button).
     */
    $(reply_button).css("display", "none");

    /* Fetch the reply form inside the reply div */
    var reply_form = reply_div.find("form");

    /* Populate the hidden 'in_reply_to' field with the correct comment id */
    reply_form.find("input[name='form.widgets.in_reply_to']")
              .val(comment_id);

    /* Add a remove-reply-to-comment Javascript function to remove the form */
    var cancel_reply_button = reply_div.find(".cancelreplytocomment");
    cancel_reply_button.attr("id", comment_id);

    /* Show the cancel buttons. */
    reply_form.find("input[name='form.buttons.cancel']")
              .css("display", "inline");

    /* Show the reply layer with a slide down effect */
    reply_div.slideDown("slow");

    /* Show the cancel button in the reply-to-comment form */
    cancel_reply_button.css("display", "inline");
}


$(document).ready(function () {


    /**************************************************************************
     * By default, hide the reply and the cancel button for the regular add
     * comment form.
     **************************************************************************/
    $(".reply").find("input[name='form.buttons.reply']")
		        .css("display", "none");
    $(".reply").find("input[name='form.buttons.cancel']")
	            .css("display", "none");


    /**************************************************************************
     * By default, show the reply button only when Javascript is enabled.
     * Otherwise hide it, since the reply functions only work with JS enabled.
     **************************************************************************/
    $(".reply-to-comment-button").css("display" , "inline");

    
    /**************************************************************************
     * If the user has hit the reply button of a reply-to-comment form (form was 
     * submitted with a value for the "in_reply_to" field in the request), 
     * create a reply-to-comment form right under this comment.
     **************************************************************************/
    var post_comment_div = $("#commenting");
    var in_reply_to_field = 
        post_comment_div.find("input[name='form.widgets.in_reply_to']");
    if (in_reply_to_field.val() !== "") {
        var current_reply_id = "#" + in_reply_to_field.val();
        var current_reply_to_div = $(".discussion").find(current_reply_id);
        createReplyForm(current_reply_to_div);
        clearForm(post_comment_div);
    }
    	
    
	/**************************************************************************
     * If the user hits the "reply" button of an existing comment, create a 
     * reply form right beneath this comment.
     **************************************************************************/
    $(".reply-to-comment-button").bind("click", function (e) {
        var comment_div = $(this).parents().filter(".comment");
        createReplyForm(comment_div);
        clearForm(comment_div);
    });


    /**************************************************************************
     * If the user hits the "clear" button of an open reply-to-comment form,
     * remove the form and show the "reply" button again.
     **************************************************************************/
    $("#form-buttons-cancel").bind("click", function (e) {
        e.preventDefault();
        var reply_to_comment_button = $(this).
		                                  parents().
								          filter(".comment").
									      find(".reply-to-comment-button");

        /* Find the reply-to-comment form and hide and remove it again. */
        reply_to_comment_form = $(this).parents().filter(".reply");
        reply_to_comment_form.slideUp("slow", function () { 
            $(this).remove(); 
        });

        /* Show the reply-to-comment button again. */
        reply_to_comment_button.css("display", "inline");

    });

});
 