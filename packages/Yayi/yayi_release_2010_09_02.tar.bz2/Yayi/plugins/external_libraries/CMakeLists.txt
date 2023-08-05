#
#  -:- LICENCE -:- 
# Copyright Raffi Enficiaud 2007-2010
# 
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# 
#  -:- LICENCE -:- 
#



# Third parties builds
#include(select_library_configurations)



# --------------------------------------------------------------------------------
# boost

set(BOOST_INSTALLATION_DIR  ${THIRD_PARTIES_PATH} CACHE PATH "Boost installation root path")

set(BOOST_ROOT              ${BOOST_INSTALLATION_DIR})


# Boost default
set(BOOST_VERSION_MAJOR 1                                                       CACHE STRING    "Boost major version")
set(BOOST_VERSION_MINOR 38                                                      CACHE STRING    "Boost minor version")
set(BOOST_VERSION_SUBMINOR 0                                                    CACHE STRING    "Boost sub minor version")
set(BOOST_VERSION               ${BOOST_VERSION_MAJOR}.${BOOST_VERSION_MINOR}.${BOOST_VERSION_SUBMINOR})
set(BOOST_LIBRARYDIR            ${BOOST_ROOT}/lib                               CACHE PATH      "Directory of the boost installation (libs)")
set(BOOST_INCLUDEDIR            ${BOOST_ROOT}/include/boost-${BOOST_VERSION_MAJOR}_${BOOST_VERSION_MINOR}    
                                                                                CACHE PATH      "Directory of the boost installation (inludes)")
set(Boost_ADDITIONAL_VERSIONS   "1.41" "1.41.0" "1.42" "1.42.0" "1.43" "1.43.0" "1.44" "1.44.0")
# use of the cmake special package

#set(Boost_USE_STATIC_LIBS   ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_DEBUG             TRUE)

find_package( Boost ${BOOST_VERSION} COMPONENTS date_time filesystem system thread regex unit_test_framework python graph) # COMPONENTS test filesystem system) # date_time
if(Boost_FOUND)
  set(BOOST_INCLUDEDIR ${Boost_INCLUDE_DIRS})
  set(Boost_INCLUDE_DIRS ${Boost_INCLUDE_DIRS} PARENT_SCOPE)
  set(Boost_LIBRARY_DIRS ${Boost_LIBRARY_DIRS} PARENT_SCOPE)
  message("Boost library found in " ${Boost_LIBRARY_DIRS})

else(Boost_FOUND)
  message(FATAL_ERROR "BOOST not found !!")
endif(Boost_FOUND)

set(BoostFilesToInstall 
  ${Boost_PYTHON_LIBRARY_RELEASE}
  ${Boost_SYSTEM_LIBRARY_RELEASE} 
  ${Boost_GRAPH_LIBRARY_RELEASE} 
  ${Boost_REGEX_LIBRARY_RELEASE} 
  ${Boost_DATE_TIME_LIBRARY_RELEASE} 
  ${Boost_FILESYSTEM_LIBRARY_RELEASE} 
  ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY_RELEASE} 
  )

if(WIN32)
  install(FILES 
    ${BoostFilesToInstall}
    CONFIGURATIONS Release
    #ARCHIVE DESTINATION lib
    #LIBRARY DESTINATION lib
    #RUNTIME DESTINATION lib
    DESTINATION lib
    COMPONENT libraries)
  install_lib_and_dll("${BoostFilesToInstall}" lib libraries) 
else()
  install_realpath_with_rename("${BoostFilesToInstall}" lib libraries Release)
endif()

set(Boost_USE_STATIC_LIBS   ON)

find_package( Boost ${BOOST_VERSION} COMPONENTS test_exec_monitor)
if(Boost_FOUND)
  message("Boost test_exec_monitor found in ${Boost_TEST_EXEC_MONITOR_LIBRARY}")
  # static linked to the exe files, no need to install it
  #install(FILES ${Boost_TEST_EXEC_MONITOR_LIBRARY_RELEASE} DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)
else(Boost_FOUND)
  message(FATAL_ERROR "BOOST test_exec_monitor not found !!")
endif(Boost_FOUND)


