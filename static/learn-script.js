document.addEventListener("DOMContentLoaded", function() {
    const showbtn = document.querySelector("#show");
    const front = document.getElementsByClassName("front-container");
    const back = document.getElementsByClassName("back-container");
    const learnbtns = document.querySelectorAll(".learn-btn");

    showbtn.addEventListener("click", function () {
        for (let i = 0; i < front.length; i++) {
            front[i].style.display = "none";
            back[i].style.display = "flex";
        }
    });

    learnbtns.forEach(function(learnbtn) {
        learnbtn.addEventListener("click", function(event) {
            for (let i = 0; i < front.length; i++) {
                front[i].style.display = "flex";
                back[i].style.display = "none";
            }
            event.stopPropagation();
        });
    });
});