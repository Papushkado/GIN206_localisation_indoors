# Cooja

C'est un simulateur de réseau fourni par Contiki. Pratique pour tester sans
charger les codes.

## Installation et utilisation

Dans le répertoire contenant Contiki :

```sh
git submodule update --init

sudo apt install ant
cd tools/cooja
ant run
```

Après installation, la commande `ant run` suffit.

En dehors de Instant Contiki, la commande `git submodule` échoue car il y a un
module qui n'existe plus sur `github`. Pour régler le problème, on supprime ce
module du répertoire _git_ en suivant les instructions sur
<https://gist.github.com/myusuf3/7f645819ded92bda6677>.

## Mettre en place un _border router_

<https://docs.contiki-ng.org/en/develop/doc/tutorials/Cooja-simulating-a-border-router.html>
