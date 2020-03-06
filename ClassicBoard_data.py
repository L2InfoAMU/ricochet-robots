
rouge1 = [[ 9,  1, 1, 3,  9, 1, 1, 1],
              [10, 12, 0, 0, 0,  0, 4, 0],
              [  8,   1, 0, 0, 0,  0, 3, 8],
              [  8,   0, 0, 0, 0,  0, 0, 0],
              [  8, 0, 6, 8, 0,  0, 0, 4],
              [12, 0, 1, 0, 0,  0, 2, 9],
              [  9, 0, 0, 0, 0, 0, 0, 4],
              [  8, 0, 0, 0, 0,   0, 2, 9]]

obR1 = [(4, 2), (5, 7), (1, 1), (2, 6)]

rouge2 = [[ 9,  1, 1, 3,  9, 1, 1, 1],
                [  8, 0, 0, 0, 0,  0, 0, 0],
              [  8,   0, 0, 0, 0,  6, 8, 0],
              [  8,   0, 4, 0, 0,  1, 0, 0],
              [ 12, 0, 3, 8, 0,  0, 0, 0],
              [  9, 4, 0, 0, 0,  0, 2, 12],
              [ 10, 9, 0, 0, 0, 0, 0, 5],
              [  8, 0, 0, 0, 0,   0, 2, 9]]

obR2 = [(2, 5), (6, 1), (5, 7), (4, 2)]

rouge3 = [[ 9,  3, 9, 1,  5, 1, 1, 1],
                [  8, 0, 0, 0, 3,  8, 0, 0],
              [  8,   0, 0, 0, 0,  0, 0, 0],
              [  10, 12, 0, 0, 0,  0, 0, 0],
              [ 8, 1, 0, 0, 0,  4, 0, 0],
              [ 12, 0, 0, 0, 2,  9, 0, 0],
              [ 9, 0, 0, 6, 8, 0, 0, 4],
              [  8, 0, 0, 1, 0,   0, 2, 9]]

obR3 = [(6, 3), (5, 5), (3, 1), (1, 4)]

bleu1 = [[ 9,  1, 1, 3,  9, 1, 1, 1],
              [  8,   0, 0, 0, 0,  6, 8, 0],
              [  10,  12, 0, 0, 0,  1, 0, 0],
              [  12, 1, 0, 0, 0,  0, 4, 0],
              [ 9, 0, 0, 0, 0,  2, 9, 0],
              [  8, 0, 4, 0, 0,  0, 0, 0],
              [ 8, 0, 3, 8, 0, 0, 0, 4],
              [  8, 0, 0, 0, 0,   0, 2, 9]]

obB1 = [(6, 2), (4, 6), (2, 1), (1, 5)]

bleu2 = [[ 9,  1, 5, 1,  3, 9, 1, 1],
              [  8,   2, 9, 0, 0,  0, 0, 0],
              [  8,  0, 0, 0, 0,  0, 0, 0],
              [  8, 0, 0, 0, 0,  2, 12, 0],
              [ 12, 0, 0, 0, 4,  0, 1, 0],
              [  9, 0, 0, 0, 3,  8, 0, 0],
              [ 8, 6, 8, 0, 0, 0, 0, 4],
              [  8, 1, 0, 0, 0,   0, 2, 9]]

obB2 = [(3, 6), (1, 2), (5, 4), (6, 1)]

bleu3 = [[ 9,  1, 1, 1,  1, 3, 9, 1],
              [  8,   0, 0, 4, 0,  0, 0, 0],
              [  8,  0, 2, 9, 0,  0, 0, 0],
              [  12, 0, 4, 0, 2,  12, 0, 0],
              [ 9, 0, 3, 8, 0,  1, 0, 0],
              [  8, 0, 0, 0, 6,  8, 0, 0],
              [ 8, 0, 0, 0, 1, 0, 0, 4],
              [  8, 0, 0, 0, 0,   0, 2, 9]]

obB3 = [(3, 5), (2, 3), (4, 2), (5, 4)]

vert1 = [[ 9,  3, 9, 1,  5, 1, 1, 1],
              [  8,   4, 0, 2, 9,  0, 0, 0],
              [  8,  3, 8, 0, 0,  0, 0, 0],
              [  8, 0, 0, 0, 0,  0, 6, 8],
              [ 8, 0, 0, 0, 0,  0, 1, 0],
              [ 12, 0, 0, 0, 0,  0, 0, 0],
              [ 9, 0, 2, 12, 0, 0, 0, 4],
              [  8, 0, 0, 1, 0,   0, 2, 9]]

