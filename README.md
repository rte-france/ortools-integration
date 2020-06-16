# Pour CentOS 7
## Prérequis
### gcc
```bash
### Avec les droits root
yum install devtoolset-7-gcc*
```

### cmake
```bash
### Avec les droits root
yum install openssl-devel
sudo yum remove cmake -y
wget https://github.com/Kitware/CMake/releases/download/v3.16.4/cmake-3.16.4.tar.gz
tar xzf cmake-3.16.4.tar.gz
cd cmake-3.16.4
./bootstrap --prefix=/usr/local
make -j 4
make install
```

## Procédure de configuration et de build
```bash
### Activation globale du gcc récent
scl enable devtoolset-7 bash

### Clone du projet d'intégration
rm -rf ortools-integration
git clone https://github.com/rte-france/ortools-integration.git -b evol-cmakes
cd ortools-integration

### Configuration et build + install de Sirius
git clone https://github.com/rte-france/temp-pne.git -b metrix Sirius
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B Sirius/buildLinux -S Sirius/src
cmake --build Sirius/buildLinux/ --config Release --target install -j4

### Configuration et build + install d'ortools
git clone https://github.com/rte-france/or-tools.git -b rte_dev_sirius or-tools
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B or-tools/buildLinux -S or-tools/ -DUSE_SIRIUS=ON -DUSE_COINOR=ON -DBUILD_PYTHON=OFF -DBUILD_TESTING=OFF -DBUILD_DEPS=ON 
cmake --build or-tools/buildLinux/ --config Release --target install -j4

### Configuration et build des tests d'intégration
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B buildLinux -S . -DUSE_SIRIUS=ON
cmake --build buildLinux/ --config Release -j4

### Lancement des tests d'intégration
(cd buildLinux; ctest -C Release -V)
```




# Pour Windows ( !!! __WORK IN PROGRESS__ !!!)
## __A résoudre__
fixTemplate pour visual 2017  
link gflags (cherche gflags_nothreads_static.lib sans le chemin, alors qu'il a déjà ${chemin}/gflags_static.lib)

## Pré-requis
- Visual Studio 15 2017 Win64
- cmake 3.14 ?
- git 2.8 (& git-bash)
- ...

## Procédure de configuration et de build ( !!! __WORK IN PROGRESS__ !!!)
```bash
### Activation globale du gcc récent
scl enable devtoolset-7 bash

### Clone du projet d'intégration
git clone https://github.com/rte-france/ortools-integration.git -b evol-cmakes
cd ortools-integration

### Configuration et build + install de Sirius
git clone https://github.com/rte-france/temp-pne.git -b metrix Sirius
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B Sirius/buildWindows -S Sirius/src -G "Visual Studio 15 2017 Win64"
cmake --build Sirius/buildWindows/ --config Release --target install -j4

### Configuration et build + install d'ortools
git clone https://github.com/rte-france/or-tools.git -b rte_dev_sirius or-tools
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B or-tools/buildLinux -S or-tools/ -DUSE_SIRIUS=ON -DUSE_COINOR=ON -DBUILD_PYTHON=OFF -DBUILD_TESTING=OFF -DBUILD_DEPS=ON 
cmake --build or-tools/buildLinux/ --config Release --target install -j4

### Configuration et build des tests d'intégration
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="install" -B buildLinux -S . -DUSE_SIRIUS=ON
cmake --build buildLinux/ --config Release -j4

### Lancement des tests d'intégration
(cd buildLinux; ctest -C Release -V)
```

