/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__

/*!@file
 * 
 */

#include <Yayi/core/yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_neighborhoodProcessing_t.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_neighbor_operators_t.hpp>



namespace yayi { namespace llmm {
  
  /*!@brief Template function for generic gradient
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_minus_min_element_subset<typename image_out::pixel_type> neighbor_operator_t;
  
    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;
    
    neighbor_operator_t op;
    return op_processor(imin, se, op, imout);
  }
  
  /*!@brief Template function for generic half superior gradient
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_sup_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_minus_center_element_subset<typename image_out::pixel_type> neighbor_operator_t;
  
    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;
    
    neighbor_operator_t op;
    return op_processor.neighbor_op_with_center(imin, se, op, imout);
  }  
  
  /*!@brief Template function for generic half superior gradient
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_inf_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_center_minus_min_element_subset<typename image_out::pixel_type> neighbor_operator_t;
  
    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;
    
    neighbor_operator_t op;
    return op_processor.neighbor_op_with_center(imin, se, op, imout);
  }    
  
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__ */
