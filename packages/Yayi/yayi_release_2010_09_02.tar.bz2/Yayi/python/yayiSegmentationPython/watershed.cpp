/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiSegmentationPython/segmentation_python.hpp>


using namespace bpy;


void declare_watershed() {
  using namespace yayi;
  def("IsotropicSeededWatershed",
    (yaRC (*)(const IImage *, const IImage*, const se::IStructuringElement*, IImage*))&yayi::segmentation::isotropic_watershed, 
    bpy::args("topographical_map", "im_seeds", "SE", "watershed"),
    "Performs the isotropic watershed transform of topographical_map, and using im_seeds as seeds"
  );
  
  def("IsotropicWatershed",
    (yaRC (*)(const IImage *, const se::IStructuringElement*, IImage*))&yayi::segmentation::isotropic_watershed, 
    bpy::args("topographical_map", "SE", "watershed"),
    "Performs the isotropic watershed transform of topographical_map, and using local minima as seeds"
  );
}
