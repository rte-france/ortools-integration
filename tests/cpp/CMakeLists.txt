CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
PROJECT(tests_cpp)

if(MSVC)
	add_compile_definitions("_CRT_SECURE_NO_WARNINGS")
	set(BUILD_SHARED_LIBS OFF)
endif(MSVC)

SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
SET(CMAKE_VS_INCLUDE_INSTALL_TO_DEFAULT_BUILD 1)
MESSAGE("CMAKE_BINARY_DIR : ${CMAKE_BINARY_DIR}")
MESSAGE("CMAKE_SOURCE_DIR : ${CMAKE_SOURCE_DIR}")

include_directories(${ORTOOLS_INSTALL_DIR}/include ${LIBS_INSTALL_DIR}/include)
enable_testing()

function(createTest testName)
	set(EXECUTABLE_NAME ${testName})
	set (SRC_EXEC ./${testName}/main.cpp)
	add_executable (${EXECUTABLE_NAME} ${SRC_EXEC})
	target_link_libraries(${EXECUTABLE_NAME} PUBLIC ${ORTOOLS_INSTALL_DIR}/lib/ortools.lib)
	
	target_compile_definitions(${EXECUTABLE_NAME} PUBLIC USE_XPRESS NOMINMAX USE_GLOP USE_BOP USE_CBC USE_CLP)
	if (MSVC)
		target_link_libraries(${EXECUTABLE_NAME} PRIVATE ${LIBS_INSTALL_DIR}/lib/*.lib ws2_32.lib)
		if (USE_XPRESS)
			target_link_libraries(${EXECUTABLE_NAME} PUBLIC ${XPRESSDIR}/lib/xprs.lib)
		endif(USE_XPRESS)
	endif(MSVC)
	
	add_test(NAME "${EXECUTABLE_NAME}" COMMAND ${EXECUTABLE_NAME}.exe)
endfunction()

MACRO(SUBDIRLIST result curdir)
  FILE(GLOB children RELATIVE ${curdir} ${curdir}/*)
  SET(dirlist "")
  FOREACH(child ${children})
    IF(IS_DIRECTORY ${curdir}/${child})
      LIST(APPEND dirlist ${child})
    ENDIF()
  ENDFOREACH()
  SET(${result} ${dirlist})
ENDMACRO()

SUBDIRLIST(SUBDIRS ${CMAKE_SOURCE_DIR})
FOREACH(subdir ${SUBDIRS})
  createTest(${subdir})
ENDFOREACH()

