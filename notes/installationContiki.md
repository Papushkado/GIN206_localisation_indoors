# Installation de Contiki

Il y a deux méthodes :

- installation du répertoire _git_ de Contiki sur une VM Ubuntu LTS ;
- installation de InstantContiki : c'est une VM Ubuntu préconfigurée avec tous
  les outils déjà installés, mais la version d'Ubuntu installée est vieille.

Je préfère la première méthode car préférant avoir une version Ubuntu à jour,
mais la deuxième demande beaucoup moins de travail.

## Installation de Contiki sur Ubuntu-22.04.4-desktop-amd64.iso

Sources :

- <https://docs.contiki-ng.org/en/develop/doc/getting-started/Toolchain-installation-on-Linux.html>
- <https://anrg.usc.edu/contiki/index.php/Installation>

### Installation de `mspgcc` pour les plateformes Wismote

On compile `mspgcc` directement depuis la source, car le package Ubuntu a une
version trop vieille qui ne permet pas de compiler. `Stow` sert à rien mais
c'est pour pas modifier le script.

```sh
sudo apt update
sudo apt install build-essential stow texinfo

wget https://raw.githubusercontent.com/contiki-ng/contiki-ng/develop/tools/toolchain/msp430/buildmsp.sh
sudo mdkir /usr/local/stow/mspgcc-4.7.4
sudo ./buildmsp.sh
# On ajoute les exécutables dans PATH
echo 'PATH="/usr/local/stow/mspgcc-4.7.4/bin:$PATH"' >> ~/.profile
```

On vérifie que cela marche avec `msp430-gcc --version`.

### Installation de `arm-none-eabi-gcc` pour les plateformes Imote2

On télécharge la toolchain sur la page <https://developer.arm.com/downloads/-/gnu-rm>.

```sh
wget -O https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2
tar -xvf gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2
mv gcc-arm-none-eabi-10.3-2021.10 /usr/local/stow
# On ajoute les exécutables dans PATH
echo 'PATH="/usr/local/stow/gcc-arm-none-eabi-10.3-2021.10/bin:$PATH"' >> ~/.profile
```

On vérifie que l'installation marche avec `arm-none-eabi-gcc --version`.

### Installation de Contiki

On clone directement et on ne prend pas la release 3.0 parce que j'ai eu des
problèmes de compilation pour Wismote avec cette version.

```sh
sudo apt install git
git https://github.com/contiki-os/contiki/archive/3.0.zip
```

### Compilation

On se place dans un répertoire donné contenant le code source `C`.

```sh
make TARGET=wismote
# ou pour Imote2
make TARGET=zoul
```

### Chargement du code sur les cartes

USB sans sudo (il faut se déconnecter puis se reconnecter pour que cela prenne
effet). `gin` est à changer selon le nom d'utilisateur.

```sh
sudo usermod -a -G plugdev gin
sudo usermod -a -G dialout gin
```

#### Wismote

Pour charger le code sur une carte Wismote, il faut `mspdebug`. Encore une
fois, le package Ubuntu est vieux donc on compile depuis la source.

```sh
sudo apt install libusb-dev libreadline-dev
wget https://github.com/dlbeer/mspdebug/archive/refs/tags/v0.25.zip
cd mspdebug-0.25
make
sudo make install

sudo mpsdebug olimex
> prog filename.wismote
```

Pour voir le `stdout`, on peut utiliser `sudo putty` puis choisir
`/dev/ttyUSB0` et `115200` pour "Speed". Sinon, il y a `screen /dev/ttyUSB0
115200`. Dans les deux cas, il faut installer les packages correspondants.

#### Imote2

_Cf._ le `README.md` de la plateforme (`platform/zoul/README.md` dans le
répertoire _git_ de Contiki).

On doit installer :

```sh
sudo apt-get install python3-serial
```

## Installation de InstantContiki3.0

### Installation de la VM

On télécharge la VM sur
<https://sourceforge.net/projects/contiki/files/Instant%20Contiki/>. Ensuite,
on décompresse le fichier avec `unzip` (prend deux ou trois minutes). À
l'intérieur du répertoire se trouve des fichiers _VMware_ d'extension `vmdk`
(et autres). Je préfère `virt-manager` mais ce dernier ne peut lire les
fichiers de _VMware_ directement. Pour régler ce problème, on exécute :

```sh
qemu-img convert -O qcow2 Instant_Contiki_Ubuntu_12.04_32-bit.vmdk InstantContiki.qcow2
```

Puis on crée une nouvelle VM avec l'option d'installation depuis une image
virtuelle déjà existante, et on choisit `InstantContiki.qcow2`.

### Compilation et chargement du code sur les cartes

_Cf._ la première méthode, mais en sautant les étapes d'installation des outils
et de configuration de l'utilisateur `gin`.
