#!groovy​

// Jenkinsfile IC.
// Utilisé pour la construction
// c10x version: 03.02.00

// README : configurer pour un projet en modifiant les blocs avec un TODO.

/**
* CONFIGURATION JENKINS !
*
* Dans la configuration "Pipeline"
* Spécifier ${gitlabBranch} dans [ Branches to build ->	Branch Specifier (blank for 'any') : ______ ]
*
* [ Branches to build -> Branch Specifier (blank for 'any') : ${gitlabBranch} ]
*/

// ####################################################################################
// ## CONSTANTES DU JOB
// ####################################################################################

/** Nom du projet /application */
//TODO: mettre le nom du projet/application
String NOM_PROJET = 'ortools-integration'

/** Nom du composant */
//TODO: mettre le nom du composant
String NOM_COMPOSANT = 'compilation'

/** 
 * Branche d'intégration continue STABLE sur laquelle on lance des tâches avances (ex : sonar). 
 * Permet de ne pas lancer Sonar sur des branches de fix ou de feature
 **/
// TODO: remplacer par la branche a scanner pas sonarqube
String BRANCHE_STABLE = 'develop'

/** Nom du projet sur INCA */
String NOM_PROJET_INCA = NOM_PROJET

/** Nom de l'image docker */
String NOM_DOCKER_IMAGE = "${NOM_PROJET}-${NOM_COMPOSANT}" 

/** Label de l'agent Jenkins sur lequel on construit l'image docker du projet */
String SLAVE_DOCKER = "${NOM_PROJET}-centos"

//####################################################################################
//## PARAMETRES DEPUIS Jenkins
//####################################################################################

/** Version en cours de construction, utilisée uniquement lors de l'étape de préparation de la livraison */
String versionApp = params.VERSION_APP ?: 'IC'

/** Si true : lancement des tâches de preparation de livraison > construction docker */
boolean doitPreparerLivraison = (params.PREPARER_LIVRAISON ?: false) == true;

/** Si true : création d'un tag git */
boolean doitTagger = (params.DOIT_TAGGER ?: false) == true;

/** Si true : publication dans INCA de l'image docker (optionnel, on peut la construire en dev directement sans avoir besoin de la livrer) */
boolean doitPublierInca = (params.PUBLIER_INCA ?: false) == true;

/** Si true : compilation de Osi et installation dans repMaui **/
boolean doitCompilerOsi = params.DOIT_COMPIL_OSI;

/** Version d'OSI à compiler. N'a d'effet que si doitCompilerOsi = true **/
String verOsi = params.VERSION_OSI ?: '0.108.3';

/** Version de Boost à compiler. N'a d'effet que si doitCompilerOsi = true **/
String verBoost = params.VERSION_BOOST ?: '1_71_0';

/** Si true : run de tests sur Osi. N'a d'effet que si doitCompilerOsi = true **/
boolean doitTesterOsi = (params.DOIT_TEST_OSI ?: false) == true;


//####################################################################################
//## VARIABLES DU JOB
//####################################################################################

/** version du composant construit */
String buildVer = "${versionApp}-build${env.BUILD_NUMBER}"

/** branch en cours de construction */
String currentBranch

//####################################################################################
//## VARIABLES CALIN
//####################################################################################

/** Répertoire d'installation de XPRESS sur CALIN **/
String repMaui = "/applis/${NOM_PROJET}"

/** Répertoire d'installation de XPRESS sur CALIN **/
String repXpress = '/applis/xpress'

//####################################################################################
//## PIPELINE
//####################################################################################

echo "## PARAMETRES DU BUILD #######"
echo "$params"
echo "## / PARAMETRES DU BUILD #######"

