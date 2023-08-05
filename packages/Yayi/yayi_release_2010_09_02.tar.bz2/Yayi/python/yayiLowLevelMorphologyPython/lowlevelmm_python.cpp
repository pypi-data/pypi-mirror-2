/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiLowLevelMorphologyPython/lowlevelmm_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;


void declare_rank_functions();
void declare_gradient_functions();
void declare_geodesic_functions();
void declare_hit_or_miss_functions();

BOOST_PYTHON_MODULE( YayiLowLevelMorphologyPython )
{
  declare_rank_functions();
  declare_gradient_functions();
  declare_geodesic_functions();
  declare_hit_or_miss_functions();
}
