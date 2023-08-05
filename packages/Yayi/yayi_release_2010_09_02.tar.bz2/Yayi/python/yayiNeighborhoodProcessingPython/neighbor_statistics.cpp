/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiNeighborhoodProcessingPython/neighborhoodprocessing_python.hpp>
#include <Yayi/core/yayiNeighborhoodProcessing/np_local_statistics.hpp>

using namespace yayi;



void declare_local_statistics()
{
  bpy::def("local_mean", 
    &np::image_local_mean,
    bpy::args("imin", "se", "imout"),
    "Computes the mean over each neighborhoods of imin defined by se");
  
  bpy::def("local_circular_mean_and_concentration", 
    &np::image_local_circular_mean_and_concentration,
    bpy::args("imin", "se", "imout"),
    "Computes the circular mean and concentration over each neighborhoods of imin defined by se (imout should be complex)");  
  
  bpy::def("local_weighted_circular_mean_and_concentration", 
    &np::image_local_weighted_circular_mean_and_concentration,
    bpy::args("imin", "se", "imout"),
    "Computes the circular mean and concentration of channel 0 linearly weighted by channel 2 over each neighborhoods of imin defined by se (imout should be complex)");  
  
  bpy::def("local_median", 
    &np::image_local_median,
    bpy::args("imin", "se", "imout"),
    "Computes the median on each neighborhood");  
  
  
  
  
  
}


