document.addEventListener("DOMContentLoaded", function() {
    const boxs = document.querySelectorAll(".box")
    const boxcontainer = document.querySelector("#box-container")
    const openbox = document.getElementById("openbox-btn")
    const box_id = document.getElementById("box_id")
    var selectedbox = null;

    boxs.forEach(function(box) {
        box.addEventListener("click", function(event) {
            if (selectedbox) {
                selectedbox.classList.remove("selected-deck");
            }
            
            selectedbox = this;
            selectedbox.classList.add("selected-deck");
            box_id.value = this.id;
            openbox.type = "submit";
            event.stopPropagation();
        });


    boxcontainer.addEventListener("click", function(event) {
        if (selectedbox) {
            selectedbox.classList.remove("selected-deck");
            selectedbox = null;
            openbox.type = "button";
            openbox.removeAttribute("value");
        }
        event.stopPropagation();
    });

        
});
});