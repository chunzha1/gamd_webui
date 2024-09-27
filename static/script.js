// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const downloadForm = document.getElementById('downloadForm');
    const messageDiv = document.getElementById('message');
    const logDiv = document.getElementById('log');

    downloadForm.addEventListener('submit', function(e) {
        e.preventDefault();  // Prevent the form from submitting normally

        const formData = new FormData(this);

        messageDiv.textContent = 'Starting download...';
        messageDiv.style.color = 'blue';
        logDiv.textContent = '';

        startDownload(formData);
    });

    function startDownload(formData) {
        fetch('/download', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'started') {
                messageDiv.textContent = data.message;
                startEventStream();
            } else {
                messageDiv.textContent = data.message;
                messageDiv.style.color = 'red';
            }
        })
        .catch(error => {
            messageDiv.textContent = 'An error occurred. Please try again.';
            messageDiv.style.color = 'red';
            console.error('Error:', error);
        });
    }

    function startEventStream() {
        const eventSource = new EventSource('/stream');

        eventSource.onmessage = function(event) {
            logDiv.textContent += event.data+'\n';
            logDiv.scrollTop = logDiv.scrollHeight;

            if (event.data.includes('Download completed successfully')) {
                eventSource.close();
                messageDiv.textContent = 'Download completed successfully.';
                messageDiv.style.color = 'green';
            }
        };

        eventSource.onerror = function(event) {
            console.error('SSE error:', event);
            eventSource.close();
        };
    }
});