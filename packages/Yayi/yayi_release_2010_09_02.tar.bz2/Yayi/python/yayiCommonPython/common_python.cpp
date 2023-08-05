/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

#include <Yayi/python/yayiCommonPython/common_python.hpp>

#ifndef _MSC_VER
#include <dlfcn.h>
#endif


void declare_variants();
void declare_enums();
void declare_utils();
void declare_errors();
void declare_object();
void declare_coordinate();
void declare_return();
void declare_graph();

BOOST_PYTHON_MODULE( YayiCommonPython )
{
  #ifndef _MSC_VER
  bpy::object sys_mod((bpy::handle<>(PyImport_ImportModule("sys"))));
  sys_mod.attr("setdlopenflags")(RTLD_NOW|RTLD_GLOBAL);
  #endif
  
  
  declare_enums();
  declare_utils();
  declare_variants();
  declare_errors();
  declare_object();
  declare_coordinate();
  declare_return();
  declare_graph();
}
