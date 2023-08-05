#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#

# The name of our project is "YAYI". CMakeLists files in this project can
# refer to the root source directory of the project as ${YAYI_SOURCE_DIR} and
# to the root binary directory of the project as ${YAYI_BINARY_DIR}.

# example of run on MAC OS X
# cmake -DENABLE_HDF5=True -DBOOST_INSTALLATION_DIR=~/ThirdParties/install__Darwin_i386/ -DHDF5_INSTALL_DIR=~/ThirdParties/install__Darwin_i386/ -DCMAKE_BUILD_TYPE=Release CMakeLists.txt

cmake_minimum_required (VERSION 2.8)
project (YAYI)


set(CMAKE_USE_RELATIVE_PATHS)
option (BUILD_SHARED_LIBS "Build Shared Libraries" ON)


set(ENABLE_HDF5  FALSE CACHE BOOL "Enable HDF5 support (you should have it already built)")
set(ENABLE_NUMPY FALSE CACHE BOOL "Enable NumPy support for YayiIOPython (should be installed in your python distribution")

set(YAYI_root_dir         ${YAYI_SOURCE_DIR}/..)
set(YAYI_output_dir_base  ${YAYI_root_dir}/../Tmp/                 CACHE PATH "Base of the output directory")

# General library settings
set(YAYI_CORE_DIR
    ${YAYI_root_dir}/core
    CACHE PATH
    "Root path of the Core of YAYI")

set(YAYI_CORE_TEST_DIR
    ${YAYI_root_dir}/coreTests
    CACHE PATH
    "Root path of the Core of YAYI's tests")

set(YAYI_PYTHONEXT_DIR
    ${YAYI_root_dir}/python
    CACHE PATH
    "Python extension root path of YAYI")

set(THIRD_ROOT_PATH
    ${YAYI_root_dir}/plugins/external_libraries
    CACHE PATH
    "Root directory of the ThirdParties")

set(THIRD_PARTIES_PATH              
    ${THIRD_ROOT_PATH}/install__${CMAKE_HOST_SYSTEM_NAME}_${CMAKE_HOST_SYSTEM_PROCESSOR}/  
    CACHE PATH
    "Directory of the external third parties installation (built outside the project)")

enable_testing()


# Subversion
if(EXISTS ${YAYI_CORE_DIR}/.svn)
  find_package(Subversion)
  if(Subversion_FOUND)
    Subversion_WC_INFO(${YAYI_CORE_DIR} YayiCoreSVN)
  else()
    set(YayiCoreSVN_WC_REVISION "XXX" CACHE STRING "Yayi SVN version")
  endif(Subversion_FOUND)
else()
  set(YayiCoreSVN_WC_REVISION "XXX" CACHE STRING "Yayi SVN version")
endif()




set(CMAKE_RUNTIME_OUTPUT_DIRECTORY
    ${YAYI_output_dir_base}/${PROJECT_NAME}_SVN${YayiCoreSVN_WC_REVISION}
    CACHE PATH
    "Directory of the ouput binaries")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY
    ${YAYI_output_dir_base}/${PROJECT_NAME}_SVN${YayiCoreSVN_WC_REVISION}
    CACHE PATH
    "Directory of the ouput shared libraries")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY
    ${YAYI_output_dir_base}/${PROJECT_NAME}_SVN${YayiCoreSVN_WC_REVISION}
    CACHE PATH
    "Directory of the ouput static libraries")
set(CMAKE_INSTALL_PREFIX
    ${YAYI_output_dir_base}/install/${PROJECT_NAME}_SVN${YayiCoreSVN_WC_REVISION}
    CACHE PATH
    "Directory of the installation")

set(TEMPORARY_DIRECTORY
    ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/temporary
    CACHE PATH
    "Directory for temporary files")


# Compiler specific configurations
include("CMakeCompilerSpecific.txt")





#set(CMAKE_SKIP_RPATH                FALSE)
#set(CMAKE_SKIP_BUILD_RPATH          FALSE)
#set(CMAKE_BUILD_WITH_INSTALL_RPATH  TRUE) 
#set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)






