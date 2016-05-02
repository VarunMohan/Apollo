(function() {
    var cards = document.getElementsByClassName("card");

    var checked = null;

    var check = function(id) {
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

    var sendVote = function(checked) {
        var XHR = new XMLHttpRequest();
        var FD = new FormData();
        FD.append("candidate", checked);
        XHR.open("POST", "/api/submit_vote");
        XHR.send(FD);
    }

    var submit_button = document.getElementById("submit");
    submit_button.addEventListener("click", function() {
        sendVote(checked);
    });

    var endElection = function() {
        var XHR = new XMLHttpRequest();
        XHR.open("POST", "/api/end_election");
        XHR.responseType = "text";
        XHR.onload = function() {
            if(XHR.readyState === XHR.DONE) {
                if(XHR.status === 200) {
                    window.location.reload(true);
                }
            }
        }
        XHR.send();
    }

    var end_election_button = document.getElementById("end-election");
    end_election_button.addEventListener("click", function() {
        endElection();
    });
})();