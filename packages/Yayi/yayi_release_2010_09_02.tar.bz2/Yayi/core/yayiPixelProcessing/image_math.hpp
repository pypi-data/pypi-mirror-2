/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_MATH_HPP__
#define YAYI_PIXEL_IMAGE_MATH_HPP__

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>


/*!@file
 * This file contains several mathematical function (log, power, sqrt, random...)
 */

namespace yayi
{

  /*!@brief Computes the logarithm of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC logarithm(const IImage *imin, IImage *imout);
  
  /*!@brief Computes the exponential of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC exponential(const IImage *imin, IImage *imout);
  
  /*!@brief Computes the power of each pixels of the image
   *
   * @param[in] var exponent
   * @author Raffi Enficiaud
   */
  YPix_ yaRC power(const IImage *imin, const variant& var, IImage *imout);

  /*!@brief Computes the square of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC square(const IImage *imin, IImage *imout);

  /*!@brief Computes the square root of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC square_root(const IImage *imin, IImage *imout);

  /*!@brief Generates the pixels of the image as being drawn from a gaussian distribution
   * with zero mean and unary variance
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC generate_gaussian_random(IImage* imin, yaF_double mean = 0., yaF_double std_deviation = 1.);


}

#endif

