#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#

project(yayiMeasurements)

set(YayiMeasurementsSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiMeasurementsSRC
  ${YayiMeasurementsSubdirectory}/yayiMeasurements.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_t.hpp
  
  ${YayiMeasurementsSubdirectory}/measurements_min_max.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_min_max_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_min_max.cpp
  
  ${YayiMeasurementsSubdirectory}/measurements_histogram.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_histogram_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_histogram.cpp
  
  ${YayiMeasurementsSubdirectory}/measurements_mean_variance.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_mean_variance_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_mean_variance.cpp
  
  ${YayiMeasurementsSubdirectory}/measurements_quantiles.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_quantiles_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_quantiles.cpp
)


include_directories(${YayiMeasurementsSubdirectory})
include_directories(${YayiMeasurementsSubdirectory}/include)
include_directories(${YayiMeasurementsSubdirectory}/src)
add_library(YayiMeasurements ${YayiMeasurementsSRC})
target_link_libraries(YayiMeasurements YayiImageCore YayiCommon)
set_target_properties(YayiMeasurements PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_MEASUREMENTS_")
install(TARGETS YayiMeasurements CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiMeasurementsSRC}")


project(yayiMeasurementsTests)
set(yayiMeasurementsTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiMeasurementsTestsSRC
  ${yayiMeasurementsTestsSubdirectory}/main.hpp
  ${yayiMeasurementsTestsSubdirectory}/main.cpp
  
  ${yayiMeasurementsTestsSubdirectory}/min_max_test.cpp
)
add_executable(YayiMeasurementsTests ${yayiMeasurementsTestsSRC})
target_link_libraries(YayiMeasurementsTests YayiCommon YayiImageCore ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiMeasurementsTests-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiMeasurementsTests)





project(yayiMeasurementsPython)
set(YayiMeasurementsPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiMeasurementsPythonSRC
  ${YayiMeasurementsPythonSubdirectory}/measurements_python.hpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_python.cpp
  
  ${YayiMeasurementsPythonSubdirectory}/measurements_min_max.cpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_histograms.cpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_statistics.cpp
)

include_directories(${YayiMeasurementsPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiMeasurementsPython "${YayiMeasurementsPythonSRC}" "YayiMeasurements")
add_test(NAME yayiMeasurementsTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiMeasurementsPythonSubdirectory}/measurements_python.py $<TARGET_FILE_DIR:YayiMeasurementsPython>)
