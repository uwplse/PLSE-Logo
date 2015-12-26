from __future__ import division

import threading
import random
import math
import pickle
import os
import sys

START = [(-1, 0, "pt.0"), (-.5, 0, "pt.1"),
         (0, 0, "pt.2"), (.5, 0, "pt.3"),
         (1, 0, "pt.4")]

MOVE_SIGMA = .25
SPLIT_PROB = .1
CLONE_PROB = .5
RANDOM_PROB = .1
MIN_LENGTH = .1
POOL_SIZE = 20
FRAC_KICK = .6
FILE = "pool.pickle"

def make_id(s):
    return s + str(round(random.random(), 9))[1:]

def move_pt(s, idx):
    dx, dy = random.gauss(0, MOVE_SIGMA), random.gauss(0, MOVE_SIGMA)
    s[idx] = (s[idx][0] + dx, s[idx][1] + dy, s[idx][2])
    return s

def mutate_move(s):
    idx = random.randint(0, len(s)-1)
    return move_pt(s, idx)

def mutate_delete(s):
    idx = random.randint(0, len(s)-1)
    del s[idx]

def mutate_split(s):
    idx = random.randint(1, len(s)-1)
    p1, p2 = s[idx-1:idx+1]
    w = random.random()
    newpoint = (w * p1[0] + (1 - w) * p2[0], w * p1[1] + (1 - w) * p2[1], make_id("pt"))
    s[idx:idx] = [newpoint]
    return move_pt(s, idx)

def valid_logo(s):
    last = s[0]
    for cur in s[1:]:
        dist = (cur[0] - last[0]) ** 2 + (cur[1] - last[1]) ** 2
        if dist < MIN_LENGTH ** 2:
            return False
    for pt in s:
        if not (-1 <= pt[0] <= 1) or not (-1 <= pt[1] <= 1):
            return False
    return True

def mutate(s):
    snext = None
    while not snext or not valid_logo(snext):
        snext = s[:]
        r = random.random()

        if r < SPLIT_PROB:
            snext = mutate_split(snext)
        elif r < SPLIT_PROB + SPLIT_PROB:
            snext = mutate_delete(snext)
        else:
            snext = mutate_move(snext)
    return snext

def cross(s1, s2):
    ids1 = [pt[2] for pt in s1]
    ids2 = [pt[2] for pt in s2]
    shared_ids = set(ids1) & set(ids2)

    s = []
    idx1, idx2 = 0, 0
    while idx1 < len(s1) and idx2 < len(s2):
        # Inv: idx1 == len(s1) <=> idx2 = len(s2)

        pt1 = s1[idx1]
        pt2 = s2[idx2]
        # Inv: pt1[2] == pt2[2]

        # Pick some intermediate between the two points
        u = random.random()
        v = random.random()
        newx = u * pt1[0] + (1 - u) * pt2[0]
        newy = v * pt1[1] + (1 - v) * pt2[1]
        s.append((newx, newy, pt1[2]))

        # Find the next shared point
        ndx1 = idx1 + 1
        while ndx1 < len(s1) and s1[ndx1][2] not in shared_ids:
            ndx1 += 1

        ndx2 = idx2 + 1
        while ndx2 < len(s2) and s2[ndx2][2] not in shared_ids:
            ndx2 += 1

        if random.random() < .5:
            s.extend(s1[idx1+1:ndx1])
        else:
            s.extend(s1[idx2+1:ndx2])

        idx1, idx2 = ndx1, ndx2

    return s

def make_svg(s):
    template = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="200" height="200"> <g>
  <rect width="180" height="180" x="10" y="10" style="fill:#39275b" />
  <path style="fill:none;stroke:#ffffff;stroke-width:14;" d="M {}" />
