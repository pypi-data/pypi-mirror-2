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
#include <Yayi/core/yayiMeasurements/measurements_min_max.hpp>

using namespace yayi;



void declare_min_max()
{
  bpy::def("meas_min_max", 
    &measurements_function<&measurements::image_meas_min_max>
    );
  
}