message("CMake running on OS ${CMAKE_HOST_SYSTEM_NAME} version ${CMAKE_HOST_SYSTEM_VERSION} on processor ${CMAKE_HOST_SYSTEM_PROCESSOR}")
message("Current revision is ${YayiCoreSVN_WC_REVISION}")
message("HDF5 support is ${ENABLE_HDF5}")
message("NumPy support is ${ENABLE_NUMPY}")

if(BUILD_SHARED_LIBS)
  message("Building shared libraries")
  add_definitions(-DYAYI_DYNAMIC)
else()
  message("Building static libraries")  
endif()





macro(add_python_library name sources dependencies)
  if((${PYTHON_VERSION} VERSION_GREATER "2.6") OR (${PYTHON_VERSION} VERSION_EQUAL "2.6" ))
    if(UNIX)
      set(YAYI_PYTHON_MODULES_EXTENSIONS_TEMP ".so")
    else()
      set(YAYI_PYTHON_MODULES_EXTENSIONS_TEMP ".pyd")
    endif()
  else()
    if(APPLE)
      set(YAYI_PYTHON_MODULES_EXTENSIONS_TEMP ".so")
    else()
      set(YAYI_PYTHON_MODULES_EXTENSIONS_TEMP ${CMAKE_SHARED_LIBRARY_SUFFIX})
    endif()
  endif()
  set(YAYI_PYTHON_MODULES_EXTENSIONS ${YAYI_PYTHON_MODULES_EXTENSIONS_TEMP} CACHE STRING "Python modules extension")

  add_library(${name} SHARED ${sources})
  if(UNIX)
    message("Adding ${name} unix specific")
    target_link_libraries(${name} "${dependencies}" ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
  else(UNIX)
    # stupid morron autolink on windows
    message("Adding ${name} windows specific")
    target_link_libraries(${name} "${dependencies}" ${PYTHON_LIBRARIES})
  endif(UNIX)
  
  set_target_properties(${name} PROPERTIES SUFFIX ${YAYI_PYTHON_MODULES_EXTENSIONS}) 
  set_target_properties(${name} PROPERTIES PREFIX "")
  set_target_properties(${name} PROPERTIES COMPILE_DEFINITIONS "BOOST_PYTHON_DYNAMIC_LIB ${COMPILE_DEFINITIONS}")

  # uniform installation  
  if(UNIX)
    install(TARGETS ${name} CONFIGURATIONS Release LIBRARY DESTINATION python COMPONENT python)
  else(UNIX)
    install(TARGETS ${name} CONFIGURATIONS Release RUNTIME DESTINATION python COMPONENT python)
  endif(UNIX)
endmacro(add_python_library)



function(install_header_files file_names)
 #message("filesnames are ${file_names}")
 get_filename_component(yayiabs ${YAYI_root_dir} ABSOLUTE)
 #message("Yayi abs is ${yayiabs}")
 foreach(loop_var ${file_names})
  get_filename_component(filepathabs ${loop_var} ABSOLUTE)
  get_filename_component(filepath ${filepathabs} PATH)
  file(RELATIVE_PATH relative_p "${yayiabs}" "${filepath}")
  
  get_filename_component(extensiont ${loop_var} EXT)
  string(TOLOWER "${extensiont}" extension)
  
  #message("File is ${loop_var} / path is ${filepathabs} / relative is ${relative_p}")
  #get_source_file_property(is_header ${loop_var} LANGUAGE)
  #message("File is ${loop_var} / relative path is ${relative_p} / is header ? ${extension}")
  if("${extension}" STREQUAL ".hpp" OR "${extension}" STREQUAL ".h")
    #message("Installing ${loop_var} to include/Yayi/${relative_p}")
    install(FILES ${loop_var} DESTINATION include/Yayi/${relative_p} COMPONENT headers)
  endif()
 endforeach()
endfunction(install_header_files)

function(install_lib_and_dll file_names path_to_install component)
 foreach(loop_var ${file_names})
  get_filename_component(filepathabs ${loop_var} ABSOLUTE)
  get_filename_component(filepath ${filepathabs} PATH)
  get_filename_component(filename ${filepathabs} NAME_WE)
  set(file_to_install ${filepath}/${filename}${CMAKE_SHARED_LIBRARY_SUFFIX})
  if(NOT EXISTS ${file_to_install})
   message("file ${file_to_install} does not EXISTS !!!")
  endif()
  message("Installing ${file_to_install} to ${path_to_install}")
  install(FILES ${file_to_install} DESTINATION ${path_to_install} COMPONENT ${component})  
 endforeach()
endfunction(install_lib_and_dll)

function(install_realpath_with_rename file_names path_to_install component configuration)
 foreach(loop_var ${file_names})
  get_filename_component(filepathreal ${loop_var} REALPATH)
  get_filename_component(filename ${loop_var} NAME)
  
  if(NOT EXISTS ${filepathreal})
   message("file ${filepathreal} does not EXISTS !!!")
  endif()
  message("Installing ${loop_var} (${filepathreal}) to ${path_to_install} with name ${filename}")
  install(FILES ${loop_var} CONFIGURATIONS ${configuration} DESTINATION ${path_to_install} COMPONENT ${component} RENAME ${filename})  
 endforeach()
endfunction(install_realpath_with_rename)


# Third parties
add_subdirectory (${THIRD_ROOT_PATH} ${TEMPORARY_DIRECTORY}/thirdParties)
#add_definitions(-DBOOST_TEST_DYN_LINK) # surtout pas !!!

# general includes
# include_directories(${YAYI_root_dir}) # this one is useless

# warning the order is important
include_directories(${YAYI_SOURCE_DIR}/../..)
include_directories(${JPEG_LIB_SRC})
include_directories(${PNG_LIB_SRC})
include_directories(${ZLIB_SRC_DIR})
include_directories(${THIRD_ROOT_PATH}/boost-1_38_fix/)     # this is for boost/utility/addressof.hpp which should be soon fixed in a newer releases of boost
include_directories(${Boost_INCLUDE_DIRS})
include_directories(${THIRD_ROOT_PATH}/Config/)
include_directories(${THIRD_PARTIES_PATH}/include)          # this one comes last
link_directories (${Boost_LIBRARY_DIRS})
#set(CMAKE_INSTALL_RPATH ${Boost_LIBRARY_DIRS})


# the yayi core libraries
add_subdirectory (${YAYI_CORE_DIR}/yayiCommon                 ${TEMPORARY_DIRECTORY}/yayiCommon)
add_subdirectory (${YAYI_CORE_DIR}/yayiImageCore              ${TEMPORARY_DIRECTORY}/yayiImageCore)
add_subdirectory (${YAYI_CORE_DIR}/yayiIO                     ${TEMPORARY_DIRECTORY}/yayiIO)
add_subdirectory (${YAYI_CORE_DIR}/yayiStructuringElement     ${TEMPORARY_DIRECTORY}/yayiStructuringElement)
add_subdirectory (${YAYI_CORE_DIR}/yayiPixelProcessing        ${TEMPORARY_DIRECTORY}/yayiPixelProcessing)
add_subdirectory (${YAYI_CORE_DIR}/yayiLowLevelMorphology     ${TEMPORARY_DIRECTORY}/yayiLowLevelMorphology)
add_subdirectory (${YAYI_CORE_DIR}/yayiNeighborhoodProcessing ${TEMPORARY_DIRECTORY}/yayiNeighborhoodProcessing)
add_subdirectory (${YAYI_CORE_DIR}/yayiDistances              ${TEMPORARY_DIRECTORY}/yayiDistances)
add_subdirectory (${YAYI_CORE_DIR}/yayiSegmentation           ${TEMPORARY_DIRECTORY}/yayiSegmentation)
add_subdirectory (${YAYI_CORE_DIR}/yayiLabel                  ${TEMPORARY_DIRECTORY}/yayiLabel)
add_subdirectory (${YAYI_CORE_DIR}/yayiMeasurements           ${TEMPORARY_DIRECTORY}/yayiMeasurements)
add_subdirectory (${YAYI_CORE_DIR}/yayiReconstruction         ${TEMPORARY_DIRECTORY}/yayiReconstruction)


## 
##
## Installation 
##
set(CPACK_PACKAGE_NAME                  "Yayi")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY   "Yayi: a generic mathematical morphology research and development framework")
set(CPACK_PACKAGE_VENDOR                "Raffi Enficiaud")
set(CPACK_PACKAGE_DESCRIPTION_FILE      "${CMAKE_CURRENT_SOURCE_DIR}/../LICENSE_1_0.txt")
set(CPACK_RESOURCE_FILE_LICENSE         "${CMAKE_CURRENT_SOURCE_DIR}/../LICENSE_1_0.txt")
set(CPACK_PACKAGE_VERSION               "0.0.7")
set(CPACK_PACKAGE_VERSION_MAJOR         "0")
set(CPACK_PACKAGE_VERSION_MINOR         "0")
set(CPACK_PACKAGE_VERSION_PATCH         "7")
set(CPACK_PACKAGE_INSTALL_DIRECTORY     "Yayi ${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}${CPACK_PACKAGE_VERSION_PATCH}")
set(CPACK_PACKAGE_CONTACT               "raffi.enficiaud@free.fr")

