/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_LOGIC_HPP__
#define YAYI_PIXEL_IMAGE_LOGIC_HPP__

/*!@file
 * This file defines the logic operations on images
 */

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  //! Performs a logical not on the input image
  YPix_ yaRC image_logical_not(const IImage* imin, IImage* imout);

}



#endif /* YAYI_PIXEL_IMAGE_LOGIC_HPP__ */
