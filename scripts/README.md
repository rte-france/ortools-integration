# POC AntaresV7 avec OR-Tools
## Procédure de build simplifiée
Cette procédure permet de compiler :
- La dll bib_solveur.dll (Sirius)
- La lib OR-Tools et ses dépendances
- La cible __antares-7.0-solver__ avec Sirius via OR-Tools activé
- Les autres cibles Antares sont compilable de manière classique via Visual Studio


>__Note : la version des sources de Sirius utilisée est composée des sources précédemment embarquée dans Antares, utilisable via l'ajout d'une API C.__

Dans une console git-bash.
```bash
git clone https://github.com/rte-france/Antares_Simulator.git -b dev_ql Antares_Simulator
cd Antares_Simulator
```
__Suivre la procédure du INSTALL.txt mais s'arrêter juste avant de lancer cmake (partie 2.2)__

Editer subrepos/scriptsED/config.sh si :
- Vous voulez changer de compilateur (Défaut :Visual Studio 15 2017 Win64)
- La variable d'environnement XPRESSDIR n'a pas été défini correctement
- Vous voulez activer CPLEX (changer ORTOOLS_CPLEX_SWITCH et définir CPLEXDIR correctement)

Dans le répertoire Antares_Simulator __(donc pas src !!!)__
```bash
bash subrepos/scriptsED/Windows/0_FullChainAuto.sh
```
Vous obtiendrez alors dans src/solver/Release l'exe __antares-7.0-solver.exe__

### Utilisation de l'exe Antares obtenu
Pour fonctionner, il doit être accompagné des dlls suivantes :
- bib_solveur.dll => ici _subrepos/Sirius/build/install/lib/Release/bib_solveur.dll_
- zlib.dll => ici _subrepos/OR-Tools/build/dependencies/install/bin/zlib.dll_
- Eventuellement les dll des solveur externe (XPRESS, CPLEX, ...) si elle ne sont pas déjà disponible dans le PATH (par défaut l'install d'XPRESS le fait)

---
---
---
---



# Sirius API
# Table of Contents

## 1. Comment utiliser Sirius via l'API C en direct
### 1.1. Récupération de Sirius et compilation
Commencez par cloner la dernière version des sources :
```
git clone https://github.com/rte-france/temp-pne.git -b pne_from_antares Sirius
```

Ensuite, il faut rentrer dans le répertoire "Sirius" ainsi créé, et lancer la configuration et la compilation :
```
cd Sirius
cmake -G "Visual Studio 15 2017 Win64" -B build -S src
cmake --build build --config Release --target INSTALL
```
Une fois la compilation et l'installation terminée, vous obtiendrez dans le sous répertoire build/install le répertoire à pointer avec SIRIUSDIR pour la suite.

