CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
PROJECT(exempleAPIC)

SET(NOM_DE_VOTRE_TARGET ${PROJECT_NAME})

SET (SRCS src/main.c)
ADD_EXECUTABLE(${NOM_DE_VOTRE_TARGET} ${SRCS} )
	
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