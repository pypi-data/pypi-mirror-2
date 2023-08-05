/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_DISTANCES_HPP__
#define YAYI_MORPHOLOGICAL_DISTANCES_HPP__

/*!@file
 * This file defines the classical morphological distances. The implementation is based
 * on the simple queue propagation
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiDistances/yayiDistances.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace distances
  {
    /*!@brief Morphological distance on input image (from sets boundary)
     * Also known as grid distance transform. 
     * @author Raffi Enficiaud
     */
    YDist_ yaRC DistanceFromSetsBoundary(const IImage* input, const se::IStructuringElement* se, IImage* output_distance);


    /*!@brief Morphological geodesic distance on input image (from sets boundary). 
     * Roughly the same as @ref DistanceFromSetsBoundary, but the distance is computed in a geodesic manner inside the image mask.
     *
     * @author Raffi Enficiaud
     */
    YDist_ yaRC GeodesicDistanceFromSetsBoundary(const IImage* input, const IImage* mask, const se::IStructuringElement* se, IImage* output_distance);
  
  
  }
  
}

#endif /* YAYI_MORPHOLOGICAL_DISTANCES_HPP__ */