obV1 = [(6, 3), (3, 6), (1, 4), (2, 1)]

vert2 = [[ 9,  1, 1, 1,  3, 9, 1, 1],
              [  8,   4, 0, 0, 0,  0, 6, 8],
              [  10,  9, 0, 0, 0,  0, 1, 0],
              [  8, 0, 0, 0, 0,  0, 0, 0],
              [ 8, 0, 0, 0, 0,  0, 4, 0],
              [ 12, 0, 0, 0, 0,  0, 3, 8],
              [ 9, 0, 2, 12, 0, 0, 0, 4],
              [  8, 0, 0, 1, 0,   0, 2, 9]]

obV2 = [(5, 6), (1, 6), (6, 3), (2, 1)]

vert3 = [[ 9,  3, 9, 5,  1, 1, 1, 1],
              [  8,   0, 2, 9, 0,  0, 0, 0],
              [  8,  0, 0, 0, 0,  0, 0, 0],
              [  8, 0, 0, 0, 0,  0, 6, 8],
              [ 10, 12, 0, 0, 0,  0, 1, 0],
              [ 8, 1, 0, 0, 4,  0, 0, 0],
              [ 12, 0, 0, 0, 3, 8, 0, 4],
              [  9, 0, 0, 0, 0,   0, 2, 9]]

obV3 = [(6, 4), (3, 6), (4, 1), (1, 3)]

jaune1 = [[ 9,  1, 1, 3,  9, 1, 1, 1],
              [  8,   0, 0, 0, 0,  2, 12, 0],
              [  8,  4, 0, 0, 0,  0, 1, 0],
              [  8, 3, 8, 0, 0,  4, 0, 0],
              [ 8, 0, 0, 0, 2,  9, 0, 0],
              [ 8, 0, 6, 8, 0,  0, 0, 6],
              [ 12, 0, 1, 0, 0, 0, 0, 5],
              [  9, 0, 0, 0, 0,   0, 2, 9]]

obJ1 = [(1, 6), (3, 1), (5, 2), (4, 5)]

jaune2 = [[ 9,  1, 1, 1,  3, 9, 1, 1],
              [  8,   0, 6, 8, 0,  0, 0, 0],
              [  8,  0, 1, 0, 0,  0, 0, 0],
              [  10, 12, 0, 0, 0,  0, 4, 0],
              [ 12, 1, 0, 0, 0,  2, 9, 0],
              [ 9, 0, 0, 0, 0,  4, 0, 0],
              [ 8, 0, 0, 0, 0, 3, 8, 4],
              [  8, 0, 0, 6, 8, 0, 2, 9]]

obJ2 = [(6, 5), (4, 6), (1, 2), (3, 1)]

jaune3 = [[ 9,  1, 3, 9,  1, 1, 1, 1],
              [  8,   0, 0, 0, 2,  12, 0, 0],
              [  8,  0, 0, 0, 0,  1, 0, 6],
              [  12, 0, 0, 0, 0,  0, 0, 1],
              [ 9, 0, 0, 6, 8,  0, 4, 0],
              [ 8, 4, 0, 1, 0,  2, 9, 0],
              [ 8, 3, 8, 0, 0, 0, 0, 4],
              [  8, 0, 0, 0, 0, 0, 2, 9]]

obJ3 = [(1, 5), (6, 1), (4, 3), (5, 6)]


jaunes = [jaune1, jaune2, jaune3]
verts = [vert1, vert2, vert3]
bleus = [bleu1, bleu2, bleu3]
rouges = [rouge1, rouge2, rouge3]

classicBoardData = [bleus, jaunes, rouges, verts]

objectifsJaunes = [obJ1, obJ2, obJ3]
objectifsVerts = [obV1, obV2, obV3]
objectifsBleus = [obB1, obB2, obB3]
objectifsRouges = [obR1, obR2, obR3]
classicBoardGoals = [objectifsBleus, objectifsJaunes, objectifsRouges, objectifsVerts]
couleurs = { "bleu" : 1, "jaune" : 2, "rouge" : 3, "vert" : 4}