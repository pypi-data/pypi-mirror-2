#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiLabel)

set(YayiLabelSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiLabelSRC
  ${YayiLabelSubdirectory}/yayi_Label.hpp
  
  ${YayiLabelSubdirectory}/include/yayi_label_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_simple.cpp
  
  ${YayiLabelSubdirectory}/yayi_label_extrema.hpp
  ${YayiLabelSubdirectory}/include/yayi_label_extrema_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_extrema.cpp
  
  ${YayiLabelSubdirectory}/yayi_label_binary_with_measure.hpp
  ${YayiLabelSubdirectory}/include/yayi_label_binary_with_measure_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_binary_with_measures.cpp
  
  ${YayiLabelSubdirectory}/include/yayi_label_with_adjacency_graph_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_with_adjacency_graph.cpp
)

include_directories(${YayiLabelSubdirectory})
include_directories(${YayiLabelSubdirectory}/include)
include_directories(${YayiLabelSubdirectory}/src)
add_library(YayiLabel ${YayiLabelSRC})
target_link_libraries(YayiLabel YayiImageCore YayiCommon)
set_target_properties(YayiLabel PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_LABEL_")
install(TARGETS YayiLabel CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiLabelSRC}")


project(yayiLabelTests)
set(yayiLabelTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiLabelTestsSRC
  ${yayiLabelTestsSubdirectory}/main.hpp
  ${yayiLabelTestsSubdirectory}/main.cpp
  ${yayiLabelTestsSubdirectory}/label_image_test.cpp
  ${yayiLabelTestsSubdirectory}/label_extrema_test.cpp
)
include_directories(${yayiLabelTestsSubdirectory})
add_executable(YayiLabelTest ${yayiLabelTestsSRC})
target_link_libraries(YayiLabelTest YayiLabel YayiStructuringElement ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiLabelTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiLabelTest)


project(yayiLabelPython)
set(YayiLabelPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiLabelPythonSRC
  ${YayiLabelPythonSubdirectory}/label_python.cpp
  ${YayiLabelPythonSubdirectory}/label_python.hpp
  
  ${YayiLabelPythonSubdirectory}/label_basic.cpp
  ${YayiLabelPythonSubdirectory}/label_extrema.cpp
)

include_directories(${YayiLabelPythonSubdirectory})
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiLabelPython "${YayiLabelPythonSRC}" "YayiLabel")
add_test(NAME yayiLabelPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiLabelPythonSubdirectory}/label_python.py $<TARGET_FILE_DIR:YayiLabelPython>)


#add_library(YayiLabelPython SHARED ${YayiLabelPythonSRC})
##link_directories(${PYTHON_LIBRARIES})
#target_link_libraries(YayiLabelPython YayiLabel ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiLabelPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiLabelPython PROPERTIES PREFIX "")

