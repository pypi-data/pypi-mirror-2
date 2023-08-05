/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COLOR_PROCESS_HPP__
#define YAYI_COLOR_PROCESS_HPP__


/*!@file
 * This file contains the declaration for color space conversion
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

#include <algorithm>
#include <functional>


namespace yayi
{
  /*!Transforms the image from RGB color space to HLS, defined with the l1 norm
   * References: Jesus Angulo Lopez's PhD, Raffi Enficiaud's PhD
   * @author Raffi Enficiaud
   */
  YPix_ yaRC RGB_to_HLS_l1(const IImage* imin, IImage* imout);

  /*!Transforms the image from HLS l1 color space to RGB
   * References: Jesus Angulo Lopez's PhD, Raffi Enficiaud's PhD
   * @author Raffi Enficiaud
   */
  YPix_ yaRC HLS_l1_to_RGB(const IImage* imin, IImage* imout);


}

#endif // YAYI_COLOR_PROCESS_HPP__
