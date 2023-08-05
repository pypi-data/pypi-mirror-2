/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_T_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_T_HPP__

/*!@file
 * This file contains the hit-or-miss operations for ordered images, based on the work of 
 * Soille and Ronse.
 */

#include <Yayi/core/yayiStructuringElement/include/yayiDisjointPairedStructuringElement_t.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_arithmetics_t.hpp>

namespace yayi { namespace llmm {
  
  
  /*! Hit-or-miss of imin into imout, using structuring element se
   * This implementation uses the Soille's definition for gray level images with flat SE. 
   * See for instance B. Naegel et al., Pattern Recognition 40 (2007), p 641, Eq. 26.
   *
   * @author Raffi Enficiaud
   */
  template <class image_in_t, class se_t, class image_out_t>
  yaRC hit_or_miss_soille_image_t(const image_in_t& imin, const se_t& se_foreground, const se_t& se_background, image_out_t& imout)
  {
    s_disjoined_paired_se<se_t> disjoin_se(se_foreground, se_background);
    
    if(!disjoin_se.are_disjoint())
    {
      DEBUG_INFO("The provided structuring elements do not seem to have disjoin support");
      return yaRC_E_bad_parameters;
    }
    
    yaRC res = erode_image_t/* minkowski_subtraction_t */(imin, se_foreground, imout);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("An error occured during the minkowski subtraction");
      return res;
    }
    
    
    #if 0
    for(offset i = 0, j = total_number_of_points(imout.Size()); i < j; i++) {
      std::cout << int_to_string(imout.pixel(i), 2) << " ";
      if(((i+1) % imout.Size()[0]) == 0)
        std::cout << std::endl;
    }
    std::cout << std::endl;
    #endif
    
    image_in_t imtemp;
    res = imtemp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("An error occured during the allocation of the temporary image");
      return res;
    }
    
    res = /*minkowski_addition_t */dilate_image_t(imin, se_background, imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("An error occured during the dilation");
      return res;
    }
    
    #if 0
    for(offset i = 0, j = total_number_of_points(imout.Size()); i < j; i++) {
      std::cout << int_to_string(imtemp.pixel(i), 2) << " ";
      if(((i+1) % imout.Size()[0]) == 0)
        std::cout << std::endl;
    }
    std::cout << std::endl;    
    #endif
    
    return subtract_with_carry_images_t(imout, imtemp, 0, imout);
  }

  
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_T_HPP__ */
