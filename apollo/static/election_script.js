var cards = document.getElementsByClassName("card");

var checked = null;

var submitted = false;

var candidate_ids = {"clinton": 0, "sanders": 1, "trump": 2};

var num_candidates;
var num_voters;

var pkg;
var pkn;

var initialize = function(ncands, nvoters, generator, key) {
    num_candidates = ncands;
    num_voters = nvoters;
    pkg = generator;
    pkn = key;
};

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
        if (!submitted) {
            submit_button.disabled = false;
        }
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
}

var sendVote = function(evote, proof) {
    var XHR = new XMLHttpRequest();
    var FD = new FormData();
    FD.append("evote", evote);
    FD.append("proof", JSON.stringify(proof));
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
    submitted = true;
    var worker = new Worker("/static/encrypt.js");
    worker.postMessage([candidate_ids[checked], num_candidates, num_voters, pkg, pkn]);
    worker.onmessage = function(e) {
        var evote = e.data[0];
        var proof = e.data[1];
        worker.terminate();
        sendVote(evote, proof);
    };
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
if(end_election_button) {
    end_election_button.addEventListener("click", function() {
        endElection();
    });
}