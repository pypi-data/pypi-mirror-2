#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiPixelProcessing)

# main library
set(YayiPixelProcessingSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiPixelProcessingSRC
  ${YayiPixelProcessingSubdirectory}/yayiPixelProcessing.hpp

  # utilities
  ${YayiPixelProcessingSubdirectory}/image_constant.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_constant_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_constant.cpp
  
  # copy
  ${YayiPixelProcessingSubdirectory}/image_copy.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_copy_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_copy.cpp
  ${YayiPixelProcessingSubdirectory}/src/image_copy_windowed.cpp
  
  # channels
  ${YayiPixelProcessingSubdirectory}/image_channels_process.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_channels_process_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_channels_process.cpp
  
  # color
  ${YayiPixelProcessingSubdirectory}/image_color_process.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_color_process_hls_T.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_color_process_luma_t.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_color_process_yuv_t.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_color_process_xyz_t.hpp
  #${YayiPixelProcessingSubdirectory}/include/image_color_process_cmyk_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_hls.cpp
  
  # compare
  ${YayiPixelProcessingSubdirectory}/image_compare.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_compare_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_compare.cpp

  # arithmetics
  ${YayiPixelProcessingSubdirectory}/image_arithmetics.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_arithmetics_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_arithmetics.cpp
  
  # logics
  ${YayiPixelProcessingSubdirectory}/image_logics.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_logics_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_logics.cpp
  
  # mathematical
  ${YayiPixelProcessingSubdirectory}/image_math.hpp 
  ${YayiPixelProcessingSubdirectory}/include/image_math_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_math.cpp
  
  #borders
  ${YayiPixelProcessingSubdirectory}/include/image_borders_t
)

include_directories(${YayiPixelProcessingSubdirectory})
include_directories(${YayiPixelProcessingSubdirectory}/include)

add_library(YayiPixelProcessing ${YayiPixelProcessingSRC})
target_link_libraries(YayiPixelProcessing YayiImageCore YayiCommon)
set_target_properties(YayiPixelProcessing PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_PIXELPROC_")
install(TARGETS YayiPixelProcessing CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiPixelProcessingSRC}")


# Test project
project(yayiPixelProcessingTests)
set(yayiPixelProcessingTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiPixelProcessingTestsSRC
  ${yayiPixelProcessingTestsSubdirectory}/simple_functions_through_interfaces.cpp
  ${yayiPixelProcessingTestsSubdirectory}/binary_operators_tests.cpp
  ${yayiPixelProcessingTestsSubdirectory}/border_tests.cpp
  ${yayiPixelProcessingTestsSubdirectory}/copy_test.cpp

  ${yayiPixelProcessingTestsSubdirectory}/main.cpp
  ${yayiPixelProcessingTestsSubdirectory}/main.hpp
)
include_directories(${yayiPixelProcessingTestsSubdirectory})
add_executable(YayiPixelProcessingTest ${yayiPixelProcessingTestsSRC})
target_link_libraries(YayiPixelProcessingTest YayiPixelProcessing ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiPixelProcessingTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiPixelProcessingTest)


# Python project
project(yayiPixelProcessingPython)
set(yayiPixelProcessingPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(yayiPixelProcessingPythonSRC
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.hpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.cpp
 
 ${yayiPixelProcessingPythonSubdirectory}/pixel_processing_channel_color.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_unary_pointwise.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_compare.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_arithmetic.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_logic.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_math.cpp
)

include_directories(${yayiPixelProcessingPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiPixelProcessingPython "${yayiPixelProcessingPythonSRC}" "YayiPixelProcessing")
add_test(NAME YayiPixelProcessingPython-1 COMMAND ${PYTHON_EXECUTABLE} ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.py $<TARGET_FILE_DIR:YayiPixelProcessingPython>)



#add_library(YayiPixelProcessingPython SHARED ${yayiPixelProcessingPythonSRC})
##link_directories(${PYTHON_LIBRARIES})
#target_link_libraries(YayiPixelProcessingPython YayiPixelProcessing YayiImageCore YayiCommon ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiPixelProcessingPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiPixelProcessingPython PROPERTIES PREFIX "")
