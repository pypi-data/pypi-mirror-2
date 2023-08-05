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
#include <Yayi/core/yayiMeasurements/measurements_histogram.hpp>

using namespace yayi;



void declare_histogram()
{
  bpy::def("meas_histogram",
    &measurements_function<&measurements::image_meas_histogram>,
    bpy::args("imin"),
    "Returns the histogram of the image");
  bpy::def("meas_histogram_on_regions", 
    &measurements_on_regions_function<&measurements::image_meas_histogram_on_regions>,
    bpy::args("imin", "imregions"),
    "Returns the histogram for each region of the image. The regions are non-overlapping and defined by imregions");
}
