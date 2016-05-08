if("function" === typeof importScripts) {
    var window = self;
    importScripts("/static/jsbn/jsbn.js", "/static/jsbn/jsbn2.js", "/static/jsbn/prng4.js", "/static/jsbn/rng.js");

    onmessage = function(e) {
        var candidate_id = e.data[0];
        var num_candidates = e.data[1];
        var num_voters = e.data[2];
        var pkg = new BigInteger(e.data[3]);
        var pkn = new BigInteger(e.data[4]);
        var pkn2 = pkn.square();
    
        var evote;
        var proof;
    
        var rng = new SecureRandom();
        
        var create512 = function() {
            return (new BigInteger(256, 1, rng)).multiply(nbv(2).pow(256)).add(new BigInteger(256, 1, rng));
        };
        
        var create1024 = function() {
            return (create512()).multiply(nbv(2).pow(512)).add(create512());
        };
        
        var create2048 = function() {
            return (create1024()).multiply(nbv(2).pow(1024)).add(create1024());
        };
    
        var encrypt = function(vote) {
            var done = false;
            while (!done) {
                var r = create1024();
                if (r.gcd(pkn).equals(BigInteger.ONE)) {
                    done = true;
                }
            }
            return [pkg.modPow(vote, pkn2).multiply(r.modPow(pkn, pkn2)).mod(pkn2), r];
        };
    
        var bigIntSum = function(bigInts) {
            var sum = BigInteger.ZERO;
            for(var i = 0; i < bigInts.length; i++) {
                sum = sum.add(bigInts[i]);
            }
            return sum;
        };
        
        var listToString = function(list) {
            var arr = [];
            for(var i = 0; i < list.length; i++) {
                arr.push(list[i].toString());
            }
            return arr;
        }
    
        var genProof = function(u, esum, real, v) {
            var a = [];
            var z = [];
            var e = [];
            var r = 0;
            for(var i = 0; i < u.length; i++) {
                if(i !== real) {
                    var newz = create2048();
                    var newe = create1024();
                    var newa = newz.modPow(pkn, pkn2).multiply(u[i].modPow(newe, pkn2).modInverse(pkn2)).mod(pkn2);
                    z.push(newz);
                    e.push(newe);
                    a.push(newa);
                }
                else {
                    r = create2048();
                    var newa = r.modPow(pkn, pkn2);
                    a.push(newa);
                    z.push(null);
                    e.push(BigInteger.ZERO);
                }
            }
            e[real] = esum.subtract(bigIntSum(e)).mod(nbv(2).pow(1024));
            z[real] = r.multiply(v.modPow(e[real], pkn2)).mod(pkn2);
            return [listToString(u), listToString(a), listToString(e), listToString(z), esum.toString()];
        };

        var encryptVote = function(candidate_id) {
            var m = nbv(num_voters).add(BigInteger.ONE);
            var vote = m.pow(candidate_id);
            var encrypted = encrypt(vote);
            evote = encrypted[0];
            var esum = create1024();
            var u = [];
            for(var i = 0; i < num_candidates; i++) {
                var newu = evote.multiply(pkg.modPow(m.pow(i), pkn2).modInverse(pkn2)).mod(pkn2);
                u.push(newu);
            }
            proof = genProof(u, esum, candidate_id, encrypted[1]);
        };
    
        encryptVote(candidate_id);
        postMessage([evote.toString(), proof]);
    };
}