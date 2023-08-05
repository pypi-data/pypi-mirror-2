/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiMeasurementsPython/measurements_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

void declare_min_max();
void declare_histogram();
void declare_stats();

BOOST_PYTHON_MODULE( YayiMeasurementsPython )
{
  declare_min_max();
  declare_histogram();
  declare_stats();
}
