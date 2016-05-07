(function() {
    var cards = document.getElementsByClassName("card");

    var checked = null;
    
    var submit_button = document.getElementById("submit");

    var check = function(id) {
        if(checked !== id) {
            document.getElementById(id).classList.remove("not-clicked");
            document.getElementById(id).classList.add("clicked");
            if(checked !== null) {
                document.getElementById(checked).classList.remove("clicked");
                document.getElementById(checked).classList.add("not-clicked");
            }
            checked = id;
            submit_button.disabled = false;
        }
        else {
            document.getElementById(id).classList.remove("clicked");
            document.getElementById(id).classList.add("not-clicked");
            checked = null;
            submit_button.disabled = true;
        }
    };

    for(var i = 0; i < cards.length; i++) {
        (function() {
            var id = cards[i].id;
            cards[i].addEventListener("click", function() {
                check(id);
            });
        }());
    };
    
    var sendVote = function(checked) {
        var XHR = new XMLHttpRequest();
        var FD = new FormData();
        FD.append("candidate", checked);
        XHR.open("POST", "/api/submit_vote");
        XHR.responseType = "text";
        XHR.onload = function() {
            if(XHR.readyState === XHR.DONE) {
                if(XHR.status === 200) {
                    if(XHR.responseText === "Success!") {
                        submit_button.innerHTML = "Vote Submitted";
                        submit_button.classList.remove("btn-secondary");
                        submit_button.classList.add("btn-success");
                    }
                    else {
                        submit_button.innerHTML = "Invalid Vote";
                        submit_button.classList.remove("btn-secondary");
                        submit_button.classList.add("btn-danger");
                    }
                }
            }
        }
        XHR.send(FD);
    };

    submit_button.addEventListener("click", function() {
        submit_button.innerHTML = '<i class="fa fa-circle-o-notch fa-spin"></i> Submitting...';
        submit_button.disabled = true;
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