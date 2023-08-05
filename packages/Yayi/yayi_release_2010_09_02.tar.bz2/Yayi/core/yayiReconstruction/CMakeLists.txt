#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiReconstruction)

# main library
set(YayiReconstructionSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiReconstructionSRC
  ${YayiReconstructionSubdirectory}/yayiReconstruction.hpp
  
  ${YayiReconstructionSubdirectory}/morphological_reconstruction.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_reconstruction_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_reconstruction.cpp
  
  ${YayiReconstructionSubdirectory}/morphological_fill_holes.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_fill_holes_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_fill_holes.cpp
  
  ${YayiReconstructionSubdirectory}/morphological_leveling.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_leveling_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_leveling.cpp
)


include_directories(${YayiReconstructionSubdirectory})
include_directories(${YayiReconstructionSubdirectory}/include)

add_library(YayiReconstruction ${YayiReconstructionSRC})
target_link_libraries(YayiReconstruction YayiImageCore YayiCommon)
set_target_properties(YayiReconstruction PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_REC_")
install(TARGETS YayiReconstruction CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiReconstructionSRC}")


# Test project
project(yayiReconstructionTests)
set(yayiReconstructionTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiReconstructionTestsSRC
  ${yayiReconstructionTestsSubdirectory}/main.cpp
  ${yayiReconstructionTestsSubdirectory}/main.hpp
  
  ${yayiReconstructionTestsSubdirectory}/reconstruction_test.cpp
  ${yayiReconstructionTestsSubdirectory}/fill_hole_test.cpp
  ${yayiReconstructionTestsSubdirectory}/leveling_test.cpp
)
include_directories(${yayiReconstructionTestsSubdirectory})
add_executable(YayiReconstructionTest ${yayiReconstructionTestsSRC})
target_link_libraries(YayiReconstructionTest YayiReconstruction YayiStructuringElement ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiReconstructionTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiReconstructionTest)


# Python project
project(yayiReconstructionPython)
set(yayiReconstructionPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(yayiReconstructionPythonSRC
 ${yayiReconstructionPythonSubdirectory}/reconstruction_python.hpp
 ${yayiReconstructionPythonSubdirectory}/reconstruction_python.cpp
 
 ${yayiReconstructionPythonSubdirectory}/morphological_reconstructions.cpp
 ${yayiReconstructionPythonSubdirectory}/fill_holes.cpp

)

include_directories(${yayiReconstructionPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiReconstructionPython "${yayiReconstructionPythonSRC}" "YayiReconstruction")
add_test(NAME YayiReconstructionPython-1 COMMAND ${PYTHON_EXECUTABLE} ${yayiReconstructionPythonSubdirectory}/reconstruction_python.py $<TARGET_FILE_DIR:YayiReconstructionPython>)

