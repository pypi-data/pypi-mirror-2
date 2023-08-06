#!/usr/bin/env python
#
# Copyright 2009 Sebastian Raaphorst.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An implementation of basic combinatorial k-subset operations using
lexicographic ordering.

Note that for our purposes here, sets are represented as lists as
ranking, unranking, and successor functions need a total order on the
elements of the set.

For the base set B, if B is an integer, we assume that our base set is
[0,...,B-1]. Otherwise, assume that B is a pair consisting of:
   1. a list representing the base set
   2. a reverse lookup dict, mapping elements of the base set to their
      position in the total order.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}
Note that we require B to contain the reverse lookup information to
speed up the algorithms here; otherwise, we would need to call index on
our base set many times, which would increase complexity by a factor of
the length of the base set.

By Sebastian Raaphorst, 2009."""

import combfuncs


def rank(B, K):
    """Return the rank of k-subset K in base set B."""

    v = (B if type(B) == int else len(B[0]))
    block = (K if type(B) == int else [B[1][i] for i in K])
    k = len(block)
    r = combfuncs.binom(v,k)
    for i in xrange(k):
        r -= combfuncs.binom(v-block[i]-1, k-i)
    return r-1


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""

    v = (B if type(B) == int else len(B[0]))

    K = [0] * k
    vi = combfuncs.binom(v,k)
    j = v
    ki = k
    s = rk + 1
    for i in xrange(k-1):
        while s > vi - combfuncs.binom(j, ki):
            j -= 1
        K[i] = v - j - 1
        s += combfuncs.binom(j+1, ki) - vi
        ki -= 1
        vi = combfuncs.binom(j, ki)
    K[k-1] = v + s - vi - 1

    return (K if type(B) == int else [B[0][i] for i in K])


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""

    retcode = None
    v = (B if type(B) == int else len(B[0]))
    Kn = (K[:] if type(B) == int else [B[1][i] for i in K])

    k = len(K)
    for i in xrange(k-1,-1,-1):
        Kn[i] += 1
        if Kn[i] < v and Kn[i] + (k-i) <= v:
            Kn[i+1:] = [Kn[i]+j-i for j in xrange(i+1,k)]
            retcode = Kn
            break

    if retcode == None:
        return retcode
    return (Kn if type(B) == int else [B[0][i] for i in Kn])


def all(B, k):
   """A generator to create all k-subsets over the specified base set B."""

   # Check to make sure that we can return subsets, i.e. there are enough
   # elements to satisfy.
   lenB = (B if type(B) == int else len(B[0]))
   if lenB < k:
       return

   # Make the base set, creating a copy of B if B is a pair as described in
   # the module introduction; thus, if B changes, the iterator does not
   # become invalid.
   Bn = (B if type(B) == int else (B[0][:], dict(B[1])))
   K = (range(k) if type(B) == int else Bn[0][:k])
   while K != None:
       yield K
       K = succ(Bn, K)
