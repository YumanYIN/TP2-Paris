"""
# Dijkstra
#
"""

from tkinter import *
import os
import math
import time

# Lecture des ficiers
fichier_noeuds = "Noeuds.csv"
fichier_arcs = "Arcs.csv"

sommet_depart = 23160
sommet_destination = 27195

degre_vers_radian = math.pi / 180.0

print("****** Lecture Noeuds *******")

LesNoeuds = open(fichier_noeuds, "r")
# format du fichier  indice \t long \t lat \n
touslesnoeuds = LesNoeuds.readlines()
LesNoeuds.close()

Longitude = []
Latitude = []

for un_noeud in touslesnoeuds:
    ce_noeud = un_noeud.split("\t")
    noeud = int(ce_noeud[0])
    Long = float(ce_noeud[1])
    Long = Long * degre_vers_radian
    Longitude.append(Long)
    Lat = float(ce_noeud[2].strip("\n"))
    Lat = Lat * degre_vers_radian
    Latitude.append(Lat)

minLat = min(Latitude)
maxLat = max(Latitude)
minLong = min(Longitude)
maxLong = max(Longitude)
NbNoeuds = len(Longitude)

print('****** Lecture Arcs *****')

LesArcs = open(fichier_arcs, "r")

touslesarcs = LesArcs.readlines()
LesArcs.close()

Origine = []
Destination = []
Longueur = []
Dangerosite = []

suiv = [[] for j in range(NbNoeuds)]
long_suiv = [[] for j in range(NbNoeuds)]
# prec = [[] for j in range(NbNoeuds)]
# numsuiv = [[] for j in range(0, NbNoeuds)]
# numprec = [[] for j in range(0, NbNoeuds)]

for un_arc in touslesarcs:
    cet_arc = un_arc.split("\t")
    Orig = int(cet_arc[0])
    Origine.append(Orig)
    Dest = int(cet_arc[1])
    Destination.append(Dest)
    Long = int(cet_arc[2])
    Longueur.append(Long)
    Dang = int(cet_arc[3].strip("\n"))
    Dangerosite.append(Dang)
    suiv[Orig].append(Dest)
    long_suiv[Orig].append(Longueur)



Nbarcs = len(Origine)
print('NbArcs= ', Nbarcs)

print('*** Dessin du graphe ***')


def TraceCercle(j, couleur, rayon):
    x = (Longitude[j] - minLong) * ratioWidth + border
    y = (Latitude[j] - minLat) * ratioHeight + border
    y = winHeight - y
    can.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, outline=couleur, fill=couleur)


fen = Tk()
fen.title('Carte de Paris')
coul_fond = "grey"  # ['purple','cyan','maroon','green','red','blue','orange','yellow']
coul_noeud = "black"

Delta_Long = maxLong - minLong
Delta_Lat = maxLat - minLat

border = 20  # taille en px des bords
winWidth_int = 900
winWidth = winWidth_int + 2 * border  # largeur de la fenetre
winHeight_int = Delta_Lat * (winWidth_int / 0.8) / Delta_Long
winHeight = winHeight_int + 2 * border  # hauteur de la fenetre : recalculee en fonction de la taille du graphe
ratio = 1.0  # rapport taille graphe / taille fenetre
ratioWidth = winWidth_int / Delta_Long  # rapport largeur graphe/ largeur de la fenetre
ratioHeight = winHeight_int / Delta_Lat  # rapport hauteur du graphe hauteur de la fenetre

can = Canvas(fen, width=winWidth, height=winHeight, bg=coul_fond)
can.pack(padx=5, pady=5)

#  cercles
rayon_noeud = 1  # rayon pour dessin des points
rayon_od = 5  # rayon pour origine et destination
for i in range(0, NbNoeuds):
    TraceCercle(i, coul_noeud, rayon_noeud)
TraceCercle(sommet_depart, 'green', rayon_od)
TraceCercle(sommet_destination, 'red', rayon_od)




"""
# Initialisation d'Algorithme de Dijkstra

# get the number of arc from i , j
def Arc(i, j):
    for u in range(0, Nbarcs):
        if Origine[u] == i and Destination[u] == j:
            return u
    return -1
"""
# liste Candidats qui ne contient que
# les sommets qui ont un potentiel non infini.
Candidat = [[] for j in range(0, NbNoeuds)]
# Initialiser cette liste Candidat avec les successeurs de sommet_depart.
for x in range(0, NbNoeuds):
    for y in range(0, len(suiv[x])):
        Candidat[x][y].append(Longueur[t])



# get now time as start time
time_start = time.clock()

infini = 99999
Pi = [infini for j in range(NbNoeuds)]

Marque = [False for j in range(NbNoeuds)]
LePrec = [-1 for j in range(NbNoeuds)]

Pi[sommet_depart] = 0
Marque[sommet_destination] = True

for k in suiv[sommet_depart]:
    Pi[k] = Longueur[Arc(sommet_depart, k)]

"""
# Algorithme de Dijkstra
"""
fini = False
NbSommetsMarques = 1
while not fini:
    minPi = infini
    for j in range(0, NbNoeuds):
        if not Marque[j] and Pi[j] < minPi:
            minPi = Pi[j]
            ce_sommet = j
    Marque[ce_sommet] = True
    NbSommetsMarques += 1
    if NbSommetsMarques % 100 == 0:
        print(NbSommetsMarques)
    TraceCercle(ce_sommet, 'yellow', 1)

    if ce_sommet == sommet_destination:
        fini = True

    for k in suiv[ce_sommet]:
        if not Marque[k]:
            # NewPot : NewPotentiel
            NewPot = Pi[ce_sommet] + Longueur[Arc(ce_sommet, k)]
            if NewPot < Pi[k]:
                Pi[k] = NewPot
                # let ce_sommet as the predecesseur of new potiential sommet
                # for create the chemin
                # pour reconstruire le chemin
                LePrec[k] = ce_sommet


time_end = time.clock()
print(time_end - time_start)
can.mainloop()