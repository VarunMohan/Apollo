var full_names = {"clinton": "Hillary Clinton", "sanders": "Bernie Sanders", "trump": "Donald Trump"};
var images;
var election_votes;

var initialize = function(clinton_img, sanders_img, trump_img, election_results) {
    election_votes = JSON.parse(election_results);
    images = {"clinton": clinton_img, "sanders": sanders_img, "trump": trump_img};
};

var descriptions = {"clinton": "For the past several decades, Mrs. Clinton, 68, has lived in the public eye as she has evolved. She has been a political spouse, the scorned wife of an embattled president, a senator who surprised her rivals by working across the aisle, and a losing presidential candidate in 2008 who went on to serve in the administration of Barack Obama, the man who had bested her.", 
                    "sanders": "Calling himself a Democratic socialist, Mr. Sanders has served in Congress as an independent from Vermont for more than two decades. Far to the left in his politics and sometimes grumpy in his demeanor, he is asking voters to join him in what he has framed as a political revolution, appealing to progressives frustrated with big challenges like income inequality.", 
                    "trump": "A billionaire businessman who made his fortune as a New York real estate developer before turning to reality television, Mr. Trump promises to use his deal-making prowess to enrich America. He has vowed to build a wall along the southern border, slash taxes and crush ISIS."};

var generateWinnerHTML = function(winner, votes, percent) {
    var votes_string = 'votes';
    if(votes === 1) {
        votes_string = 'vote';
    }
    return '<div class="card card-winner">' + 
               '<img class="card-img-left img-winner" src="' + images[winner] + '" alt="' + full_names[winner] + '">' + 
               '<div class="card-inline-block">' + 
                   '<h3 class="card-title title card-title-winner">' + 
                       '<div class="full-title-winner">' + 
                           full_names[winner] + 
                       '</div>' + 
                       '<div class="check-winner">' + 
                           '<i class="fa fa-check" aria-hidden="true"></i>' + 
                       '</div>' + 
                   '</h3>' + 
                   '<p class="card-text-winner">' + descriptions[winner] + '</p>' + 
                   '<progress class="progress" value="' + percent + '" max="100">' + percent + '%</progress>' + 
                   '<h3 class="stats">' + 
                       '<div class="votes">' + 
                           votes + ' ' + votes_string + 
                       '</div><div class="percentage">' + 
                           percent + '%' + 
                       '</div>' + 
                   '</h3>' + 
               '</div>' + 
           '</div>';
};

var generateLoserHTML = function(loser, rank, votes, percent) {
    var votes_string = 'votes';
    if(votes === 1) {
        votes_string = 'vote';
    }
    return '<div class="labeled-card">' + 
               '<div class="number-label">' + 
                   '<div class="number">' + 
                       rank + '.' + 
                   '</div>' + 
               '</div>' + 
               '<div class="card card-loser">' + 
                   '<img class="card-img-left img-loser" src="' + images[loser] + '" alt="' + full_names[loser] + '">' + 
                   '<div class="card-inline-block">' + 
                       '<h3 class="card-title title">' + full_names[loser] + '</h3>' + 
                       '<p class="card-text">' + descriptions[loser] + '</p>' + 
                       '<progress class="progress" value="' + percent + '" max="100">' + percent + '%</progress>' + 
                       '<h5 class="stats">' + 
                           '<div class="votes">' + 
                               votes + ' ' + votes_string + 
                           '</div><div class="percentage">' + 
                               percent + '%' + 
                           '</div>' + 
                       '</h5>' + 
                   '</div>' + 
               '</div>' + 
           '</div>';
};

var generateResults = function(results) {
    var dict = {"clinton": results.clinton, "sanders": results.sanders, "trump": results.trump};
    var items = Object.keys(dict).map(function(key) {
        return [key, dict[key]];
    });
    items.sort(function(first, second) {
        return second[1] - first[1];
    });
    var total = dict["clinton"] + dict["sanders"] + dict["trump"];
    var election_results = document.getElementById("election-results");
    var winning_vote_num = items[0][1];
    for(var i = 0; i < items.length; i++) {
        var percent;
        if(total === 0) {
            percent = 0;
        }
        else {
            percent = Math.round(items[i][1] / total * 100 * 10) / 10;
        }
        if(items[i][1] === winning_vote_num) {
            election_results.innerHTML += generateWinnerHTML(items[i][0], items[i][1], percent);
        }
        else {
            election_results.innerHTML += generateLoserHTML(items[i][0], i + 1, items[i][1], percent);
        }
    }
}

var verify_election_button = document.getElementById("verify-election");

var verifyElection = function() {
    var myvote = document.cookie.split('=')[1];
    var good = false;
    for (var i = 0; i < election_votes.length; i++) {
        var vote = election_votes[i];
        if (vote === myvote) {
            good = true;
        }
    }
    if (!good) {
        verify_election_button.innerHTML = "Invalid Election";
        verify_election_button.disabled = true;
        verify_election_button.classList.remove("btn-info");
        verify_election_button.classList.add("btn-danger");
    } else {
        verify_election_button.innerHTML = "Valid Election";
        verify_election_button.disabled = true;
        verify_election_button.classList.remove("btn-info");
        verify_election_button.classList.add("btn-success");
    }
}

verify_election_button.addEventListener("click", function() {
    verifyElection();
});
