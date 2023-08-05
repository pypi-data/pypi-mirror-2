/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMPARE_HPP__
#define YAYI_COMPARE_HPP__

/*!@file
 * This file contains the image comparison stub functions
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  
  //! Returns a pixel wise comparison of imin with value. For each pixel, assigns true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_s(const IImage* imin, comparison_operations c, variant value, variant true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_i(const IImage* imin1, comparison_operations c, const IImage* imin2, variant true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with value. For each pixel, assigns the corresponding pixel of im_true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_si(const IImage* imin1, comparison_operations c, variant value, const IImage* im_true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns the corresponding pixel of im_true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_ii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns the corresponding pixel of im_true_value or im_false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_iii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, const IImage* im_false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with the constant value. For each pixel, assigns the corresponding pixel of im_true_value or im_false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_sii(const IImage* imin1, comparison_operations c, variant value, const IImage* im_true_value, const IImage* im_false_value, IImage* imout);

}

#endif /* YAYI_COMPARE_HPP__ */
