// certificate.js

document.addEventListener("DOMContentLoaded", function () {
    var carets = document.getElementsByClassName("caret");
    for (var i = 0; i < carets.length; i++) {
        carets[i].addEventListener("click", function () {
            this.classList.toggle("caret-down");
            var nestedList = this.nextElementSibling;
            if (nestedList.style.display === "block") {
                nestedList.style.display = "none";
            } else {
                nestedList.style.display = "block";
            }
        });
    }
});
