
# Crawler Web 

Dans ce projet, nous allons implémenter un simple [crawler
Web](http://fr.wikipedia.org/wiki/Robot_d%27indexation), c'est-à-dire un outil
capable de parcourir des pages Web en suivant les URLs. C'est typiquement ce que
font les moteurs de recherche comme Google. Notre objectif ici est de jouer avec
certains des concepts importants que nous avons découvert dans ce MOOC et de
pratiquer quelques modules de la librairie standard, mais nous ne chercherons
pas la performance parce que ça augmenterait très rapidement la complexité du
code et la difficulté du sujet. Cependant, vous constaterez que même si ce
crawler n'est pas adapté à crawler des millions de pages, il est parfaitement
capable de crawler des dizaines de milliers de pages et de vous rendre des
services (comme identifier les liens morts sur un site Web).

## Réalisation du crawler Web

Ce projet est découpé en trois niveaux de difficulté. Nous allons commencer par
le niveau avancé qui va vous demander d'écrire vous même tout le code en
fonction de nos spécifications. Pour le niveau intermédiaire, nous vous
fournirons une partie du code, et pour le niveau facile, nous vous fournirons
tout le code, votre travail se limitant à l'utilisation du crawler. À vous de
choisir où vous voulez commencer.

Il est très important de comprendre que le code que l'on vous propose d'écrire
n'est ni totalement fiable, ni validé par des tests. Est-ce que cela est un
problème pour ce projet ? Non, mais il est important dans du vrai code de
production de le fiabiliser au maximum (en capturant les exceptions avec des
reactions appropriés et en testant toutes les entrées) et de le tester (en
ajoutant, par exemple, des tests unitaires et des tests fonctionnels). Cela a
évidement un coût très élévé en terme d'augmentation du code (on peut facilement
multiplier par 2 ou 3 le nombre de lignes de code) et de temps de développement
(il va falloir imaginer tous les cas à tester).

Le but de notre crawler est, à partir de l'URL d'une page Web initiale,
d'extraire tous les liens hypertexte des pages parcourues, et d'utiliser ces
liens pour parcourir de nouvelles pages et extraire de nouveaux liens.

##### Niveau avancé

Tout notre programme peut-être écrit dans un même module. Nous avons dans ce
module deux classes.

 * La classe `HTMLPage` représente une page HTML. En particulier, une instance
de cette classe a&nbsp;:
  * un attribut `url` qui est une chaîne de caractères représentant l'URL
correspondant à la page Web,
  * un attribut `urls` qui est une liste de toutes les URLs trouvées dans cette
page,
  * un attribut `http_code` qui est le code HTTP retourné par la requête sur
`url`.

 Cette classe a trois méthodes.
  * Le constructeur prend comme argument une URL (sous forme d'une chaîne de
caractères).
  * La méthode `page_fetcher` prend comme argument une URL et retourne un
itérateur sur la page HTML ou une liste vide en cas d'erreur. On utilisera la
méthode `urlopen` dans librairie standard `urllib2`.
  * une méthode `extract_urls_from_page` qui va parcourir l'itérateur retourné
par la méthode `page_fetcher` et extraire toutes les URLs dans la page pour
créer une liste de toutes les URLs dans la page, liste qui sera référencée par
l'attribut `urls` de l'instance. Pour extraire une URL, on cherchera dans le
`body` de la page Web toutes les chaîne de caractères qui sont des valeurs de
l'attribut `href` et qui commencent par `http` ou `https` (notons que c'est loin
d'être parfait).

 * La classe `Crawler` permet de créer une instance d'un objet itérable qui à
chaque itération retournera un nouvel objet HTMLPage qui a été crawlé.
L'instance du crawler va avoir comme attributs
   * l'ensemble des sites à crawler
   * l'ensemble des sites déjà crawlés
   * un dictionnaire qui à chaque URL fait correspondre la liste de tous les
sites qui ont référencés cette URL lors du crawl.

 Cette classe a trois méthodes.
   * Le constructeur prend comme argument l'URL à partir de laquelle on commence
le crawl comme chaîne de caractères, le nombre maximum de sites à crawler et une
liste de domaines sur lesquels on veut restreindre le crawl.
   * la méthode update_sites_to_be_crawler qui prend comme argument un objet
HTMLpage et qui met à jour l'ensemble des sites à crawler en fonction des URLs
contenues dans la page passée en argument et des domaines sur lesquels on veut
restreindre le crawl.
   * une méthode `__iter__` qui retourne un itérateur qui à chaque appel à
next() retourne un nouvel objet HTMLpage qui fait partie du crawl


Ensuite, nous allons simplement créer un objet crawler et itérer dessus pour
extraire toutes les pages mortes (avec un code 404) que l'on trouve et tous les
sites qui référencent ces pages mortes.

##### Le mot de la fin

Nous avons à de nombreuses reprises évoqué la puissance de la librairie
standard, mais aussi des librairies tierces. En particulier, nous avons insisté
sur le fait qu'au démarrage d'un projet, il vaut mieux commencer par chercher si
une librairie Python ne fait pas déjà tout ou partie de ce que vous voulez
faire.

Il existe une librairie Python très puissante qui permet justement de faire des
crawlers&nbsp;: il s'agit de [Scrapy](http://scrapy.org/). Maintenant que vous
avez compris les bases d'un crawler Web, vous pourrez tirer pleinement bénéfice
des Scrapy.

Il existe également un librairie pour parser du code HTML, c'est
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/).
