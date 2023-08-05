#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiDistances)

set(YayiDistancesSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiDistancesSRC
  ${YayiDistancesSubdirectory}/yayiDistances.hpp
  ${YayiDistancesSubdirectory}/quasi_distance.hpp
  
  ${YayiDistancesSubdirectory}/include/quasi_distance_T.hpp
  ${YayiDistancesSubdirectory}/src/quasi_distance.cpp
  
  #${YayiDistancesSubdirectory}/include/exact_distances_t.hpp
  #${YayiDistancesSubdirectory}/include/distance_operations_t.hpp


  ${YayiDistancesSubdirectory}/include/morphological_distance_t.hpp
  ${YayiDistancesSubdirectory}/morphological_distance.hpp
  ${YayiDistancesSubdirectory}/src/morphological_distance.cpp
  
)


include_directories(${YayiDistancesSubdirectory})
include_directories(${YayiDistancesSubdirectory}/include)
include_directories(${YayiDistancesSubdirectory}/src)
add_library(YayiDistances ${YayiDistancesSRC})
target_link_libraries(YayiDistances YayiCommon YayiIO)
set_target_properties(YayiDistances PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_DISTANCES_")
install(TARGETS YayiDistances CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiDistancesSRC}")


project(yayiDistancesTests)
set(yayiDistancesTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiDistancesTestsSRC
  ${yayiDistancesTestsSubdirectory}/main.hpp
  ${yayiDistancesTestsSubdirectory}/main.cpp
  
  ${yayiDistancesTestsSubdirectory}/quasi_distance_test.cpp
  ${yayiDistancesTestsSubdirectory}/morpho_distance_tests.cpp
  ${yayiDistancesTestsSubdirectory}/exact_distance_tests.cpp
)

if(${CMAKE_HOST_UNIX})
  # to copy from boost directory at "libs/random/random_device.cpp"
  if(EXISTS ${yayiDistancesTestsSubdirectory}/random_device.cpp) 
    add_definitions(-DYAYI_REAL_RANDOM_EXISTS__)
    set(yayiDistancesTestsSRC ${yayiDistancesTestsSRC} ${yayiDistancesTestsSubdirectory}/random_device.cpp)
  endif()
endif(${CMAKE_HOST_UNIX})


add_executable(YayiDistancesTest ${yayiDistancesTestsSRC})
target_link_libraries(YayiDistancesTest YayiDistances YayiStructuringElement YayiIO ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(YayiDistancesTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiDistancesTest)



project(yayiDistancesPython)
set(YayiDistancesPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiDistancesPythonSRC
  ${YayiDistancesPythonSubdirectory}/distances_python.hpp
  ${YayiDistancesPythonSubdirectory}/distances_python.cpp
  
  ${YayiDistancesPythonSubdirectory}/quasi_distance.cpp
  ${YayiDistancesPythonSubdirectory}/binary_distance.cpp
)


include_directories(${YayiDistancesPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiDistancesPython "${YayiDistancesPythonSRC}" "YayiDistances")
add_test(NAME YayiDistancesTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiDistancesPythonSubdirectory}/distances_python.py $<TARGET_FILE_DIR:YayiDistancesPython>)

#add_library(YayiDistancesPython SHARED ${YayiDistancesPythonSRC})
#target_link_libraries(YayiDistancesPython YayiCommon YayiImageCore YayiDistances ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiDistancesPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiDistancesPython PROPERTIES PREFIX "")

