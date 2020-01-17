# ortools-integration
## Sous Windows
### Pré-requis
- Visual Studio 15 2017 Win64
- cmake 3.10
- git (& git-bash)
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
