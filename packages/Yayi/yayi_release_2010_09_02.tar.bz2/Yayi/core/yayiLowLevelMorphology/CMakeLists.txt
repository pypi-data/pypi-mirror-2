#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#



project(yayiLowLevelMorphology)

set(YayiLLMSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})
set(YayiLLMMSRC
  ${YayiLLMSubdirectory}/yayiLowLevelMorphology.hpp

  ${YayiLLMSubdirectory}/include/lowlevel_neighborhoodProcessing_t.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_neighbor_operators_t.hpp
  ${YayiLLMSubdirectory}/include/neighbor_operators_traits_t.hpp
    
  ${YayiLLMSubdirectory}/lowlevel_erosion_dilation.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_erosion_dilation_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_erosion_dilation.cpp
  
  ${YayiLLMSubdirectory}/lowlevel_morpho_gradient.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_morpho_gradient_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_gradient.cpp
  
  ${YayiLLMSubdirectory}/lowlevel_opening_closing.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_opening_closing_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_opening_closing.cpp
  
  ${YayiLLMSubdirectory}/lowlevel_geodesic.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_geodesic_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_geodesic.cpp
  
  ${YayiLLMSubdirectory}/include/lowlevel_hit_or_miss_t.hpp
  ${YayiLLMSubdirectory}/lowlevel_hit_or_miss.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_hit_or_miss.cpp
)

include_directories(${YayiLLMSubdirectory})
include_directories(${YayiLLMSubdirectory}/include)
add_library(YayiLowlevelMorphology ${YayiLLMMSRC})
target_link_libraries(YayiLowlevelMorphology YayiIO YayiStructuringElement YayiPixelProcessing YayiImageCore YayiCommon)
set_target_properties(YayiLowlevelMorphology PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_LLMM_")
install(TARGETS YayiLowlevelMorphology CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiLLMMSRC}")


# Test project
project(yayiLowlevelMorphologyTests)
set(yayiLowLevelMorphologyTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiLowLevelMorphologyTestsSRC
  ${yayiLowLevelMorphologyTestsSubdirectory}/simple_operators_interface_tests.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/erosion_dilation_test.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/hit_or_miss_test.cpp
  
  ${yayiLowLevelMorphologyTestsSubdirectory}/main.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/main.hpp
)
add_executable(YayiLowLevelMorphologyTest ${yayiLowLevelMorphologyTestsSRC})
target_link_libraries(YayiLowLevelMorphologyTest YayiLowlevelMorphology YayiIO YayiStructuringElement YayiPixelProcessing YayiImageCore YayiCommon ${Boost_TEST_EXEC_MONITOR_LIBRARY} ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY})
add_test(YayiLowLevelMorphologyTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiLowLevelMorphologyTest)




# Python project
project(yayiLowLevelMorphologyPython)
set(yayiLowLevelMorphologyPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(yayiLowLevelMorphologyPythonPythonSRC
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_python.hpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_python.cpp
  
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_rank.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_gradient.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_geodesic.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_hit_or_miss.cpp
)

include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiLowLevelMorphologyPython "${yayiLowLevelMorphologyPythonPythonSRC}" "YayiLowlevelMorphology")
# todo add test

#add_library(YayiLowLevelMorphologyPython SHARED ${yayiLowLevelMorphologyPythonPythonSRC})
#target_link_libraries(YayiLowLevelMorphologyPython YayiLowlevelMorphology ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiLowLevelMorphologyPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiLowLevelMorphologyPython PROPERTIES PREFIX "")
