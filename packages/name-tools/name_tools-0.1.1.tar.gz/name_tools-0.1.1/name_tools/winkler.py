import math

def winkler(s1, s2):
    match_len = int(math.floor(max(len(s1), len(s2)) / 2.0) - 1)

    for i in xrange(0, len(s1)):
        c1 = s1[i]

        for j in xrange(max(0, i - match_len), min(len(s2), i + match_len)):
            c2 = s2[j]

            
            
