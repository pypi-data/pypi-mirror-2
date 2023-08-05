/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiPixelProcessingPython/pixelprocessing_python.hpp>

#include <Yayi/core/yayiPixelProcessing/image_logics.hpp>

using namespace bpy;

void declare_logic() {

  def("LogicalNot",  
    &yayi::image_logical_not, 
    args("im_source", "im_destination"),
    "Logical not of the input image");
}