set(CPACK_COMPONENTS_ALL libraries headers python)
set(CPACK_COMPONENT_APPLICATIONS_DISPLAY_NAME   "Applications")
set(CPACK_COMPONENT_PYTHON_DISPLAY_NAME         "Python exports")
set(CPACK_COMPONENT_LIBRARIES_DISPLAY_NAME      "Libraries")
set(CPACK_COMPONENT_HEADERS_DISPLAY_NAME        "C++ Headers")

set(CPACK_COMPONENT_APPLICATIONS_DESCRIPTION    "An extremely useful application that makes use of Yayi")
set(CPACK_COMPONENT_LIBRARIES_DESCRIPTION       "Static / dynamic libraries used to build programs with Yayi")
set(CPACK_COMPONENT_HEADERS_DESCRIPTION         "C/C++ header files of Yayi")
set(CPACK_COMPONENT_PYTHON_DESCRIPTION          "Python shared libraries wrapping the functionalities of Yayi")

set(CPACK_COMPONENT_HEADERS_DEPENDS             libraries)
set(CPACK_COMPONENT_PYTHON_DEPENDS              libraries)
set(CPACK_COMPONENT_APPLICATIONS_DEPENDS        libraries)

set(CPACK_COMPONENT_LIBRARIES_GROUP                 "Development")
set(CPACK_COMPONENT_HEADERS_GROUP                   "Development")
set(CPACK_COMPONENT_GROUP_DEVELOPMENT_DESCRIPTION   "All the tools/files you need for developing C/C++ programs with Yayi")

