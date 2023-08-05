/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiCommon/include/current_configuration.hpp>
#include <Yayi/python/yayiCommonPython/common_python.hpp>

#include <boost/python/tuple.hpp>

bpy::tuple build_version() {
  
  tm date = yayi::current_build_date();
  return bpy::make_tuple(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec);

}

void declare_utils()
{

  bpy::def("current_build_version", yayi::current_build_version, "Returns the current build version");
  bpy::def("current_build_date",    build_version, "Returns the date of build as a tuple in the following format: (year, month, day, hour, minutes, seconds)");
  

}