# Python libraries
find_package(PythonLibs REQUIRED)
if(PYTHONLIBS_FOUND)
  message("Python libraries found ! at ${PYTHON_LIBRARIES} and ${PYTHON_INCLUDE_PATH}")
  set(PYTHON_LIBRARIES ${PYTHON_LIBRARIES} PARENT_SCOPE)
  set(PYTHON_INCLUDE_PATH ${PYTHON_INCLUDE_PATH} PARENT_SCOPE)
endif()


find_package(PythonInterp REQUIRED)
if(PYTHONINTERP_FOUND)
  #used to switch python extension on windows dll -> pyd 
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -c "import sys; v=sys.version_info[:2]; print '%d.%d' % v"
    OUTPUT_VARIABLE PYTHON_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
  message (STATUS "Compiling for Python ${PYTHON_VERSION}")
  string  (REPLACE "." "" PYTHON_VERSION_NO_DOTS ${PYTHON_VERSION})
  set     (PYTHON_VERSION       ${PYTHON_VERSION}     PARENT_SCOPE)
  set     (PYTHON_EXECUTABLE    ${PYTHON_EXECUTABLE}  PARENT_SCOPE)
  
  if(ENABLE_NUMPY)
    execute_process(
      COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print numpy.get_include()"
      OUTPUT_VARIABLE NUMPY_INCLUDE_PATH
      ERROR_VARIABLE  NUMPY_ERROR
      OUTPUT_STRIP_TRAILING_WHITESPACE
      )
    if(NOT (NUMPY_ERROR STREQUAL "") OR (NUMPY_INCLUDE_PATH STREQUAL ""))
      message(FATAL_ERROR "NUMPY the following error occured: ${NUMPY_ERROR} - Consider setting PYTHON_ROOT in the environment")
    endif()
    message (STATUS "Getting headers for Numpy from ${NUMPY_INCLUDE_PATH}")
    set     (NUMPY_INCLUDE_PATH   ${NUMPY_INCLUDE_PATH}     PARENT_SCOPE)
  endif()
endif()


