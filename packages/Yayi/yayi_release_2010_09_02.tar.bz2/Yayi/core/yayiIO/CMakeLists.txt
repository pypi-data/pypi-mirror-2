#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiIO)

if(ENABLE_NUMPY)
  add_definitions(-DYAYI_IO_NUMPY_ENABLED__)
  include_directories(${NUMPY_INCLUDE_PATH})
endif()
if(ENABLE_HDF5)
  add_definitions(-DYAYI_IO_HDF5_ENABLED__)
  include_directories(${HDF5_INCLUDE_DIRS})
endif()

set(YayiIOSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiIOSRC
  ${YayiIOSubdirectory}/include/yayi_IO.hpp

  ${YayiIOSubdirectory}/src/IO_raw.cpp
  ${YayiIOSubdirectory}/src/IO_jpg.cpp
  ${YayiIOSubdirectory}/src/IO_png.cpp
)

if(ENABLE_HDF5)
  set(YayiIOSRC ${YayiIOSRC} ${YayiIOSubdirectory}/src/IO_HDF5.cpp)
endif()


include_directories(${YayiIOSubdirectory})
include_directories(${YayiIOSubdirectory}/include)
include_directories(${YayiIOSubdirectory}/src)
if(ENABLE_HDF5)
  include_directories(${HDF5_INCLUDE_DIRS})
endif()

add_library(YayiIO ${YayiIOSRC})
target_link_libraries(YayiIO YayiImageCore YayiCommon ${JPEG} ${PNG})
if(ENABLE_HDF5)
  message("Linking to HDF5 ---- " ${HDF5LIBL} ${HDF5LIBB})
  target_link_libraries(YayiIO ${HDF5LIBL} ${HDF5LIBB})
endif()
set_target_properties(YayiIO PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_IO_")
install(TARGETS YayiIO CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiIOSRC}")


project(yayiIOTests)
set(yayiIOTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiIOTestsSRC
  ${yayiIOTestsSubdirectory}/io_raw_tests.cpp
  ${yayiIOTestsSubdirectory}/io_jpeg_tests.cpp
  ${yayiIOTestsSubdirectory}/io_png_tests.cpp

  ${yayiIOTestsSubdirectory}/main.cpp
  ${yayiIOTestsSubdirectory}/main.hpp
)
if(ENABLE_HDF5)
  set(yayiIOTestsSRC ${yayiIOTestsSRC} ${yayiIOTestsSubdirectory}/io_hdf5_tests.cpp)
endif()

add_executable(YayiIOTest ${yayiIOTestsSRC})
target_link_libraries(YayiIOTest YayiIO YayiImageCore YayiCommon ${Boost_SYSTEM_LIBRARY} ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiIOTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiIOTest)





project(yayiIOPython)
set(YayiIOPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiIOPythonSRC
 ${YayiIOPythonSubdirectory}/io_python.hpp
 ${YayiIOPythonSubdirectory}/io_python.cpp
 
 ${YayiIOPythonSubdirectory}/io_python_jpg.cpp
 ${YayiIOPythonSubdirectory}/io_python_png.cpp
 ${YayiIOPythonSubdirectory}/io_python_raw.cpp
)
if(ENABLE_HDF5)
  set(YayiIOPythonSRC ${YayiIOPythonSRC} ${YayiIOPythonSubdirectory}/io_python_hdf5.cpp)
endif()

if(ENABLE_NUMPY)
  set(YayiIOPythonSRC ${YayiIOPythonSRC} ${YayiIOPythonSubdirectory}/io_python_numpy.cpp)
endif()


include_directories(${YayiIOPythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiIOPython "${YayiIOPythonSRC}" "YayiIO")

if(ENABLE_HDF5)
  set(ADD_HDF5 "HDF5")
else()
  set(ADD_HDF5 "")
endif()

if(ENABLE_NUMPY)
  set(ADD_NUMPY "NUMPY")
else()
  set(ADD_NUMPY "")
endif()

add_test(NAME yayiIOTestPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiIOPythonSubdirectory}/io_python.py $<TARGET_FILE_DIR:YayiIOPython> ${ADD_HDF5} ${ADD_NUMPY})


#add_library(YayiIOPython SHARED ${YayiIOPythonSRC})
##link_directories(${PYTHON_LIBRARIES})
#target_link_libraries(YayiIOPython YayiIO YayiImageCore YayiCommon ${PYTHON_LIBRARIES})
#set_target_properties(YayiIOPython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiIOPython PROPERTIES PREFIX "")