set(CPACK_ALL_INSTALL_TYPES Full Developer Python)
set(CPACK_COMPONENT_LIBRARIES_INSTALL_TYPES         Python Developer Full)
set(CPACK_COMPONENT_HEADERS_INSTALL_TYPES           Developer Full)
set(CPACK_COMPONENT_PYTHON_INSTALL_TYPES            Python Full)


if(WIN32 AND NOT UNIX)
  # There is a bug in NSI that does not handle full unix paths properly. Make
  # sure there is at least one set of four (4) backlasshes.
  #set(CPACK_PACKAGE_ICON                "")
  #set(CPACK_NSIS_INSTALLED_ICON_NAME    "")
  set(CPACK_NSIS_DISPLAY_NAME           "${CPACK_PACKAGE_INSTALL_DIRECTORY}")
  set(CPACK_NSIS_HELP_LINK              "http:////raffi.enficiaud.free.fr")
  set(CPACK_NSIS_URL_INFO_ABOUT         "http:////raffi.enficiaud.free.fr")
  set(CPACK_NSIS_CONTACT                "raffi.enficiaud@free.fr")
  set(CPACK_NSIS_MODIFY_PATH            ON)
else()
  set(CPACK_STRIP_FILES                 "")
  set(CPACK_SOURCE_STRIP_FILES          "")
  
  #CPACK_DEBIAN_PACKAGE_VERSION
  #CPACK_DEBIAN_PACKAGE_ARCHITECTURE
  
  
endif()

if(UNIX)
  set(CPACK_GENERATOR DEB)
endif()
include(CPack)


