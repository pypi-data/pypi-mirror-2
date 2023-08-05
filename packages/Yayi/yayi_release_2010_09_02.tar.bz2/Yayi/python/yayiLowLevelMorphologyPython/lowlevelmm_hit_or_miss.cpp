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
#include <Yayi/core/yayiLowLevelMorphology/lowlevel_hit_or_miss.hpp>
using namespace bpy;

void declare_hit_or_miss_functions() {
  def("SoillesHitOrMiss",
    &yayi::llmm::hit_or_miss_soille,
    bpy::args("im_source", "foreground_SE", "background_SE", "im_destination"),
    "Performs the hit-or_miss transform for gray level images based on Soilles definition.");

}
