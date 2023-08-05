/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiReconstructionPython/reconstruction_python.hpp>
#include <Yayi/core/yayiReconstruction/morphological_reconstruction.hpp>
#include <Yayi/core/yayiReconstruction/morphological_leveling.hpp>

void declare_morphological_reconstructions()
{
  using namespace bpy;
  def("OpeningByReconsutruction",
    &yayi::reconstructions::opening_by_reconstruction, 
    bpy::args("image_marker", "image_mask", "SE", "reconstruction"),
    "Performs an algebraic opening by morphological reconstruction of image_marker under image_mask (successive geodesic dilations)"
  );

  def("ClosingByReconsutruction",
    &yayi::reconstructions::closing_by_reconstruction, 
    bpy::args("image_marker", "image_mask", "SE", "reconstruction"),
    "Performs an algebraic closing by morphological reconstruction of image_marker over image_mask (successive geodesic erosions)"
  );

  def("Levelings",
    &yayi::reconstructions::leveling_by_double_reconstruction, 
    bpy::args("image_marker", "image_mask", "SE", "levelings"),
    "Performs a leveling of image_marker with reference image_mask"
  );
}