# Lib JPEG
project(jpeg-7)
#find_package(JPEG)
#if(JPEG_FOUND)
#  message("Jpeg location is ${JPEG_INCLUDE_DIR}")
#  set(JPEG_INCLUDEDIR       ${JPEG_INCLUDE_DIR} )
#  set(JPEG_LIB_DIR          ${JPEG_LIBRARIES}   )
#else(JPEG_FOUND)

  set(LIBJPEG jpeg-7)
  set(LIBJPEG_SOURCE_DIR ${LIBJPEG} CACHE PATH "Jpeg sources directory")

  set(LIBJPEG_SRC 

    # common
    ${LIBJPEG_SOURCE_DIR}/jcapimin.c  ${LIBJPEG_SOURCE_DIR}/jcapistd.c  ${LIBJPEG_SOURCE_DIR}/jdapimin.c  ${LIBJPEG_SOURCE_DIR}/jdapistd.c
    ${LIBJPEG_SOURCE_DIR}/jcomapi.c   ${LIBJPEG_SOURCE_DIR}/jcparam.c   ${LIBJPEG_SOURCE_DIR}/jctrans.c   ${LIBJPEG_SOURCE_DIR}/jdtrans.c
    ${LIBJPEG_SOURCE_DIR}/jaricom.c   ${LIBJPEG_SOURCE_DIR}/jerror.c    ${LIBJPEG_SOURCE_DIR}/jmemmgr.c   ${LIBJPEG_SOURCE_DIR}/jutils.c
    ${LIBJPEG_SOURCE_DIR}/jmemnobs.c
    
    # compression
    ${LIBJPEG_SOURCE_DIR}/jcinit.c    ${LIBJPEG_SOURCE_DIR}/jcmaster.c  ${LIBJPEG_SOURCE_DIR}/jcmainct.c  ${LIBJPEG_SOURCE_DIR}/jcprepct.c
    ${LIBJPEG_SOURCE_DIR}/jccoefct.c  ${LIBJPEG_SOURCE_DIR}/jccolor.c   ${LIBJPEG_SOURCE_DIR}/jcsample.c  ${LIBJPEG_SOURCE_DIR}/jcdctmgr.c
    ${LIBJPEG_SOURCE_DIR}/jfdctint.c  ${LIBJPEG_SOURCE_DIR}/jfdctfst.c  ${LIBJPEG_SOURCE_DIR}/jfdctflt.c  ${LIBJPEG_SOURCE_DIR}/jchuff.c
    ${LIBJPEG_SOURCE_DIR}/jcarith.c   ${LIBJPEG_SOURCE_DIR}/jcmarker.c  ${LIBJPEG_SOURCE_DIR}/jdatadst.c

    # decompression
    ${LIBJPEG_SOURCE_DIR}/jdmaster.c  ${LIBJPEG_SOURCE_DIR}/jdinput.c   ${LIBJPEG_SOURCE_DIR}/jdmainct.c  ${LIBJPEG_SOURCE_DIR}/jdcoefct.c
    ${LIBJPEG_SOURCE_DIR}/jdpostct.c  ${LIBJPEG_SOURCE_DIR}/jdmarker.c  ${LIBJPEG_SOURCE_DIR}/jdhuff.c    ${LIBJPEG_SOURCE_DIR}/jdarith.c
    ${LIBJPEG_SOURCE_DIR}/jddctmgr.c  ${LIBJPEG_SOURCE_DIR}/jidctint.c  ${LIBJPEG_SOURCE_DIR}/jidctfst.c  ${LIBJPEG_SOURCE_DIR}/jidctflt.c
    ${LIBJPEG_SOURCE_DIR}/jdsample.c  ${LIBJPEG_SOURCE_DIR}/jdcolor.c   ${LIBJPEG_SOURCE_DIR}/jdmerge.c   ${LIBJPEG_SOURCE_DIR}/jquant1.c
    ${LIBJPEG_SOURCE_DIR}/jquant2.c   ${LIBJPEG_SOURCE_DIR}/jdatasrc.c
  )

  # installation
  set(LIBJPEG_PUBLIC_HEADERS 
    ${LIBJPEG_SOURCE_DIR}/../Config/jconfig.h 
    ${LIBJPEG_SOURCE_DIR}/jpeglib.h 
    ${LIBJPEG_SOURCE_DIR}/jmorecfg.h 
    ${LIBJPEG_SOURCE_DIR}/jerror.h
    ${LIBJPEG_SOURCE_DIR}/jinclude.h
    ${LIBJPEG_SOURCE_DIR}/jpegint.h
    #${LIBJPEG_SOURCE_DIR}/jdct.h
    #${LIBJPEG_SOURCE_DIR}/jmemsys.h
    ${LIBJPEG_SOURCE_DIR}/jversion.h
  )

  if(DEFINED BUILD_SHARED_LIBS)
  if(CMAKE_HOST_WIN32)
      set(JPEG_BUILD_SHARED_TMP False) # unactivated because needs code change inside the library
    else()
      set(JPEG_BUILD_SHARED_TMP ${BUILD_SHARED_LIBS})
    endif()
  else()
    set(JPEG_BUILD_SHARED_TMP False)
  endif()
  set(LIBJPEG_BUILD_SHARED ${JPEG_BUILD_SHARED_TMP} CACHE BOOL "Build JPEG shared (activate this if you know what you are doing)")

  if(CMAKE_HOST_WIN32)
    if(LIBJPEG_BUILD_SHARED)
      set(LIBJPEG_SRC ${LIBJPEG_SRC} ${LIBJPEG_SOURCE_DIR}/../Config/jpeg.def)
    endif()
  endif()

  include_directories(${LIBJPEG_SOURCE_DIR}/../Config/)

  if(LIBJPEG_BUILD_SHARED)
    message("Shared JPEG")
    add_library (${LIBJPEG} SHARED ${LIBJPEG_SRC} ${LIBJPEG_PUBLIC_HEADERS}) 
  else()
    message("Static JPEG")
  add_library (${LIBJPEG} STATIC ${LIBJPEG_SRC} ${LIBJPEG_PUBLIC_HEADERS}) 
  endif()
  
  set(JPEG                ${LIBJPEG}              PARENT_SCOPE)
  set(JPEG_LIB_SRC        ${CMAKE_CURRENT_SOURCE_DIR}/${LIBJPEG_SOURCE_DIR}   PARENT_SCOPE)
  install(TARGETS ${LIBJPEG} CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
  install(FILES ${LIBJPEG_PUBLIC_HEADERS} DESTINATION include/${LIBJPEG} COMPONENT headers)

#endif(JPEG_FOUND)







# ZLib

project(zlib-1.2.3)
#find_package(ZLIB)
set(ZLIB_FOUND False)
if(ZLIB_FOUND)
  message("Zlib location is ${ZLIB_INCLUDE_DIR}")
  set(ZLIB_INCLUDE_DIR       ${ZLIB_INCLUDE_DIR}  PARENT_SCOPE)
  set(ZLIB_LIBRARIES         ${ZLIB_LIBRARIES}    PARENT_SCOPE)
else(ZLIB_FOUND)

  set(LIBZLIB zlib-1.2.3)
  set(ZLIB_SOURCE_DIR
        ${LIBZLIB}
        CACHE PATH
        "ZLib sources directory")

  message("Zlib directory is ${ZLIB_SOURCE_DIR}")

  #win32\zlib.def
  set(ZLIB_SRC

    ${ZLIB_SOURCE_DIR}/adler32.c
    ${ZLIB_SOURCE_DIR}/compress.c
    ${ZLIB_SOURCE_DIR}/crc32.c
    ${ZLIB_SOURCE_DIR}/deflate.c
    ${ZLIB_SOURCE_DIR}/gzio.c
    ${ZLIB_SOURCE_DIR}/infback.c
    ${ZLIB_SOURCE_DIR}/inffast.c
    ${ZLIB_SOURCE_DIR}/inflate.c
    ${ZLIB_SOURCE_DIR}/inftrees.c
    ${ZLIB_SOURCE_DIR}/trees.c
    ${ZLIB_SOURCE_DIR}/uncompr.c
    ${ZLIB_SOURCE_DIR}/zutil.c

    ${ZLIB_SOURCE_DIR}/zutil.c
    ${ZLIB_SOURCE_DIR}/crc32.h
    ${ZLIB_SOURCE_DIR}/deflate.h
    ${ZLIB_SOURCE_DIR}/inffast.h
    ${ZLIB_SOURCE_DIR}/inffixed.h
    ${ZLIB_SOURCE_DIR}/inflate.h
    ${ZLIB_SOURCE_DIR}/inftrees.h
    ${ZLIB_SOURCE_DIR}/trees.h

    #${ZLIB_SOURCE_DIR}/contrib/masmx86/gvmat32.asm
    #${ZLIB_SOURCE_DIR}/contrib/masmx86/gvmat32c.c
    #${ZLIB_SOURCE_DIR}/contrib/masmx86/inffas32.asm

  )
  
  set(ZLIB_PUBLIC_HEADERS
    ${ZLIB_SOURCE_DIR}/zlib.h
    ${ZLIB_SOURCE_DIR}/zconf.h
  )
  
  if(DEFINED BUILD_SHARED_LIBS)
    set(ZLIB_BUILD_SHARED_TMP ${BUILD_SHARED_LIBS})
  else()
    set(ZLIB_BUILD_SHARED_TMP False) # false by default unless used by several different librairies
  endif()
  set(ZLIB_BUILD_SHARED ${ZLIB_BUILD_SHARED_TMP} CACHE BOOL "Build ZLIB shared")
  
  if(ZLIB_BUILD_SHARED)
    message("ZLib shared lib")
    if(WIN32)
      set(ZLIB_SRC ${ZLIB_SRC} ${ZLIB_SOURCE_DIR}/win32/zlib.def)
    endif()
    add_library(${LIBZLIB} SHARED ${ZLIB_SRC} ${ZLIB_PUBLIC_HEADERS})
  else()
    message("ZLib static lib")
    add_library(${LIBZLIB} STATIC ${ZLIB_SRC} ${ZLIB_PUBLIC_HEADERS})
  endif()

  if(CMAKE_HOST_WIN32)
    get_target_property(current_def ${LIBZLIB} COMPILE_DEFINITIONS)
    if(NOT current_def)
      set(current_def "")
    endif()    
    if(ZLIB_BUILD_SHARED)
      set(ZLIB_DLL True)
      set(current_def   "${current_def} ZLIB_DLL")
    endif()
    set(current_def_debug   ${current_def})
    set(current_def_release ${current_def} NDEBUG) # for assembly, but needs a special command line and does not seem to be portable: ASMV ASMINF
    set_target_properties(${LIBZLIB} PROPERTIES COMPILE_DEFINITIONS_DEBUG "${current_def_debug}")
    set_target_properties(${LIBZLIB} PROPERTIES COMPILE_DEFINITIONS_RELEASE "${current_def_release}")
    set_target_properties(${LIBZLIB} PROPERTIES DEFINE_SYMBOL "ZLIB_DLL")
  endif()


  set(ZLIB                ${LIBZLIB} PARENT_SCOPE)
  set(ZLIB_SRC_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/${ZLIB_SOURCE_DIR} PARENT_SCOPE)
  install(TARGETS ${LIBZLIB} CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
  install(FILES ${ZLIB_PUBLIC_HEADERS} CONFIGURATIONS Release DESTINATION include/${LIBZLIB} COMPONENT headers)
  
endif(ZLIB_FOUND)






# lib PNG
project(PNG)

# RelativePath="..\..\scripts\pngw32.def"
set(LIBPNG png-1.2.38)
set(LIBPNG_SOURCE_DIR     lib${LIBPNG}     CACHE PATH     "PNG sources directory")

set(LIBPNG_SRC
  ${LIBPNG_SOURCE_DIR}/pngget.c
  ${LIBPNG_SOURCE_DIR}/pngmem.c
  ${LIBPNG_SOURCE_DIR}/pngpread.c
  ${LIBPNG_SOURCE_DIR}/pngread.c
  ${LIBPNG_SOURCE_DIR}/pngrio.c
  ${LIBPNG_SOURCE_DIR}/pngrtran.c
  ${LIBPNG_SOURCE_DIR}/pngrutil.c
  ${LIBPNG_SOURCE_DIR}/pngset.c
  ${LIBPNG_SOURCE_DIR}/pngtrans.c
  
  ${LIBPNG_SOURCE_DIR}/pngerror.c
  ${LIBPNG_SOURCE_DIR}/png.c
  
  ${LIBPNG_SOURCE_DIR}/pngwio.c
  ${LIBPNG_SOURCE_DIR}/pngwrite.c
  ${LIBPNG_SOURCE_DIR}/pngwtran.c
  ${LIBPNG_SOURCE_DIR}/pngwutil.c
)


set(LIBPNG_PUBLIC_HEADERS 
  ${LIBPNG_SOURCE_DIR}/png.h
  ${LIBPNG_SOURCE_DIR}/pngconf.h)

  if(DEFINED BUILD_SHARED_LIBS)
    set(PNG_BUILD_SHARED_TMP ${BUILD_SHARED_LIBS})
  else()
    set(PNG_BUILD_SHARED_TMP False) # false by default, unless used by several libraries
  endif()
  set(LIBPNG_BUILD_SHARED ${PNG_BUILD_SHARED_TMP} CACHE BOOL "Build PNG shared")

if(CMAKE_HOST_WIN32)
  if(ZLIB_BUILD_SHARED AND LIBPNG_BUILD_SHARED)
    set(LIBPNG_SRC ${LIBPNG_SRC} ${LIBPNG_SOURCE_DIR}/scripts/pngw32.def)
  endif()
endif()

include_directories(${ZLIB_SOURCE_DIR})
if(LIBPNG_BUILD_SHARED)
  message("PNG shared lib")
  add_library(${LIBPNG} SHARED ${LIBPNG_SRC} ${LIBPNG_PUBLIC_HEADERS})
else()
  message("PNG static lib")
  add_library(${LIBPNG} STATIC ${LIBPNG_SRC} ${LIBPNG_PUBLIC_HEADERS})
endif()
target_link_libraries(${LIBPNG} ${LIBZLIB})


if(CMAKE_HOST_WIN32)
  # on windows only / warning: get back the Release/Debug definitions
  get_target_property(current_def ${LIBPNG} COMPILE_DEFINITIONS)
  if(NOT current_def)
    set(current_def "")
  endif()
  if(ZLIB_BUILD_SHARED AND LIBPNG_BUILD_SHARED)
    set(current_def ${current_def} PNG_USE_PNGVCRD ZLIB_DLL PNG_LIBPNG_SPECIALBUILD)
  endif()
  set(current_def_debug   ${current_def} DEBUG PNG_DEBUG=1)
  set(current_def_release ${current_def} NDEBUG)
  set_target_properties(${LIBPNG} PROPERTIES COMPILE_DEFINITIONS_DEBUG "${current_def_debug}")
  set_target_properties(${LIBPNG} PROPERTIES COMPILE_DEFINITIONS_RELEASE "${current_def_release}")
  set_target_properties(${LIBPNG} PROPERTIES DEFINE_SYMBOL "PNG_BUILD_DLL")
endif()




set(PNG                 ${LIBPNG}              PARENT_SCOPE)
set(PNG_LIB_SRC         ${CMAKE_CURRENT_SOURCE_DIR}/${LIBPNG_SOURCE_DIR}   PARENT_SCOPE)
install(TARGETS ${LIBPNG} CONFIGURATIONS Release DESTINATION lib COMPONENT libraries)
install(FILES ${LIBPNG_PUBLIC_HEADERS} CONFIGURATIONS Release DESTINATION include/lib${LIBPNG} COMPONENT headers)



# HDF5 IO capabilities
if(ENABLE_HDF5)
  if(WIN32)
    #TODO use /install__Windows_x86 default path 
    set(HDF5 hdf5)
    set(HDF5_SOURCE_DIR
        hdf5
        CACHE PATH
        "hdf5 sources directory")
    message("hdf5 directory is ${HDF5_SOURCE_DIR}")

    # use http://www.hdfgroup.org/HDF5/release/obtain5.html
    #put it in external_libraries\hdf5
    set(HDF5_INSTALL_DIR ${HDF5_SOURCE_DIR} CACHE PATH "HDF5 installation root path")
    set(HDF5_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/${HDF5_INSTALL_DIR}/include PARENT_SCOPE)  
  else(WIN32)
  # to compile with ./configure --prefix=$HOME/usr/local/ --with-zlib=$HOME/usr/local/
  set(HDF5_INSTALL_DIR  ${THIRD_PARTIES_PATH} CACHE PATH "HDF5 installation root path")
  set(HDF5_INCLUDE_DIRS ${HDF5_INSTALL_DIR}/include PARENT_SCOPE)
  endif(WIN32)
  
  find_library(HDF5LIBB hdf5 PATHS ${HDF5_INSTALL_DIR}/lib/
      DOC "HDF5 library found on the system"
      NO_DEFAULT_PATH
      NO_CMAKE_ENVIRONMENT_PATH
      NO_CMAKE_PATH
      NO_SYSTEM_ENVIRONMENT_PATH
      NO_CMAKE_SYSTEM_PATH
  )
  find_library(HDF5LIBL hdf5_hl PATHS ${HDF5_INSTALL_DIR}/lib/
      DOC "HDF5 Lite library found on the system"
      NO_DEFAULT_PATH
      NO_CMAKE_ENVIRONMENT_PATH
      NO_CMAKE_PATH
      NO_SYSTEM_ENVIRONMENT_PATH
      NO_CMAKE_SYSTEM_PATH
  )
  
  get_filename_component(HDF5LIBB2 ${HDF5LIBB} REALPATH)
  get_filename_component(HDF5LIBL2 ${HDF5LIBL} REALPATH)
  
  set(HDF5LIBB ${HDF5LIBB2} PARENT_SCOPE)
  set(HDF5LIBL ${HDF5LIBL2} PARENT_SCOPE)
  
  set(HDF5FilesToInstall ${HDF5LIBB} ${HDF5LIBL})
  install(FILES ${HDF5FilesToInstall} DESTINATION lib COMPONENT libraries)
  if(WIN32)
    install_lib_and_dll("${HDF5FilesToInstall}" lib libraries) 
  endif()



  #set(HDF5LIB "${HDF5LIBB} ${HDF5LIBL}" PARENT_SCOPE)
  
  #add_library(HDF5 SHARED IMPORTED)
  #add_library(HDF5_HL SHARED IMPORTED)
  #set_target_properties(HDF5 PROPERTIES IMPORTED_LOCATION ${HDF5_INSTALL_DIR}/lib/) #${HDF5LIBB})
  #set_target_properties(HDF5_HL PROPERTIES IMPORTED_LOCATION ${HDF5_INSTALL_DIR}/lib/) #${HDF5LIBB})
  #get_target_property(TOTO HDF5 IMPORTED_LOCATION)
  #message("HDF5 name --- " ${TOTO})
  #set(HDF5LIB ${HDF5} ${HDF5_HL} PARENT_SCOPE)
endif()
