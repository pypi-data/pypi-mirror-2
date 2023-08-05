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
#include <Yayi/python/yayiLabelPython/label_python.hpp>

void declare_label_basic();
void declare_label_extrema();

BOOST_PYTHON_MODULE( YayiLabelPython )
{
  declare_label_basic();
  declare_label_extrema();
}
