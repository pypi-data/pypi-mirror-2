#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#




project(yayiImageCore)

set(YayiImageCoreSubdirectory ${YAYI_CORE_DIR}/${PROJECT_NAME})

set(YayiImageCoreSRC
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_T.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_zeroary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_unary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_binary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_ternary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_fourary_t.hpp
  
  ${YayiImageCoreSubdirectory}/include/yayiImageAllocators_T.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageIterator.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageUtilities_T.hpp

  ${YayiImageCoreSubdirectory}/include/yayiImageCore.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageCore_Impl.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageCore_ImplDispatch.hpp
  ${YayiImageCoreSubdirectory}/src/yayiImageCore.cpp
  
  ${YayiImageCoreSubdirectory}/yayiImageCoreFunctions.hpp
  ${YayiImageCoreSubdirectory}/src/yayiGetSame.cpp
)


include_directories(${YayiImageCoreSubdirectory})
include_directories(${YayiImageCoreSubdirectory}/include)
include_directories(${YayiImageCoreSubdirectory}/src)
add_library(YayiImageCore ${YayiImageCoreSRC})
target_link_libraries(YayiImageCore YayiCommon)
set_target_properties(YayiImageCore PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_CORE_")
install(TARGETS YayiImageCore CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install_header_files("${YayiImageCoreSRC}")


project(yayiImageCoreTests)
set(yayiImageCoreTestsSubdirectory ${YAYI_CORE_TEST_DIR}/${PROJECT_NAME})
set(yayiImageCoreTestsSRC
  ${yayiImageCoreTestsSubdirectory}/image_access.cpp
  ${yayiImageCoreTestsSubdirectory}/image_creation.cpp
  ${yayiImageCoreTestsSubdirectory}/image_utilities.cpp
  ${yayiImageCoreTestsSubdirectory}/image_apply_tests.cpp
  ${yayiImageCoreTestsSubdirectory}/image_iterators.cpp
  ${yayiImageCoreTestsSubdirectory}/main.cpp
  ${yayiImageCoreTestsSubdirectory}/main.hpp
)
add_executable(YayiImageCoreTest ${yayiImageCoreTestsSRC})
target_link_libraries(YayiImageCoreTest YayiImageCore ${Boost_TEST_EXEC_MONITOR_LIBRARY})
add_test(yayiImageCoreTest-1 ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/YayiImageCoreTest)





project(yayiImageCorePython)
set(YayiImageCorePythonSubdirectory ${YAYI_PYTHONEXT_DIR}/${PROJECT_NAME})
set(YayiImageCorePythonSRC
 ${YayiImageCorePythonSubdirectory}/imagecore_python.hpp
 ${YayiImageCorePythonSubdirectory}/imagecore_python.cpp

 ${YayiImageCorePythonSubdirectory}/imagecore_image.cpp
 ${YayiImageCorePythonSubdirectory}/imagecore_iterator.cpp
 ${YayiImageCorePythonSubdirectory}/imagecore_interfacepixel.cpp
)

include_directories(${YayiImageCorePythonSubdirectory}/include)
include_directories(${PYTHON_INCLUDE_PATH})
add_python_library(YayiImageCorePython "${YayiImageCorePythonSRC}" "YayiImageCore")
add_test(NAME yayiImageCoreTestPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiImageCorePythonSubdirectory}/imagecore_python.py $<TARGET_FILE_DIR:YayiImageCorePython>)


#add_library(YayiImageCorePython SHARED ${YayiImageCorePythonSRC})
##link_directories(${PYTHON_LIBRARIES})
#target_link_libraries(YayiImageCorePython YayiCommon YayiImageCore ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
#set_target_properties(YayiImageCorePython PROPERTIES SUFFIX ".so")
#set_target_properties(YayiImageCorePython PROPERTIES PREFIX "")

