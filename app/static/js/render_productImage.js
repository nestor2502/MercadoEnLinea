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

/* VERIFY INPUTS 
var nameInput = document.getElementById("nameProduct")
var updateButton = document.getElementById("updateButton")
*/

