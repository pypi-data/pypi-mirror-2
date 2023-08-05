/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__
#define YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__

#include <Yayi/core/yayiNeighborhoodProcessing/yayiNeighborhoodProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace np
  {
    using namespace yayi::se;
    
    //! Computes the mean for each neighborhood specified by se
    YNPro_ yaRC image_local_mean(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the circular mean and concentration (channel 0) for each neighborhood specified by se
    YNPro_ yaRC image_local_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the circular mean and concentration (channel 0) lineary weighted by channel 2 for each neighborhood specified by se
    YNPro_ yaRC image_local_weighted_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the median of each neighborhood
    YNPro_ yaRC image_local_median(IImage const* imin, IStructuringElement const* se, IImage* imout);

  }
}

#endif /* YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__ */ 
