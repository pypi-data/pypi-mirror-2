/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_ARITHMETIC_HPP__
#define YAYI_PIXEL_IMAGE_ARITHMETIC_HPP__

/*!@file
 * This file defines the arithmetic operations on images
 */

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  //! Adds two images
  YPix_ yaRC image_add(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Subtracts two images
  YPix_ yaRC image_subtract(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Absolute difference of two images
  YPix_ yaRC image_abssubtract(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Multiplies two images
  YPix_ yaRC image_multiply(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Adds a contant value to the image
  YPix_ yaRC image_add_constant(const IImage* imin, variant c, IImage* imout);

  //! Subtracts a contant value from the image
  YPix_ yaRC image_subtract_constant(const IImage* imin, variant c, IImage* imout);

  //! Multiplies an image by a constant value
  YPix_ yaRC image_multiply_constant(const IImage* imin, variant c, IImage* imout);

  //! Computes the intersection (infimum) of two images
  YPix_ yaRC image_infimum(const IImage*imin1, const IImage* imin2, IImage* imout);

  //! Computes the union (supremum) of two images
  YPix_ yaRC image_supremum(const IImage*imin1, const IImage* imin2, IImage* imout);

}

#endif
