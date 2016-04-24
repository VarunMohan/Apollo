from tallier import Tallier
from registrar import Registrar
from voter import Voter

import random

if __name__ == '__main__':
    r = Registrar()
    t = Tallier(r)

    voters = [Voter(i, r, t) for i in range(100)]
    total = 0
    for voter in voters:
      vote = random.randint(0,10)
      total += vote
      voter.vote(vote)

    result = t.tally_votes()
    assert result == total

    print("Everything is going swimmingly")
