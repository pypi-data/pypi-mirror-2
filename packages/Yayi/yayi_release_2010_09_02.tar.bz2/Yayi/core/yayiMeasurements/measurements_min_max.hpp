/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_MIN_MAX_HPP__
#define YAYI_MEASUREMENTS_MIN_MAX_HPP__

/*!@file
 * This file defines the min/max function
 */

#include <Yayi/core/yayiMeasurements/yayiMeasurements.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  namespace measurements
  {
    //! This function computes the min and max over the image, and return the result in the variant as a pair of values of the same type as the image
    YMeas_ yaRC image_meas_min_max(const IImage* imin, variant& out);
     
    
    
  }
}


#endif /* YAYI_MEASUREMENTS_MIN_MAX_HPP__ */
