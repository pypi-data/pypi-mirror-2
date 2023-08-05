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
#include <Yayi/core/yayiLabel/yayi_label_extrema.hpp>
using namespace yayi::label;

void declare_label_extrema() {
  bpy::def("ImageLabelMinimas", &ImageLabelMinimas, "(imin, se, imout) : labels minimum plateaus of imin into imout with a single id per connected component");
  bpy::def("ImageLabelMaximas", &ImageLabelMaximas, "(imin, se, imout) : labels maximum plateaus of imin into imout with a single id per connected component");
}