// Execution sur le slave CENTOS du projet
node("rte-math-prog-linux") {
	try {
		// export de la buildVersion pour le job IC/DC parent qui fait la mise à jour du fichier compose. */
		env.BUILD_VERSION = buildVer
		
		// stageDevin ('🦊 Checkout') {
		// 	echo "🦊 Recuperation du code source de Git"
		// 	// On force la suppression du workspace pour garantir de travailler sur un projet git propre
		// 	cleanWs()

		// 	// checkout du projet et récupération de la branche courante
		// 	def result = gitCheckout {}
		// 	currentBranch = "${result['GIT_BRANCH']}"

		// 	// init de la config git (email, userName)
		// 	utils.gitInitConfig()
		// }
		// stageDevin('📦 Compile BOOST', doitCompilerOsi) {
		// 	echo "🏭 Compilation de la librairie BOOST"
		// 	try {
		// 		sh "cd third-party && tar xzf boost_${verBoost}.tar.gz && rm -f boost_${verBoost}.tar.gz"
		// 		sh "mkdir -p ${repMaui}"
		// 		sh "chmod +x -R third-party/boost_${verBoost} && cd third-party/boost_${verBoost} && ./bootstrap.sh && ./b2 --with-test --prefix=${repMaui}/boost install"
		// 		sh "rm -rf third-party/boost_${verBoost}"
		// 	} catch (Exception e) {
		// 		echo "🛑 Impossible d'extraire/compiler BOOST. Avez-vous bien place l'archive de la bonne version dans le repertoire 'third-party' ?"
		// 		currentBuild.result = 'ABORTED'
		// 		error(e.getMessage())
		// 	}
		// }
		// stageDevin ('🏭 Build MAUI') {
		// 	echo "🏭 Compilation MAUI"
		// 	sh "cd icdc/lua2sh && mkdir build && cd build && cmake ../ && make -j8 && chmod +x lua2sh"
		// 	sh "./icdc/lua2sh/build/lua2sh ${WORKSPACE}/icdc/modulefiles/maui/1.0.0.lua ${WORKSPACE}/icdc/env.sh";
		// 	sh "chmod +x icdc/env.sh"
		// 	sh "chmod +x third-party/build-wrapper/build-wrapper-linux-x86-64"
		// 	sh "source ./icdc/env.sh > /dev/null && mkdir build && cd build && cmake -DCODE_COVERAGE=TRUE -DCMAKE_BUILD_TYPE=Debug ../"
		// 	sh "source ./icdc/env.sh > /dev/null && cd build && ../third-party/build-wrapper/build-wrapper-linux-x86-64 --out-dir ../bw_output make -j8"
		// }
		// stageDevin ('⚗️ Unit Test'){
		// 	echo "⚗️ Lancement des tests unitaires"
		// 	sh "source ./icdc/env.sh > /dev/null && cd build && export MAUI_testDataDir=${WORKSPACE}/test-data && make test -j8"
		// }
		// stageDevin ('🔬 Code Quality', BRANCHE_STABLE == currentBranch) {
		// 	echo "🔬 Analyse sonar du code sur la branche stable de développement"
		// 	sh "cd build && rm -rf ./*"
		// 	sh "source ./icdc/env.sh && cd build && cmake -DCODE_COVERAGE=TRUE -DCMAKE_BUILD_TYPE=Debug ../"
		// 	sh "source ./icdc/env.sh && cd ./build && export MAUI_testDataDir=${WORKSPACE}/test-data && make code-coverage -j8"
		// 	// Clean non relevant reports
		// 	sh "rm -f ./build/coverage/reports/#usr#*"
		// 	sh "rm -f ./build/coverage/reports/#applis#*"
		// 	//sh "rm -f ./build/coverage/reports/*#include#*"
		// 	sh "rm -f ./build/coverage/reports/*#test#*"
		// 	sonar {
		// 		useMaven = "false"
		// 		scanVersion = "scan3.3"
		// 	}
		// }
		// stageDevin('🚀 Publish to Nexus'){
		// 	echo "🚀 Publication de la version : ${buildVer}, à partir de (tag/branch) : ${currentBranch}"
		// 	// First rebuild Release version and put in new directory
		// 	sh "rm -rf ./build && source ./icdc/env.sh && mkdir build && cd build && cmake -DCODE_COVERAGE=FALSE -DCMAKE_BUILD_TYPE=Release ../"
		// 	sh "source ./icdc/env.sh && cd build && make -j8"
		// 	sh "mkdir livraison"
		// 	// TO DO : ajouter flag pour pusher les dépendances sur Nexus
		// 	sh "cp ${repMaui}/lib -r livraison && cp ${repMaui}/lib64 -r livraison && cp ${repMaui}/include -r livraison"
		// 	sh "cp build/src/maui-dispo livraison"
		// 	sh "cp icdc/modulefiles -r livraison"
		// 	sh "cp icdc/sbatch_maui_dispo.sh livraison"
		// 	// Push to Nexus
		// 	publishRaw {
		// 		wip = !(doitPublierInca || doitTagger)
		// 		buildVersion = buildVer
		// 	}
		// }
		// stageDevin ('🏷️Tag', doitTagger) {
		// 	echo "🏷️ Creation du tag de build"
		//     String msg = "Tag Jenkins ${buildVersion}\n\n 🏭 ${env.BUILD_URL}";
		// 	gitTag{
		// 		tagName = buildVersion
		// 		doitPush = true
		// 		tagMsg = msg
		// 	}
		// }
	} catch (e) {
		// notify{
		// 	// BAL MAUI
		// 	to = 'rte-dsit-maui@rte-france.com'
		// 	errorMsg = e.toString()
		// }
		throw e;
	} finally {
		stageDevin('♻️ Cleanup') {
			echo "♻️ Nettoyage du workspace"
			cleanWs()
		}
	}
}