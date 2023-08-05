#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiNeighborhoodProcessing)

# main library
set(YayiNeighborhoodProcessingSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiNeighborhoodProcessingSRC
  ${YayiNeighborhoodProcessingSubdirectory}/yayiNeighborhoodProcessing.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/include/np_operators_adapters_t.hpp

  ${YayiNeighborhoodProcessingSubdirectory}/np_local_statistics.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/include/np_local_statistics_t.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/src/np_local_statistics.cpp
)


include_directories(${YayiNeighborhoodProcessingSubdirectory})
include_directories(${YayiNeighborhoodProcessingSubdirectory}/include)

add_library(YayiNeighborhoodProcessing ${YayiNeighborhoodProcessingSRC})
target_link_libraries(YayiNeighborhoodProcessing YayiImageCore YayiCommon)
set_target_properties(YayiNeighborhoodProcessing PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_NeighborhoodProcessing_")
install(TARGETS YayiNeighborhoodProcessing CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiNeighborhoodProcessingSRC}")


# Test project
project(yayiNeighborhoodProcessingTests)
set(yayiNeighborhoodProcessingTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiNeighborhoodProcessingTestsSRC
  ${yayiNeighborhoodProcessingTestsSubdirectory}/main.cpp
  ${yayiNeighborhoodProcessingTestsSubdirectory}/main.hpp
  
  ${yayiNeighborhoodProcessingTestsSubdirectory}/np_test_mean.cpp
)
include_directories(${yayiNeighborhoodProcessingTestsSubdirectory})
add_executable(YayiNeighborhoodProcessingTest ${yayiNeighborhoodProcessingTestsSRC})
target_link_libraries(YayiNeighborhoodProcessingTest YayiNeighborhoodProcessing YayiStructuringElement ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiNeighborhoodProcessingTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiNeighborhoodProcessingTest)


# Python project
project(yayiNeighborhoodProcessingPython)
set(yayiNeighborhoodProcessingPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(yayiNeighborhoodProcessingPythonSRC
 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.hpp
 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.cpp
 
 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighbor_statistics.cpp
)

include_directories(${yayiNeighborhoodProcessingPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiNeighborhoodProcessingPython "${yayiNeighborhoodProcessingPythonSRC}" "YayiNeighborhoodProcessing")
add_test(NAME YayiNeighborhoodProcessingPython-1 COMMAND ${PYTHON_EXECUTABLE} ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.py $<TARGET_FILE_DIR:YayiNeighborhoodProcessingPython>)

