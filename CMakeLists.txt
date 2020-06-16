CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
project(ortools_rte_integration_tests VERSION 0.1.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

set(GFLAGS_USE_TARGET_NAMESPACE TRUE)
find_package(ortools CONFIG REQUIRED)


if(USE_XPRESS)
  find_package(XPRESS REQUIRED)
endif()

if (USE_SIRIUS)
	find_package(sirius_solver REQUIRED)
endif()

include(utilsRTE)
GENERIC_LOG()

include(CTest)
enable_testing()

add_subdirectory(src)
