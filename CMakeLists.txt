CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
project(ortools_rte_integration_tests VERSION 0.1.0)

set(GFLAGS_USE_TARGET_NAMESPACE TRUE)
find_package(ortools CONFIG REQUIRED)

if (USE_SIRIUS)
	find_package(bib_solveur REQUIRED)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(utilsRTE)
GENERIC_LOG()

include(CTest)
enable_testing()

add_subdirectory(src)
