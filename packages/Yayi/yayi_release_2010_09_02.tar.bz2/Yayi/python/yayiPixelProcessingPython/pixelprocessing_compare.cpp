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

#include <Yayi/core/yayiPixelProcessing/image_compare.hpp>

using namespace bpy;

void declare_compare() {

  bpy::enum_<yayi::comparison_operations>("comparison_operations")
    .value("op_equal", yayi::e_co_equal)
    .value("op_diff",  yayi::e_co_different)
    .value("op_supeq", yayi::e_co_superior)
    .value("op_sup",   yayi::e_co_superior_strict)
    .value("op_infeq", yayi::e_co_inferior)
    .value("op_inf",   yayi::e_co_inferior_strict)

    //.export_values()
    ;
    

  def("CompareS",
    &yayi::image_compare_s, 
    bpy::args("im_source", "compare_op", "value", "value_true", "value_false", "im_destination"),
    "Compare an image to value at each pixel, fills the destination image with value_true or value_false accordingly");

  def("CompareI",
    &yayi::image_compare_i, 
    bpy::args("im_source_left", "compare_op", "im_source_right", "value_true", "value_false", "im_destination"),
    "Compare an im_source_left to im_source_right at each pixel, fills the destination image with value_true or value_false accordingly");
    
  def("CompareSI",
    &yayi::image_compare_si,
    bpy::args("im_source", "compare_op", "value_compare", "im_true", "value_false", "im_destination"),
    "Compare an im_source to value_compare at each pixel, set the destination image with the corresponding pixel of im_true or the constant value_false accordingly");

  def("CompareII",
    &yayi::image_compare_ii,
    bpy::args("im_source_left", "compare_op", "im_source_right", "im_true", "value_false", "im_destination"),
    "Compare an im_source_left to im_source_right at each pixel, set the destination image with the corresponding pixel of im_true or the constant value_false accordingly");

  def("CompareIII",
    &yayi::image_compare_iii,
    bpy::args("im_source_left", "compare_op", "im_source_right", "im_true", "im_false", "im_destination"),
    "Compare an im_source_left to im_source_right at each pixel, set the destination image with the corresponding pixel of im_true or im_false accordingly");

  def("CompareSII",
    &yayi::image_compare_sii,
    bpy::args("im_source", "compare_op", "value", "im_true", "im_false", "im_destination"),
    "Compare an im_source to value at each pixel, set the destination image with the corresponding pixel of im_true or im_false accordingly");

    
}
