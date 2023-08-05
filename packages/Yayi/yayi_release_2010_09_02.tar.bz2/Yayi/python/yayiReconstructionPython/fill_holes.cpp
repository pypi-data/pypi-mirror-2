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
#include <Yayi/core/yayiReconstruction/morphological_fill_holes.hpp>

void declare_morphological_fill_holes()
{
  using namespace bpy;
  def("FillHoles",
    &yayi::reconstructions::fill_holes, 
    bpy::args("imin", "SE", "imout"),
    "Fills the holes of imin using SE as neighboring graph. Stores the output in imout"
  );


}