### 1.2. Utilisation avec cmake
SIRIUSDIR peut être une variable d'environnement, ou bien passée à cmake via un -D (qui prendra la priorité sur la variable d'environnement) 
```
cmake -DSIRIUSDIR="C:\MesProjets\Sirius\build\install" mesSources/
```
SIRIUSDIR doit contenir :
+ includes/
+ lib/Release/ contenant bib_solveur.lib et bib_solveur.dll
+ _Pour Debug : lib/Debug/  contenant bib_solveur.lib et bib_solveur.dll_
```cmake
CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
PROJECT(VOTRE_PROJET)

...
# contenu de votre projet : sources, headers, creation des targets, ...
...

IF (USE_SIRIUS)

    # global, une seule fois pour toutes les targets
    IF (NOT SIRIUSDIR)
		SET(SIRIUSDIR $ENV{SIRIUSDIR})
	ENDIF (NOT SIRIUSDIR)
    IF (NOT SIRIUSDIR)
        MESSAGE(FATAL_ERROR "variable SIRIUSDIR not found")
    ENDIF (NOT SIRIUSDIR)
	GET_FILENAME_COMPONENT(SIRIUSDIR ${SIRIUSDIR} ABSOLUTE)

    # global, une seule fois pour toutes les targets
    IF (MSVC)
        INSTALL(FILES ${SIRIUSDIR}/lib/Release/bib_solveur.dll DESTINATION "${CMAKE_BINARY_DIR}/Release" CONFIGURATIONS Release)
        INSTALL(FILES ${SIRIUSDIR}/lib/Debug/bib_solveur.dll DESTINATION "${CMAKE_BINARY_DIR}/Debug" CONFIGURATIONS Debug)
    ENDIF (MSVC)

    # Pour chaque target qui utilise Sirius
	SET(SIRIUS_INCLUDES_DIR ${SIRIUSDIR}/includes)
	FILE(GLOB SIRIUS_INCLUDES ${SIRIUS_INCLUDES_DIR}/*.h)
	TARGET_INCLUDE_DIRECTORIES(${NOM_DE_VOTRE_TARGET} PUBLIC ${SIRIUS_INCLUDES_DIR})

    # Pour chaque target qui utilise Sirius
    IF (UNIX)
        TARGET_LINK_LIBRARIES(${NOM_DE_VOTRE_TARGET} PUBLIC ${SIRIUSDIR}/lib/libbib_solveur.so)
    ELSEIF (MSVC)
        TARGET_LINK_LIBRARIES(${NOM_DE_VOTRE_TARGET} optimized ${SIRIUSDIR}/lib/Release/bib_solveur.lib)
        TARGET_LINK_LIBRARIES(${NOM_DE_VOTRE_TARGET} debug ${SIRIUSDIR}/lib/Debug/bib_solveur.lib)
    ENDIF()
	
ENDIF(USE_SIRIUS)
```
### 1.3. Compiler le projet
```bash
# Exemple de compilation, à effectuer dans le répertoire exempleAPIC
# Il faut bien sur adapter "../SiriusInstall" à votre SIRIUSDIR
# on build INSTALL pour copier automatiquement bib_solveur.dll à coté de l'exe après l'avoir compilé
cmake -Bbuild -DUSE_SIRIUS=ON -DSIRIUSDIR="../SiriusInstall" -G"Visual Studio 15 2017 Win64" .
cmake --build build/ --config Release --target INSTALL 
```
Le binaire ainsi compilé ne peut pas fonctionner sans "bib_solveur.dll", qui doit donc être soit dans le PATH Windows, soit à coté de l'exe. Ici si on a compilé la target INSTALL, c'est fait automatiquement.
```
./build/Release/exempleAPIC.exe
```
## 2. Comment utiliser Sirius via or-tools en C++

## 3. Comment utiliser Sirius via or-tools en Python

### 3.1. Récupération de la bibliothèque
La dernière version d'ortools pour python (avec Sirius/Xpress/Cplex) est disponible ici :
https://edcloud.eurodecision.com/index.php/s/S5t3L18kbRtxHuu
Mot de passe : Sirius
### 3.2. Utilisation de la bibliothèque
Pour pouvoir utiliser le contenu de cette version, il faut lancer votre script depuis le répertoire contenant l'arborescence obtenue en dézippant l'archive.
Donc si vous lancez à partir de "monRepertoire" vous devez avoir "monRepertoire/ortools/linear_solver/"
Un exemple est fourni dans le fichier test.py. Pour la syntaxe ortools,  sinon se référer au site officiel : https://developers.google.com/optimization/introduction/python  
Vous aurez accès aux interfaces de solveur suivantes :
+ pywraplp.Solver.CPLEX_LINEAR_PROGRAMMING
+ pywraplp.Solver.XPRESS_LINEAR_PROGRAMMING
+ pywraplp.Solver.SIRIUS_LINEAR_PROGRAMMING
+ pywraplp.Solver.CPLEX_MIXED_INTEGER_PROGRAMMING
+ pywraplp.Solver.XPRESS_MIXED_INTEGER_PROGRAMMING
+ pywraplp.Solver.SIRIUS_MIXED_INTEGER_PROGRAMMING

