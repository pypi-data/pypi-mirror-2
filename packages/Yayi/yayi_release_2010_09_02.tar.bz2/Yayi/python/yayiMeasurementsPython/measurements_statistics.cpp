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
#include <Yayi/core/yayiMeasurements/measurements_mean_variance.hpp>
#include <Yayi/core/yayiMeasurements/measurements_quantiles.hpp>

using namespace yayi;

void declare_stats()
{
  bpy::def("meas_mean",
    &measurements_function<&measurements::image_meas_mean>,
    bpy::args("imin"),
    "Returns the mean of the image");
    
  bpy::def("meas_mean_on_regions", 
    &measurements_on_regions_function<&measurements::image_meas_mean_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the mean for each region of the image. The regions are non-overlapping and defined by imregions");

  bpy::def("meas_circular_mean_and_concentration_on_regions", 
    &measurements_on_regions_function<&measurements::image_meas_circular_mean_and_concentration_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the circular mean and concentration for each region of the image. "
    "The regions are non-overlapping and defined by imregions. "
    "The return type is a map of complex elements");

  bpy::def("meas_weighted_circular_mean_and_concentration_on_region", 
    &measurements_on_regions_function<&measurements::image_meas_weighted_circular_mean_and_concentration_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the circular mean and concentration of channel 0 weighted by channel 2 for each region of the image. "
    "The regions are non-overlapping and defined by imregions. "
    "The return type is a map of complex elements.");




  bpy::def("meas_median",
    &measurements_function<&measurements::image_meas_median>,
    bpy::args("imin"),
    "Returns the median of the image");
    

}
