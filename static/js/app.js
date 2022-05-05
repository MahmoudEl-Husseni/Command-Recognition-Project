//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

const downloadLink = document.getElementById('download');
const startButton = document.getElementById('start');
const uploadURL = "{{ url_for('index') }}";

const handleSuccess = function (stream) {
	const options = { mimeType: 'audio/webm' };
	const recordedChunks = [];
	const mediaRecorder = new MediaRecorder(stream, options);

	mediaRecorder.addEventListener('dataavailable', function (e) {
		if (e.data.size != 0) { recordedChunks.push(e.data) };
	});

	mediaRecorder.addEventListener('stop', async function () {
		downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
		downloadLink.download = 'acetest.wav';



		//const audioBlob = new Blob(recordedChunks, { type: "audio/wav" })
		//const audioUrl = URL.createObjectURL(audioBlob);
		//const audio = new Audio(audioUrl);
		//audio.play();
});



	startButton.addEventListener('click', function () {

		startButton.disabled = true;
		recordedChunks.pop();
		mediaRecorder.start();
		setTimeout(() => { mediaRecorder.stop(); startButton.disabled = false; }, 1000);


	});
};

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
	.then(handleSuccess);