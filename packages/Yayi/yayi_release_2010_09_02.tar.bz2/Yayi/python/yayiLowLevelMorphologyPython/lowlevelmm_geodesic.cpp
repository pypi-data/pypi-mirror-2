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
#include <Yayi/core/yayiLowLevelMorphology/lowlevel_geodesic.hpp>
using namespace bpy;

void declare_geodesic_functions() {
  def("GeodesicDilation",
    &yayi::llmm::geodesic_dilation,
    bpy::args("im_source", "im_mask", "SE", "im_destination"),
    "Performs the classical geodesic dilation of im_source under im_mask with the provided structuring element");
    
  def("GeodesicErosion",
    &yayi::llmm::geodesic_erosion,  
    bpy::args("im_source", "im_mask", "SE", "im_destination"),
    "Performs the classical geodesic erosion of im_source over im_mask with the provided structuring element");
}
