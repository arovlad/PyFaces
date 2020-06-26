form = null;

function readFile() {
      if (this.files && this.files[0]) {
            var FR = new FileReader();
            FR.addEventListener("load", function(e) {
                document.getElementsByClassName("upload")[0].className = "button upload intermediate";
                document.getElementsByClassName("upload")[0].innerHTML = "Change file";
                document.getElementsByClassName("submit")[0].style.display = "initial";
				form = document.createElement('form');
				form.method = 'post';
				form.action = "/welcome/app/result";
				const hiddenField = document.createElement('input');
				hiddenField.type = 'hidden';
				hiddenField.name = 'imagedata';
				hiddenField.value = e.target.result;
				form.appendChild(hiddenField);
				document.body.appendChild(form);
                document.getElementsByClassName("submit")[0].addEventListener("click", function(){
                  document.getElementById("highlight-buttons").innerHTML = "Preparing your result.<br>This may take up to 2 minutes.";
                  form.submit();
                });
            });
            FR.readAsDataURL( this.files[0] );
      }
}

document.getElementById("filedata").addEventListener("change", readFile);
