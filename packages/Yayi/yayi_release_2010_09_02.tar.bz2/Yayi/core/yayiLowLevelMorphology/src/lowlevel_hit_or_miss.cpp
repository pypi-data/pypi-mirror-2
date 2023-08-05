/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/core/yayiLowLevelMorphology/lowlevel_hit_or_miss.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_hit_or_miss_t.hpp>

#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi { namespace llmm {
  yaRC hit_or_miss_soille(const IImage* imin, const IStructuringElement* se_foreground, const IStructuringElement* se_background, IImage* imout)
  {
    using namespace dispatcher;
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, 
      const IImage*, 
      const IStructuringElement*, 
      const IStructuringElement*, 
      IImage*> dispatch_object(return_value, imin, se_foreground, se_background, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        hit_or_miss_soille_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        hit_or_miss_soille_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        hit_or_miss_soille_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        hit_or_miss_soille_image_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        hit_or_miss_soille_image_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        hit_or_miss_soille_image_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        hit_or_miss_soille_image_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        hit_or_miss_soille_image_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        hit_or_miss_soille_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        hit_or_miss_soille_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        hit_or_miss_soille_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        hit_or_miss_soille_image_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        hit_or_miss_soille_image_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        hit_or_miss_soille_image_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        hit_or_miss_soille_image_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        hit_or_miss_soille_image_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
      
    if(res == yaRC_ok) return return_value;
    return res;
  }

}}
