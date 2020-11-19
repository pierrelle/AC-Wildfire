# Automates cellulaires : feu de forêt 

## Fonctionnel

### Consignes de base
 Dans ce projet scolaire, l'objectif est de simuler des feux de forêt. Les premières consignes étaient de tester des simulations avec des densités d'arbres variées, avec la règle qu'un arbre prend feu si au moins un de ses voisins directs est en feu. Ainsi, il est possible de voir quand il y percolation ou non. Par la suite, nous étions libre d'ajouter les éléments que nous souhaitions.
 
 ### Notre objectif
 Nous voulions faire une simulation se rapprochant plus de la réalité.
 
 ### Les ajouts
  - **Deux types d'arbres** : les arbres légers et les arbres lourds. Un arbre léger prend feu plus facilement qu’un arbre lourd. Visuellement, ils se différencient par les couleurs respectives vert clair et vert foncé. 
  - **Deux types de feu** : les petits feux et les gros feux. Un arbre commence par prendre légèrement feu, puis s’enflamme de manière plus importante. Visuellement, ils se différencient par les couleurs respectives rouge clair et rouge foncé.
  - **Le vent** : il peut provenir du nord, du sud, de l’est ou de l’ouest. Il modifie la portée du feu, lui permettant donc d'atteindre des arbres plus lointains dans la direction du vent.
  - **Des probabilités** : prenant en  compte le type de l’arbre, le nombre et le type des feux environnants.
  - **Un pare-feu** : c'est un méthode de coupe forestière visant à limiter la progragation des feux de forêts. Ici, ce sont des coupes linéaires divisant la forêt en plusieurs blocs.

  ## Technique

### Executer le programme
Toutes les libraires nécéssaires sont dans le fichier `requirements.txt`, une fois installées il suffit d'éxecuter le fichier `main.py`.

### Indices de la grille 
Chaque case de la grille correspond à un arbre. Pour cela elle a une valeur entière qui désigne l'état de l'arbre :

| Indice | Type d'arbre | Couleur |
| ------ |       ------ |   ------ |
| 0 | Aucun arbre | Blanc |
| 1 | Arbre léger | Vert clair |
| 2 | Arbre lourd | Vert foncé |
| 3 | Petit feu | Rouge clair |
| 4 | Grand feu | Rouge foncé |
| 5 | Etat de transition prise de feu | / |


### Probabilité qu'un arbre prenne feu 

	$p = min(\frac{nb_feu_3*transmission_feu_3 + nb_feu_4*transmission_feu_4}{resistance_arbre}, 1)$

Exemple : 
  - Si un arbre léger a pour voisin 2 arbres en feu, un en petit feu, un en grand feu, il a 70% de risque de prendre feu. Un arbre lourd a 54% de risque.
  - Si un arbre léger a pour voisin 4 arbres en feu, trois en petit feu, un en grand feu, il a 100% de risque de prendre feu. Un arbre lourd a 85% de risque.

