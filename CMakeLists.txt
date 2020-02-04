CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
project(ortools_rte_integration_tests VERSION 0.1.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(utilsRTE)
GENERIC_LOG()

include(CTest)
enable_testing()

add_subdirectory(src)
