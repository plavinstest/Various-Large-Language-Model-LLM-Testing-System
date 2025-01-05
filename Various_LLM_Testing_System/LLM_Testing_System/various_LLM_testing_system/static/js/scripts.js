$(document).ready(function() {

    // Trigger chat function when Enter key is pressed in the input field
    $('#chat-input').on('keypress', function(e) {
        if (e.key === 'Enter') {
            chat_function();
        }
    });


    // Trigger chat function when the send button is clicked
    $('#send-button').on('click', function() {
        chat_function();
    });


    function chat_function() {
        // Get user input and selected model
        const message = $('#chat-input').val();
        const model = $('#models_name').val();
        // Validate user input
        if (!message) {
            alert("Please enter some text!!!");
            return;
        } else if (model === null) { // Update to match the disabled value
            // Ensure a model is selected
            alert("Please select a model!!!");
            return;
        } else {
            // Prepare form data for AJAX request
            var form_data = new FormData();
            form_data.append("message", message);
            form_data.append("model", model);
    
            // Display user's message in the chat box
            $('#chat-box').append('<div class="user-message">' + message + '</div>');
    
            $.ajax({
                url: '/',  // Django endpoint to handle the request
                type: 'POST',
                data: form_data,
                processData: false, // Required for FormData
                contentType: false, // Required for FormData
                success: function (response) {
                    // Handle successful response from the server
                    var response_status = response['status'];
                    var response_message = response['answer'];
                    if (response_status == 'success') {
                        $('#chat-box').append('<div class="bot-message">' + response_message + '</div>');
                    } else {
                        // Handle server-side failure
                        const dummyResponse = "We could not proceed with " + message + ". Please try again.";
                        $('#chat-box').append('<div class="bot-message">' + dummyResponse + '</div>');
                    }
                    // $('#chat-input').val('');  // Clear input field
                    // Auto-scroll chat box to the bottom
                    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight); // Scroll to bottom
                },
                error: function () {
                    // Handle AJAX request errors
                    alert('Error sending message. May be server is not responding');
                }
            });
        }
    }




    // function chat_function(){
    //     const message = $('#chat-input').val();
    //     const model = $('#models_name').val();
    //     if (!message){
    //         alert("Please enter some text!!!");
    //         return;
    //     }
    //     else if (model===null){
    //         alert("Please select a model!!!");
    //         return;
    //     }
    //     else{
    //         var form_data = new FormData();
    //         form_data.append("message", message);
    //         form_data.append("model", model);
    //         // form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
    //         $.ajax({
    //             url: '/',  // Django endpoint to handle the request
    //             type: 'POST',
    //             data: form_data,
    //             processData: false,  // Required for FormData
    //             contentType: false,  // Required for FormData
    //             success: function(response) {
    //                 // For now, simulate a response
    //                 var response_status = response['status']
    //                 var response_message = response['answer']
    //                 if (response_status == 'success'){
    //                     // const dummyResponse = "This is a dummy response for: " + message;
    //                     $('#chat-box').append('<p>' + response_message + '</p>');
    //                     // $('#chat-input').val('');  // Clear input field
    //                 }
    //                 else{
    //                   const dummyResponse = "We could not proceed with" + `${message}. Please try again.`;
    //                   $('#chat-box').append('<p>' + dummyResponse + '</p>');
    //                 //   $('#chat-input').val('');  // Clear input field  
    //                 }
    //                 $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight); // Scroll to bottom
    //             },
    //             error: function() {
    //                 alert('Error sending message. May be server is not responding');
    //                 // const dummyResponse = "This is a dummy response for: " + message;
    //                 // $('#chat-box').append('<p>' + dummyResponse + '</p>');
    //                 // $('#chat-input').val('');  // Clear input field
    //                 // $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight); // Scroll to bottom
    //             }
    //         });

    //     }
        
    // }
});