/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_COPY_HPP__
#define YAYI_PIXEL_IMAGE_COPY_HPP__

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>


namespace yayi
{

  /*!@brief Copy an image into another
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy(const IImage* imin, IImage* imout);

  /*!@brief Copy a window of an image into a window of another image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy(const IImage* imin, const variant &rectin, const variant &rectout, IImage* imout);

}

#endif

