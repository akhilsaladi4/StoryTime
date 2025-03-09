document.addEventListener('DOMContentLoaded', (event) => {
    const thisVideo = document.getElementById('video');

    if (!thisVideo) {
        console.error("Video element not found");
    } else {
        thisVideo.style.display = 'none'; 
        thisVideo.style.width = '25%';
        thisVideo.style.height = 'auto';
        console.log("Video element found and styled");
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            thisVideo.srcObject = stream; 
            console.log("Webcam stream started");
        })
        .catch(err => {
            console.error("Error accessing the camera: ", err);
        });

    function captureImage(callback) {
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');
        
        canvas.width = thisVideo.videoWidth;
        canvas.height = thisVideo.videoHeight;
        context.drawImage(thisVideo, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'webcam.jpg');
            
            fetch('/process-image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.background_image) {
                    document.querySelector(".background").style.backgroundImage = `url('/static/images/${data.background_image}')`;
                }
                if (callback) callback();
            })
            .catch(error => {
                console.error('Error processing image:', error);
            });
        }, 'image/jpeg');
    }

    function readSentenceAloud(sentence, callback) {
        fetch('/read-sentence-aloud', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sentence: sentence })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Sentence read aloud:', data);
            if (callback) callback();
        })
        .catch(error => {
            console.error('Error reading sentence aloud:', error);
        });
    }

    function startReadingStory() {
        const story = document.querySelector('#story').innerText;
        const sentences = story.split('. ');
        let currentSentenceIndex = 0;

        function readNextSentence() {
            if (currentSentenceIndex < sentences.length) {
                const sentence = sentences[currentSentenceIndex];
                readSentenceAloud(sentence, () => {
                    captureImage(() => {
                        currentSentenceIndex++;
                        readNextSentence();
                    });
                });
            } else {
                console.log('Story reading complete');
                document.getElementById('refine-story-button').style.display = 'block'; 
            }
        }

        readNextSentence();
    }

    startReadingStory();

    document.getElementById('refine-story-button').addEventListener('click', () => {
        fetch('/refine-story', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('story').innerText = data.refined_story;
            document.getElementById('refine-story-button').style.display = 'none'; 
            startReadingStory();
        })
        .catch(error => {
            console.error('Error refining story:', error);
        });
    });
    
});

