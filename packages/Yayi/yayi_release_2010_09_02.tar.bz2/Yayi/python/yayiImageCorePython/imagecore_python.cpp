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

#include <Yayi/python/yayiImageCorePython/imagecore_python.hpp>

void declare_image();
void declare_iterators();
void declare_interface_pixel();

BOOST_PYTHON_MODULE( YayiImageCorePython )
{
  declare_image();
  declare_iterators();
  declare_interface_pixel();
}
