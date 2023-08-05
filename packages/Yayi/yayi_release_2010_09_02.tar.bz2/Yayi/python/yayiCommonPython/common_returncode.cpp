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
#include <Yayi/core/yayiCommon/common_coordinates.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_types.hpp>

struct custom_yaRC_to_python
{
  static PyObject* convert(yayi::yaRC const& s)
  {
    using namespace yayi;
    if(s.code != return_code_constants::e_Yr_ok)
      throw yayi::errors::yaException("Error : " + (std::string)s);
    else
      Py_RETURN_NONE;
  }
};


void declare_return() {
  boost::python::to_python_converter<yayi::yaRC, custom_yaRC_to_python>();
}

