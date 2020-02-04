# ortools-integration
## Sous Windows
### Pré-requis
- Visual Studio 15 2017 Win64
- cmake 3.10
- git 2.8 (& git-bash)
- ...

### Procédure
Dans un terminal git bash :
```bash
git clone https://github.com/rte-france/ortools-integration.git -b master
cd ortools-integration
```
Vous pouvez éditer le fichier de configuration __subrepos/scripts/subrepos/scripts/config.sh__

Une fois celà fait, lancer la configuration, le build et l'install d'ortools :
```bash
bash subrepos/scripts/Windows/2_OR-Tools_config-build-install.sh
```

Et après, pour compiler les tests C++ et les lancer :
```bash
bash subrepos/scripts/Windows/4_OR-Tools_tests.sh
```
## Pour pouvoir contribuer sur les subrepos (dont le fork ortools de RTE)
Le plus simple est "d'installer" la fonctionnalité subrepo. Il s'agit simplement de scripts qui ajoute des fonctionnalités à git.
L'installation est très simple.
```bash
git clone https://github.com/ingydotnet/git-subrepo /path/to/git-subrepo
echo 'source /path/to/git-subrepo/.rc' >> ~/.bashrc
source ~/.bashrc
```
Les commandes sont relativements instinctives par rapport à git.  
Après avoir commité des modifications dans subrepos/OR-Tools, on peut les pusher avec
```bash
git subrepo push subrepos/OR-Tools
```
Plus de détails ici :  
https://github.com/ingydotnet/git-subrepo

