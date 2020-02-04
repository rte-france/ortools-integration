# Sirius API
# Table of Contents
* [Sirius API](   #sirius-api)
  * [Comment utiliser Sirius via l'API C en direct](#comment-utiliser-sirius-via-lapi-c-en-direct)
      * [Récupération de la bibliotèque](#récupération-de-la-bibliotèque)
      * [Utilisation avec cmake](#utilisation-avec-cmake)
      * [Compiler le projet](#compiler-le-projet)
  * [Comment utiliser Sirius via or-tools en C++](#comment-utiliser-sirius-via-or-tools-en-c)
  * [Comment utiliser Sirius via or-tools en Python](#comment-utiliser-sirius-via-or-tools-en-python)
  * [Comment compiler or-tools avec Sirius](#comment-compiler-or-tools-avec-sirius)
      * [C++](#c)
      * [Python](#python)

## Comment utiliser Sirius via l'API C en direct
### Récupération de la bibliotèque
La dernière version de l'API C est disponible ici :  
https://edcloud.eurodecision.com/index.php/s/CP2w4FrKa0C6E3E  
Mot de passe : Sirius

Le répertoire obtenu en dézippant l'archive sera celui à pointer avec SIRIUSDIR.
### Utilisation avec cmake
SIRIUSDIR peut être une variable d'environnement, ou bien passée à cmake via un -D (qui prendra la priorité sur la variable d'environnement) 
```
cmake -DSIRIUSDIR="C:\MesLibs\Sirius" mesSources/
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
### Compiler le projet
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
## Comment utiliser Sirius via or-tools en C++

## Comment utiliser Sirius via or-tools en Python

## Comment compiler or-tools avec Sirius
### C++
### Python

