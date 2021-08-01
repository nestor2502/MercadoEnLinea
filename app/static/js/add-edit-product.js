/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onerror = function(event) {
            alert("Archivo no compatible\n");
            reader.abort(); // (...does this do anything useful in an onerror handler?)
            return;
        };
        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

(function () {
    $('#customFile').on('change', function () {
        readURL(input);
        
    });
});
/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */

var input = document.getElementById('customFile');
var infoArea = document.getElementById('upload');

input.addEventListener('change', showFileName );

function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = fileName;
}
