(function() {
    var cards = document.getElementsByClassName("card");

    var checked = null;

    var check = function(id) {
        console.log(checked);
        if(checked !== id) {
            document.getElementById(id).classList.remove("not-clicked");
            document.getElementById(id).classList.add("clicked");
            if(checked !== null) {
                document.getElementById(checked).classList.remove("clicked");
                document.getElementById(checked).classList.add("not-clicked");
            }
            checked = id;
            document.getElementById("submit").disabled = false;
        }
        else {
            document.getElementById(id).classList.remove("clicked");
            document.getElementById(id).classList.add("not-clicked");
            checked = null;
            document.getElementById("submit").disabled = true;
        }
    };

    for(var i = 0; i < cards.length; i++) {
        (function() {
            var id = cards[i].id;
            cards[i].addEventListener("click", function() {
                check(id);
            });
        }());
    }
})();