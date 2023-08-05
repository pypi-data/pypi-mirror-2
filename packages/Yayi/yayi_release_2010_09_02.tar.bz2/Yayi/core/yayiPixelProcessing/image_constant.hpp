/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_CONSTANT_HPP__
#define YAYI_PIXEL_IMAGE_CONSTANT_HPP__

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>


namespace yayi
{

  /*!@brief Sets an image to a constant value
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC constant(IImage* imin, const variant&);


}

#endif

