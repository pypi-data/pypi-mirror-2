/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_QUANTILES_HPP__
#define YAYI_MEASUREMENTS_QUANTILES_HPP__

/*!@file
 * This file defines the quantiles functions
 */

#include <Yayi/core/yayiMeasurements/yayiMeasurements.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  namespace measurements
  {
    //! This function computes the median over the image
    YMeas_ yaRC image_meas_median(const IImage* imin, variant& out);
     
    
    
  }
}


#endif /* YAYI_MEASUREMENTS_QUANTILES_HPP__ */
