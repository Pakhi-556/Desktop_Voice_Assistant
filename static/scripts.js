$(document).ready(function() {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    const startListening = () => {
        $('#output').text('Listening...');
        recognition.start();
    };

    $('#startBtn').click(async function() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            startListening();
            $('.container').hide();
            $('#micContainer').show()
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Error accessing microphone. Please allow microphone access to use voice recognition.');
        }
    });

     // Event listener for Alt + Z key press
     $(document).keydown(function(e) {
        if (e.key === 'z') {
            $('#startBtn').click();
        }
    });
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.trim();
        $('#output').text('Recognized Command: ' + transcript);

        $.ajax({
            url: '/get-information',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: transcript }),
            success: function(response) {
                console.log(response);

               if(response.response_text!=""){
                // Display the response text on the page
                $('#response').html('<div class="response-container">'+response.response_text+'</div>');
                $('#response').show();
               }else{
                $('#response').hide();
               }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    };
    
    recognition.onend = function() {
        // Hide mic animation container and show main content container
        $('#micContainer').hide();
        $('.container').show();
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        alert('Speech recognition error. Please try again or allow microphone access.');
    };
    
    $('#loginBtn').click(function() {
        // Redirect to the login page
        window.location.href = '/login';
    });

    // Slowing down the background video playback
    const video = document.getElementById('video-background');
    video.playbackRate = 0.4; // Adjust this value as needed
});