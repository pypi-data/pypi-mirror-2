#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiSegmentation)

set(YayiSegmentationSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiSegmentationSRC
  ${YayiSegmentationSubdirectory}/yayiSegmentation.hpp
  
  #${YayiSegmentationSubdirectory}/include/viscous_watershed_T.hpp
  #${YayiSegmentationSubdirectory}/src/viscous_watershed.cpp
  
  ${YayiSegmentationSubdirectory}/include/isotropic_watershed_t.hpp
  ${YayiSegmentationSubdirectory}/src/isotropic_watershed.cpp
)


include_directories(${YayiSegmentationSubdirectory})
include_directories(${YayiSegmentationSubdirectory}/include)
include_directories(${YayiSegmentationSubdirectory}/src)
add_library(YayiSegmentation ${YayiSegmentationSRC})
target_link_libraries(YayiSegmentation YayiCommon YayiImageCore)
set_target_properties(YayiSegmentation PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_SEGMENTATION_")
install(TARGETS YayiSegmentation CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiSegmentationSRC}")




project(yayiSegmentationTests)
set(yayiSegmentationTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiSegmentationTestsSRC
  ${yayiSegmentationTestsSubdirectory}/main.hpp
  ${yayiSegmentationTestsSubdirectory}/main.cpp
  
  ${yayiSegmentationTestsSubdirectory}/isotropic_watershed_test.cpp
)
add_executable(YayiSegmentationTests ${yayiSegmentationTestsSRC})
target_link_libraries(YayiSegmentationTests YayiSegmentation YayiStructuringElement ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(YayiSegmentationTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiSegmentationTests)




project(yayiSegmentationPython)
set(YayiSegmentationPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiSegmentationPythonSRC
  ${YayiSegmentationPythonSubdirectory}/segmentation_python.hpp
  ${YayiSegmentationPythonSubdirectory}/segmentation_python.cpp
  ${YayiSegmentationPythonSubdirectory}/watershed.cpp
)

include_directories(${YayiSegmentationPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiSegmentationPython "${YayiSegmentationPythonSRC}" "YayiSegmentation")
add_test(NAME YayiSegmentationTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiSegmentationPythonSubdirectory}/segmentation_python.py $<TARGET_FILE_DIR:YayiSegmentationPython>)


#add_library(YayiSegmentationPython SHARED ${YayiSegmentationPythonSRC})
#target_link_libraries(YayiSegmentationPython YayiSegmentation ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiSegmentationPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiSegmentationPython PROPERTIES PREFIX "")

