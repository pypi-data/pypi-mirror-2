/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_QUASI_DISTANCES_HPP__
#define YAYI_QUASI_DISTANCES_HPP__

#include <Yayi/core/yayiDistances/yayiDistances.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace distances
  {
  
    /*!@brief Quasi distance on input image
     *
     * The implementation follows the one specified in the PhD of Raffi Enficiaud
     * @author Raffi Enficiaud
     */
    YDist_ yaRC quasi_distance(const IImage* input, const se::IStructuringElement* se, IImage* output_distance, IImage* output_residual);
  
    
    /*!@brief Weighted quasi distance on input image
     *
     * The weights are applied to the residue on each step. The algorithms stops when either no more weights are found or 
     * idempotency is reached.
     * @author Raffi Enficiaud
     */
    YDist_ yaRC quasi_distance_weighted(const IImage* input, const se::IStructuringElement* se, const variant& v_weights, IImage* output_distance, IImage* output_residual);
    
    
    
    /*! Regularization of the result given by the quasi-distances residual algorithm 
     *  @author Raffi Enficiaud
     *  @see quasi_distance
     */
    YDist_ yaRC DistancesRegularization(const IImage* input_distance, const se::IStructuringElement* se, IImage* output_distance);
  
  }
}


#endif /* YAYI_QUASI_DISTANCES_HPP__ */
