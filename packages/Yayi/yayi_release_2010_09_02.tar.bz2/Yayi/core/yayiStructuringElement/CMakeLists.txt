#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#



project(yayiStructuringElement)

set(yayiStructuringElementSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiSESRC
  ${yayiStructuringElementSubdirectory}/yayiStructuringElement.hpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElement.cpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElementFactory.cpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElementNeighborListFactory.cpp
  
  ${yayiStructuringElementSubdirectory}/yayiStructuringElementChain.hpp
  
  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeNeighborhood_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeStructuringElement_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeStructuringElement_hexagon_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiStructuringElement_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiNeighborhoodStrategy_t.hpp
  
  ${yayiStructuringElementSubdirectory}/include/yayiDisjointPairedStructuringElement_t.hpp
  
  ${yayiStructuringElementSubdirectory}/yayiRuntimeStructuringElements_predefined.hpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElements_predefined.cpp
  
  ${yayiStructuringElementSubdirectory}/include/se_dispatcher.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiStructuringElementUtilities_t.hpp
  
)


include_directories(${yayiStructuringElementSubdirectory})
include_directories(${yayiStructuringElementSubdirectory}/include)
include_directories(${yayiStructuringElementSubdirectory}/src)
add_library(YayiStructuringElement ${YayiSESRC})
target_link_libraries(YayiStructuringElement YayiImageCore YayiCommon)
set_target_properties(YayiStructuringElement PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_SE_")
install(TARGETS YayiStructuringElement CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiSESRC}")




project(yayiStructuringElementTest)
set(yayiStructuringElementTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiSETestsSRC
  ${yayiStructuringElementTestsSubdirectory}/iterator_covering.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_tests_basic.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_runtime_tests.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_neighborhood_runtime_tests.cpp
  ${yayiStructuringElementTestsSubdirectory}/neigh_factory.cpp

  ${yayiStructuringElementTestsSubdirectory}/main.cpp
  ${yayiStructuringElementTestsSubdirectory}/main.hpp
)
add_executable(YayiStructuringElementTest ${yayiSETestsSRC})
target_link_libraries(YayiStructuringElementTest YayiStructuringElement YayiIO ${Boost_SYSTEM_LIBRARY}
                      ${Boost_TEST_EXEC_MONITOR_LIBRARY} )
add_test(yayiStructuringElementTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiStructuringElementTest)



# Python project
project(yayiStructuringElementPython)
set(yayiStructuringElementSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(yayiStructuringElementPythonSRC
 ${yayiStructuringElementSubdirectory}/structuringelement_python.hpp
 ${yayiStructuringElementSubdirectory}/structuringelement_python.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_declares.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_neighborhoods.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_predefined.cpp

)

include_directories(${yayiStructuringElementSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiStructuringElementPython "${yayiStructuringElementPythonSRC}" "YayiStructuringElement")
add_test(NAME YayiStructuringElementsTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${yayiStructuringElementSubdirectory}/structuringelements_python.py $<TARGET_FILE_DIR:YayiStructuringElementPython>)
