/* SHOW UPLOADED IMAGE */
function showImage(event){
    var image = URL.createObjectURL(event.target.files[0]);
    var newImg = document.getElementById('imageResult');
    newImg.src = image;
}

/* CHANGE IMAGE LABEL */
var input = document.getElementById('customFile');
input.addEventListener('change', showFileName);

function showFileName(event) {
    var input = event.srcElement;
    var fileName = input.files[0].name;
    var infoArea = document.getElementById('labelImage');
    infoArea.textContent = fileName;
}

/* AVAILABLE CHECKBOX TEXT */
var checkbox = document.getElementById('check-available');
checkbox.addEventListener('click', showAvailable);

function showAvailable() {
    if ($("#check-available").is(":checked")) {
        $("#text-available").text("DISPONIBLE");
    } else {
        $("#text-available").text("NO DISPONIBLE");
    }
}