## 4. Comment compiler or-tools avec Sirius
### 4.1. Pré-requis Windows
La machine doit avoir d'installé
* Visual Studio 2017 Community edition (avec composants C++)
* Git-bash
* Cmake (version >= 3.5.2, recommandé >= 3.10.xx)
* Python (version >= 3.7)
### 4.2. Pré-requis Linux
Sur une Debian 9 ou équivalente
* Visual Studio 2017 Community edition (avec composants C++)
* Git-bash
* Cmake (version >= 3.5.2, recommandé >= 3.10.xx)
* Python (version >= 3.7)
### 4.3. C++
#### 4.3.1. Récupération de dépendances précompilées.
Télécharger et désipper ortoolsDepInstall.zip https://eurodecision-my.sharepoint.com/:u:/p/eric_dumont_fr/ESsC1booMCVPqnyl-aPuBEYBf9OXDNL0_mpMRtVDOHpEdA?e=ah3yO3
Le répertoire ortoolsDepInstall (que vous pouvez renommer) devra être pointé par la variable ORTOOLSDEPDIR  
Voir le paragraphe [1.1. Récupération de Sirius et compilation](#11-r%C3%A9cup%C3%A9ration-de-sirius-et-compilation)

#### 4.3.2. Clonage des scripts de config et compil, et modification des chemins des solveurs et libs.
```
git clone git@edgitlab.eurodecision.com:RTE/ortoolsdevs.git -b master ortools_scripts
cd ortools_scripts
```
editer les scripts sirius-or-tools-configure-windows-prebuilt-libs.sh pour adpater les chemins et options :
  - ORTOOLSDEPDIR -> doit pointer sur le répertoire dézippé
  - SIRIUSDIR -> doit pointer sur un répertoire de Sirius d'une des branches possédant l'API C++ (par exemple celle fourni en 1)
  - CPLEXDIR et XPRESSDIR si besoin (XPRESSDIR est probablement déjà OK avec l'install classique de XPRESS).
  - Optionnel : ORTOOLSINSTALLDIR -> par défaut la lib compilée de ortools sera installée dans le sous répertoire "ortools_install_dir" du répertoire de source d'ortools que l'on va cloner en 3
Pour désactiver un solver (par exemple CPLEX) il suffit de :
  - Commenter la ligne commençant par lookForLib "${CPLEXDIR}" ... en la préfixant d'un # (dans le script de config et de build)
  - Changer l'option passé à CMAKE en -DUSE_CPLEX=OFF (uniquement dans le script de config)

#### 4.3.3. Ortools : Sources, config et compilation
```
git clone https://github.com/rte-france/or-tools.git -b rte_dev_sirius ortools_rte_dev_sirius
cd ortools_rte_dev_sirius

bash ../sirius-or-tools-configure-windows-prebuilt-libs.sh
bash ../sirius-or-tools-build-windows.sh
```

Si tous s'est bien passé, les lib et headers ont été installés dans ORTOOLSINSTALLDIR (par défaut le sous répertoire "ortools_install_dir")
Et les tests auront été lancés et tous en succès avec un message se terminant comme ceci :  
```
  ...
  17/18 Test #17: cc_strawberry_fields_with_column_generation_sirius ...   Passed    9.35 sec  
        Start 18: cc_strawberry_fields_with_column_generation_cplex  
  18/18 Test #18: cc_strawberry_fields_with_column_generation_cplex ....   Passed    7.57 sec  
  
  100% tests passed, 0 tests failed out of 18  
  
  Total Test time (real) =  71.41 sec  
```
#### 4) Antares avec ortools
##### A partir de zero (nouveau clone du repo)
```
git clone https://github.com/rte-france/Antares_Simulator.git -b dev_mr Antares_Simulator
```
Suivre les instructions d'installation mais s'arrêter avant de lancer le cmake "final" (exemple : cmake -G "Visual Studio 14 2015" -DCMAKE_BUILD_TYPE=release .)  

##### Ou bien à partir d'une installation existante pointant déjà sur le repo rte-france, faire le clean (git clean -xdf) et changer de branche
```
git fetch
git checkout dev_mr
```

##### Configuration via du cmake et compilation
Modifier si besoin le script "antares-or-tools-configure-windows.sh" pour changer les paths vers l'installation d'ortool, CPLEX, Sirius, etc.
```
cd Antares_Simulator/src
bash ${chemin_vers_les_scripts_de_compilation}/antares-or-tools-configure-windows.sh
cmake --build . --config Release --target antares-7.0-solver
```
Et ensuite pour pouvoir lancer il faut s'assurer que la dll du solveur choisi dans le code est disponible dans le path (bib_solveur.dll pour Sirius)
### Python

