/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef MEASUREMENTS_MEAN_VARIANCE_HPP__
#define MEASUREMENTS_MEAN_VARIANCE_HPP__


/*!@file
 * This file defines simple statistic functions over images
 */

#include <Yayi/core/yayiMeasurements/yayiMeasurements.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>



namespace yayi
{
  namespace measurements
  {
  
    //! Returns the mean over the image
    YMeas_ yaRC image_meas_mean(const IImage* imin, variant& out);
    
    //! Returns the mean on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    YMeas_ yaRC image_meas_mean_on_region(const IImage* imin, const IImage* imregions, variant& out);

    //! Returns the circular mean on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    YMeas_ yaRC image_meas_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out);

    //! Returns the circular mean on first channel linearly weighted by third channel, on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    YMeas_ yaRC image_meas_weighted_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out);

  
  }
}


#endif /* MEASUREMENTS_MEAN_VARIANCE_HPP__ */

