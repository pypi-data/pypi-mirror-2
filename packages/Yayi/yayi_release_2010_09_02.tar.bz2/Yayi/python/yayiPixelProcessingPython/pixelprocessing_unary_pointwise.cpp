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

#include <Yayi/core/yayiPixelProcessing/image_constant.hpp>
#include <Yayi/core/yayiPixelProcessing/image_copy.hpp>
#include <Yayi/core/yayiPixelProcessing/image_channels_process.hpp>



using namespace bpy;

void declare_unary_pointwise() {

  def("Copy",
      (yayi::yaRC (*)(const yayi::IImage*, yayi::IImage* ))&yayi::copy,
      bpy::args("im_source", "im_destination"), 
      "Copy one image onto another");

  def("Constant", 
      &yayi::constant, 
      bpy::args("im", "value"),
      "Sets all the pixels of the image to value \"value\"");

  def("CopyWindow", 
      (yayi::yaRC (*)(const yayi::IImage*, const yayi::variant &, const yayi::variant &, yayi::IImage* ))&yayi::copy,
       bpy::args("im_source", "window_source", "window_destination", "im_destination"), 
       "Copy a window of an image onto a window of another image");


}

