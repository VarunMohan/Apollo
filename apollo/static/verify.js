if("function" === typeof importScripts) {
    var window = self;
    importScripts("/static/jsbn/jsbn.js", "/static/jsbn/jsbn2.js", "/static/jsbn/prng4.js", "/static/jsbn/rng.js");
    onmessage = function(e) {
        var rng = new SecureRandom();
        var create512 = function() {
            return (new BigInteger(256, 1, rng)).multiply(nbv(2).pow(256)).add(new BigInteger(256, 1, rng));
        };
        
        var create1024 = function() {
            return (create512()).multiply(nbv(2).pow(512)).add(create512());
        };

        var election_votes = e.data[0];
        var msg = new BigInteger(e.data[1]);
        var pkg = new BigInteger(e.data[2]);
        var pkn = new BigInteger(e.data[3]);
        var pkn2 = pkn.square();
        var C = BigInteger.ONE;
        var echall_num = create1024();

        var checkElection = function(dum) {
            an = new BigInteger(dum[0]);
            z = new BigInteger(dum[1]);
            zn = z.modPow(pkn, pkn2);
            res = an.multiply(pkg.modPow(msg, pkn2).modInverse(pkn2).multiply(C).mod(pkn2).modPow(echall_num, pkn2)).mod(pkn2);
            return res.equals(zn)
        };

        var verifyElection = function(e_chall) {
            var XHR = new XMLHttpRequest();
            var FD = new FormData();
            FD.append("e_chall", e_chall);
            XHR.open("POST", "/api/verify_election");
            XHR.responseType = "text";
            XHR.onload = function() {
                if(XHR.readyState === XHR.DONE) {
                    if(XHR.status === 200) {
                        postMessage([checkElection(JSON.parse(XHR.responseText))]);
                    }
                }
            }
            XHR.send(FD);
        };


        for (var i = 0; i < election_votes.length; i++) {
            election_votes[i] = new BigInteger(election_votes[i]);
            C = C.multiply(election_votes[i]).mod(pkn2);
        }

        verifyElection(echall_num.toString());
    }
}
