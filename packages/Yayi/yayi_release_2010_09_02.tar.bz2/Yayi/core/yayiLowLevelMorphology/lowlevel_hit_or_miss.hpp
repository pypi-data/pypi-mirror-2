/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__

/*!@file
 * This file contains the hit-or-miss operations for ordered images, based on the work of 
 * Soille and Ronse.
 */

#include <Yayi/core/yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi { namespace llmm {

  /*! This function implements the hit-or-miss transform for ordered images in the sense defined by Soille
   *  se_foreground and se_background are the structuring elements that should fit the foreground and the background respectively.
   *  se_background should not contain the center and the two structuring elements should have disjoint support (an error is returned otherwise).
   *  @author Raffi Enficiaud
   */
  YLLMM_ yaRC hit_or_miss_soille(const IImage* imin, const se::IStructuringElement* se_foreground, const se::IStructuringElement* se_background, IImage* imout);
  
  
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__ */
