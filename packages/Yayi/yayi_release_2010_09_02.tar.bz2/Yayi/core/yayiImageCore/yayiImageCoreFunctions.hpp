/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_IMAGE_CORE_FUNCTIONS_HPP__
#define YAYI_IMAGE_CORE_FUNCTIONS_HPP__

/*!@file
 * This file defines some utility functions on the images
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi {
  //! Returns the same image as im
  YCor_ IImage* GetSameImage(const IImage* const &im);
  
  //! Returns an image with the same geometrical properties than im, but with the type of pixels set to t
  YCor_ IImage* GetSameImage(const IImage* const &im, const type& t);
}

#endif