</g> </svg> """

    s = [(-1.1, s[0][1])] + s + [(1.1, s[-1][1])]
    points = ["{} {}".format(pt[0] * 85 + 100, pt[1] * -85 + 100) for pt in s]
    return template.format(" ".join(points))

def write_svg(f, s):
    with open(f, "wt") as f:
        f.write(make_svg(s))

def mutate_lots(s):
    for i in range(20):
        s = mutate(s)
    return s

class Pool:
    def __init__(self):
        self.pool = [(make_id("img"), mutate_lots(START)) for i in range(POOL_SIZE)]
        self.scores = {id: [0, 0] for (id, s) in self.pool}

        for id, s in self.pool:
            write_svg("imgs/" + id + ".svg", s)

    def choose(self):
        return random.choice(self.pool)

    def save(self):
        with open(FILE, "wb") as f:
            pickle.dump((self.pool, self.scores), f)

    def load(self):
        with open(FILE, "rb") as f:
            pool, scores = pickle.load(f)
        self.pool = pool
        self.scores = scores

        for id, s in self.pool:
            write_svg("imgs/" + id + ".svg", s)

    def vote(self, win_id, lose_id):
        try:
            score1 = self.scores[win_id]
            score2 = self.scores[lose_id]
        except:
            return
        score1[0] += 1
        score2[1] += 1

        if score2[1] < 3: return
        if score2[0] / sum(score2) < FRAC_KICK:
            self.kick(lose_id)

    def hate(self, id):
        try:
            score = self.scores[id]
        except:
            return
        score[1] += 1

        if score[1] < 3: return
        if score[0] / sum(score) < FRAC_KICK:
            self.kick(id)

    def kick(self, id):
        idx = [i for (i, (id_, s)) in enumerate(self.pool) if id_ == id][0]
        del self.pool[idx]
        del self.scores[id]
        self.introduce()

    def introduce(self):
        while len(self.pool) < POOL_SIZE:
            r = random.random()
            if r < CLONE_PROB:
                _, old = self.choose()
                s = mutate(old)
            elif r < CLONE_PROB + RANDOM_PROB:
                s = mutate_lots(START)
            else:
                old1, old2 = [s for _, s in random.sample(self.pool, 2)]
                s = cross(old1, old2)

            id = make_id("img")
            while id in self.scores:
                id = make_id("img")

            self.pool.append((id, s))
            self.scores[id] = [0, 0]

            write_svg("imgs/" + id + ".svg", s)

POOL = None

import bottle
bottle.TEMPLATE_PATH.append(".")

@bottle.get("/")
@bottle.view("page")
def page():
    id1, s1 = POOL.choose()
    id2, s2 = id1, None

    while id2 == id1:
        id2, s2 = POOL.choose()

    return dict(id1=id1, id2=id2)

def wilson_lb(good, bad):
    if good + bad == 0:
        return 0
    else:
        return ((good + 1.9208) / (good + bad)
                - 1.96 * math.sqrt((good * bad) / (good + bad) + 0.9604) /
                (good + bad)) / (1 + 3.8416 / (good + bad))

@bottle.get("/pool")
@bottle.view("pool")
def pool():
    items = POOL.scores.items()
    return dict(opts=sorted(items, key=lambda x: wilson_lb(float(x[1][0]), float(x[1][1])), reverse=True))

@bottle.get("/imgs/:fn")
def imgs(fn):
    return bottle.static_file(fn, root="./imgs/")

@bottle.get("/vote/:winid/:loseid")
def vote(winid, loseid):
    POOL.vote(winid, loseid)
    bottle.redirect("/")

@bottle.get("/hate/:id1/:id2")
def hate(id1, id2):
    POOL.hate(id1)
    POOL.hate(id2)
    bottle.redirect("/")

if __name__ == "__main__":
    POOL = Pool()

    if os.path.exists(FILE):
        POOL.load()

    def save_periodically():
        threading.Timer(60, save_periodically).start()
        POOL.save()

    save_periodically()

    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        bottle.run(host="localhost", port=8001, debug=True, reload=True)
    else:
        bottle.run(host="0.0.0.0", port=8001, reload=True)
