GENERIC_LOG()

if(MSVC)
	add_compile_definitions("_CRT_SECURE_NO_WARNINGS")
	set(BUILD_SHARED_LIBS OFF)
	SET(CMAKE_VS_INCLUDE_INSTALL_TO_DEFAULT_BUILD 1)
	SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif(MSVC)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${ORTOOLS_INSTALL_DIR}/include ${LIBS_INSTALL_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR})

function(createCppTest PACKAGE_NAME testName)
	set(EXECUTABLE_NAME ${PACKAGE_NAME}_${testName})
	set (SRC_EXEC ./${PACKAGE_NAME}/${testName}/main.cpp ./cppTestsUtils.cpp)
	add_executable (${EXECUTABLE_NAME} ${SRC_EXEC})
	
	#target_compile_definitions(${EXECUTABLE_NAME} PUBLIC USE_XPRESS NOMINMAX USE_GLOP USE_BOP USE_CBC USE_CLP)
	if (MSVC)
		#target_link_libraries(${EXECUTABLE_NAME} PUBLIC ${ORTOOLS_INSTALL_DIR}/lib/ortools.lib)
		#target_link_libraries(${EXECUTABLE_NAME} PRIVATE ${LIBS_INSTALL_DIR}/lib/*.lib ws2_32.lib)
		#target_compile_definitions(${EXECUTABLE_NAME} PUBLIC USE_CBC)
		if (USE_XPRESS)
			target_compile_definitions(${EXECUTABLE_NAME} PUBLIC USE_XPRESS)
			# target_link_libraries(${EXECUTABLE_NAME} PUBLIC ${XPRESSDIR}/lib/xprs.lib)
		endif(USE_XPRESS)
	else()
	endif(MSVC)
	
	target_link_libraries(${EXECUTABLE_NAME} PUBLIC ortools::ortools)

	if (USE_SIRIUS)
		target_compile_definitions(${EXECUTABLE_NAME} PUBLIC USE_SIRIUS)
		target_link_libraries(${EXECUTABLE_NAME} PUBLIC bib_solveur)
	endif()
	
	add_test(NAME "${EXECUTABLE_NAME}" COMMAND ${EXECUTABLE_NAME})
endfunction()

FUNCTION(GENERATE_CPP_TESTS PACKAGE_NAME)
	SUBDIRLIST(SUBDIRS ${CMAKE_CURRENT_SOURCE_DIR}/${PACKAGE_NAME})

	FOREACH(subdir ${SUBDIRS})
		createCppTest(${PACKAGE_NAME} ${subdir})
	ENDFOREACH()
ENDFUNCTION()

GENERATE_CPP_TESTS(Basic)
IF (USE_XPRESS)
	GENERATE_CPP_TESTS(Xpress)
ENDIF()
#GENERATE_CPP_TESTS(Cbc)

if (USE_SIRIUS)
	GENERATE_CPP_TESTS(Sirius)
ENDIF()