/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_HISTOGRAM_HPP__
#define YAYI_MEASUREMENTS_HISTOGRAM_HPP__

/*!@file
 * This file defines the histogram functions
 */

#include <Yayi/core/yayiMeasurements/yayiMeasurements.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  namespace measurements
  {
    //! This function computes the histogram over the image, and return the result in the variant as sequence of pairs (key, value)
    YMeas_ yaRC image_meas_histogram(const IImage* imin, variant& out);

    //! This function computes an histogram on each regions defined by imregions, and return the result 
    //! in the variant as a sequence of pairs (region_id, histogram)
    YMeas_ yaRC image_meas_histogram_on_regions(const IImage* imin, const IImage* imregions, variant& out);

  }
}

#endif /* YAYI_MEASUREMENTS_HISTOGRAM_HPP__ */
