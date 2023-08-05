/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/python/yayiCommonPython/common_python.hpp>
#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>

using namespace yayi;
using namespace yayi::errors;

void yayi_except_translator(yaException const& x) {
  PyErr_SetString(PyExc_RuntimeError, ("Exception caught : " + x.message()).c_str());
  boost::python::throw_error_already_set();
}


void declare_errors() {
  bpy::register_exception_translator<yaException>(yayi_except_translator);
}

