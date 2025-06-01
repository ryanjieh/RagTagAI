const video = document.querySelector("#camera");
const canvas = document.querySelector("#snapshot");
const context = canvas.getContext("2d");
const uploadButton = document.querySelector("#upload-button");
const imageInput = document.querySelector("#image-input");
const resultBox = document.querySelector("#result-box");
let picture_option = "";

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });
    video.srcObject = stream;
  } catch (err) {
    alert("Could not access camera: " + err.message);
  }
}

function captureImage() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.style.display = "block";

  picture_option = "camera";
}

uploadButton.addEventListener("click", () => {
  imageInput.click();
});

function uploadImage() {
  const files = imageInput.files;
  if (files.length > 0) {
    const image = files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      const img = new Image();
      img.src = reader.result;
      img.onload = () => {
        const canvasWidth = canvas.width;
        const canvasHeight = canvas.height;

        const imgAspect = img.width / img.height;
        const canvasAspect = canvasWidth / canvasHeight;

        let drawWidth, drawHeight;

        // Scale to fit within canvas while preserving aspect ratio
        if (imgAspect > canvasAspect) {
          drawWidth = canvasWidth;
          drawHeight = canvasWidth / imgAspect;
        } else {
          drawHeight = canvasHeight;
          drawWidth = canvasHeight * imgAspect;
        }

        const offsetX = (canvasWidth - drawWidth) / 2;
        const offsetY = (canvasHeight - drawHeight) / 2;

        context.clearRect(0, 0, canvasWidth, canvasHeight);
        context.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
      };
    };
    reader.readAsDataURL(image);

    canvas.style.display = "block";
    picture_option = "upload";
  }
}

function rateImage() {
  const formData = new FormData();
  canvas.toBlob((blob) => {
    formData.append("image", blob, "image.png");
  }, "image/png");

  fetch("/rate", {
    method: "POST",
    body: formData,
  })
    .then((resp) => resp.json())
    .then((res) => {
      resultBox.innerHTML = res.result;
    });
}

startCamera();
