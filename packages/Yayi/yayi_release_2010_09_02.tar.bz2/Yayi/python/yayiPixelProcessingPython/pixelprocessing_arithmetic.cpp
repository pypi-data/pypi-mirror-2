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

#include <Yayi/core/yayiPixelProcessing/image_arithmetics.hpp>

using namespace bpy;

void declare_arithmetic() {

  def("Add",  
      &yayi::image_add, 
      args("im_source1", "im_source2", "im_destination"),
      "Adds two images");

  def("Substract",  
      &yayi::image_subtract, 
      args("im_source1", "im_source2", "im_destination"),
      "Subtracts two images");

  def("AbsSubstract",  
      &yayi::image_abssubtract, 
      args("im_source1", "im_source2", "im_destination"),
      "Subtracts two images");
  
  def("Multiply",  
      &yayi::image_multiply, 
      args("im_source1", "im_source2", "im_destination"),
      "Multiplies two images");

  def("AddConstant",  
      &yayi::image_add_constant, 
      args("im_source", "value", "im_destination"),
      "Add a contant value to the image");

  def("SubtractConstant",  
      &yayi::image_subtract_constant, 
      args("im_source", "value", "im_destination"),
      "Subtract a contant value from the image");

  def("MultiplyConstant",  
      &yayi::image_multiply_constant, 
      args("im_source", "value", "im_destination"),
      "Multiply an image by a constant value");
  
  def("Intersection",  
      &yayi::image_infimum, 
      args("im_source1", "im_source2", "im_destination"),
      "Intersection (infimum) of two images");

  def("Union",  
      &yayi::image_supremum, 
      args("im_source1", "im_source2", "im_destination"),
      "Union (supremum) of two images");
  

}
