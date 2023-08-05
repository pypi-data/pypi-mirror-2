/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/python/yayiLabelPython/label_python.hpp>
#include <Yayi/core/yayiLabel/yayi_label_binary_with_measure.hpp>
using namespace yayi::label;


yayi::variant ImageBinaryLabelWithAreaPython(const yayi::IImage* imin, const yayi::se::IStructuringElement* se, yayi::IImage* imout) {

  using namespace yayi;
  variant out;
  yaRC ret = ImageBinaryLabelArea(imin, se, imout, out);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return out;
}




void declare_label_basic() {
  bpy::def("ImageLabel", 
    &ImageLabel, 
    bpy::args("imin", "se", "imout"),
    "labels imin in imout with a single id per connected component");

  bpy::def("ImageBinaryLabelWithAreas", 
    &ImageBinaryLabelWithAreaPython, 
    bpy::args("imin", "se", "imout"), 
    "returns an area \"dictionary\" : binary labels imin in imout with a single "
    "id per connected component, returns the a dictionary associating each id with an area measurement");

}


