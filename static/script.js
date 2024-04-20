document.addEventListener("DOMContentLoaded", function() {
    const createButton = document.getElementById("create-deck");
    const deckContainer = document.getElementById("deck_container");
    
    createButton.addEventListener("click", function() {
        document.getElementById("deck-name").style.display = "flex";
    });

    var deckEnvelops = document.querySelectorAll(".deck_envelop");
    var form = document.querySelector("#deck-name form");
    var deleteButton = document.querySelector(".control-deck button[name='delete']");
    var openButton = document.querySelector(".control-deck button[name='open']");
    var nameParagraph = document.querySelector("#name");
    var selectedDeckEnvelop = null; // To keep track of the selected deck envelope
    const x = document.getElementById("x")

    deckEnvelops.forEach(function(deckEnvelop) {
        deckEnvelop.addEventListener("click", function(event) {
            if (selectedDeckEnvelop) {
                selectedDeckEnvelop.classList.remove("selected-deck");
            }
            
            selectedDeckEnvelop = this;
            selectedDeckEnvelop.classList.add("selected-deck");

            var deckName = this.querySelector("p").textContent;
            
            var deleteAction = "/delete"; // Replace with the appropriate route for delete
            var openAction = "/open";     // Replace with the appropriate route for open
            
            deleteButton.form.action = deleteAction;
            deleteButton.value = deckName;
            deleteButton.form.method = "post"
            
            openButton.form.action = openAction;
            openButton.value = deckName;
            openButton.form.method = "post"
            
            event.stopPropagation(); // Prevents the click event from propagating to the deck container
        });
    });

    // Add a click event listener to the deck container to clear the selected deck
    deckContainer.addEventListener("click", function(event) {
        if (selectedDeckEnvelop) {
            selectedDeckEnvelop.classList.remove("selected-deck");
            selectedDeckEnvelop = null;
            deleteButton.form.action = "/";
            deleteButton.removeAttribute("value");
            deleteButton.form.method = "get";
            
            openButton.form.action = "/";
            openButton.removeAttribute("value");
            openButton.form.method = "get";
        }
        event.stopPropagation();
    });

    x.addEventListener("click", function() {
        document.getElementById("deck-name").style.display = "none";
    });
});