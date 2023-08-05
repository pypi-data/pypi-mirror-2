#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#



project(yayiCommon)

set(YayiCommonSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiCommonSRC
  ${YayiCommonSubdirectory}/yayiCommon.hpp

  ${YayiCommonSubdirectory}/common_config.hpp
  ${YayiCommonSubdirectory}/common_coordinates.hpp
  ${YayiCommonSubdirectory}/common_coordinates_operations_t.hpp
  ${YayiCommonSubdirectory}/include/common_coordinates_mpl_utils_t.hpp
  ${YayiCommonSubdirectory}/common_hyperrectangle.hpp
  ${YayiCommonSubdirectory}/common_errors.hpp
  ${YayiCommonSubdirectory}/common_histogram.hpp
  ${YayiCommonSubdirectory}/common_pixels.hpp
  ${YayiCommonSubdirectory}/common_pixels_T.hpp
  ${YayiCommonSubdirectory}/common_types.hpp
  ${YayiCommonSubdirectory}/common_priority_queues.hpp
  ${YayiCommonSubdirectory}/common_variant.hpp
  ${YayiCommonSubdirectory}/common_constants.hpp
  ${YayiCommonSubdirectory}/common_labels.hpp
  ${YayiCommonSubdirectory}/common_colorspace.hpp
  ${YayiCommonSubdirectory}/common_orders.hpp
  
  ${YayiCommonSubdirectory}/include/common_dispatch.hpp
  ${YayiCommonSubdirectory}/include/common_graph.hpp
  ${YayiCommonSubdirectory}/include/common_graphDispatch.hpp
  ${YayiCommonSubdirectory}/include/common_object.hpp
  ${YayiCommonSubdirectory}/include/common_string_utilities.hpp
  ${YayiCommonSubdirectory}/include/common_types_T.hpp
  ${YayiCommonSubdirectory}/include/current_configuration.hpp
  ${YayiCommonSubdirectory}/include/common_variantDispatch.hpp
  ${YayiCommonSubdirectory}/include/common_time.hpp
  
  ${YayiCommonSubdirectory}/src/common_error.cpp
  ${YayiCommonSubdirectory}/src/common_types.cpp
  ${YayiCommonSubdirectory}/src/common_colorspace.cpp
  ${YayiCommonSubdirectory}/src/current_configuration.cpp
  ${YayiCommonSubdirectory}/src/current_configuration_svn.hpp

)


if(NOT (${YayiCoreSVN_WC_REVISION} STREQUAL "XXX"))

file(WRITE ${YayiCommonSubdirectory}/src/current_configuration_svn_generated.hpp 
"
#ifndef YAYI_CURRENT_CONFIGURATION_SVN_HPP__
#define YAYI_CURRENT_CONFIGURATION_SVN_HPP__

/*!@file 
 * Template used with the SVN (TortoiseSVN or CMake) version retrieval facility
 * Auto generated file : do not edit
 * @author Raffi Enficiaud
 */

namespace yayi
{
")

file(APPEND ${YayiCommonSubdirectory}/src/current_configuration_svn_generated.hpp "\tstd::string svn_revision_version  = \"${YayiCoreSVN_WC_REVISION}\";\n")
file(APPEND ${YayiCommonSubdirectory}/src/current_configuration_svn_generated.hpp "\tstd::string svn_revision_date     = \"${YayiCoreSVN_WC_LAST_CHANGED_DATE}\";\n")
file(APPEND ${YayiCommonSubdirectory}/src/current_configuration_svn_generated.hpp "}\n\n#endif\n")

endif()

include_directories(${YayiCommonSubdirectory})
include_directories(${YayiCommonSubdirectory}/include)
include_directories(${YayiCommonSubdirectory}/src)
add_library(YayiCommon ${YayiCommonSRC})
target_link_libraries(YayiCommon ${Boost_GRAPH_LIBRARY} ${Boost_DATE_TIME_LIBRARY} ${Boost_REGEX_LIBRARY})
set_target_properties(YayiCommon PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_COMMON_")
install(TARGETS YayiCommon CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiCommonSRC}")



# Test project
project(yayiCommonCoreTests)
set(YayiCommonTestSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(YayiCommonTestSRC

 ${YayiCommonTestSubdirectory}/build_date.cpp
 ${YayiCommonTestSubdirectory}/coordinates.cpp
 ${YayiCommonTestSubdirectory}/dispatch_tests.cpp
 ${YayiCommonTestSubdirectory}/main.cpp
 ${YayiCommonTestSubdirectory}/main.hpp
 ${YayiCommonTestSubdirectory}/types_and_variant_tests.cpp
 ${YayiCommonTestSubdirectory}/priority_queues.cpp
 ${YayiCommonTestSubdirectory}/graphs.cpp
)
add_executable(YayiCommonTest ${YayiCommonTestSRC})
target_link_libraries(YayiCommonTest YayiCommon ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiCommonTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiCommonTest)


# Python project
project(yayiCommonPython)
set(YayiCommonPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiCommonPythonSRC
 ${YayiCommonPythonSubdirectory}/common_python.hpp
 ${YayiCommonPythonSubdirectory}/common_python.cpp

 ${YayiCommonPythonSubdirectory}/common_utils.cpp
 ${YayiCommonPythonSubdirectory}/common_enums.cpp
 ${YayiCommonPythonSubdirectory}/common_variant.cpp
 ${YayiCommonPythonSubdirectory}/common_error.cpp
 ${YayiCommonPythonSubdirectory}/common_object.cpp
 ${YayiCommonPythonSubdirectory}/common_coordinate.cpp
 ${YayiCommonPythonSubdirectory}/common_returncode.cpp
 ${YayiCommonPythonSubdirectory}/common_graph.cpp
)

include_directories(${YayiCommonPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiCommonPython "${YayiCommonPythonSRC}" "YayiCommon")
add_test(NAME yayiCommonTestPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiCommonPythonSubdirectory}/common_test.py $<TARGET_FILE_DIR:YayiCommonPython>)


#add_library(YayiCommonPython SHARED ${YayiCommonPythonSRC})
##link_directories(${PYTHON_LIBRARIES})
#target_link_libraries(YayiCommonPython YayiCommon ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiCommonPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiCommonPython PROPERTIES PREFIX "")
