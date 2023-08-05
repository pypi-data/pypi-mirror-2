/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiLowLevelMorphology/lowlevel_geodesic.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_geodesic_t.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi { namespace llmm {

  yaRC geodesic_erosion(const IImage* imin, const IImage* immask, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, immask, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        geodesic_erode_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_erode_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_erode_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_erode_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >,

        geodesic_erode_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_erode_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_erode_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_erode_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC geodesic_dilation(const IImage* imin, const IImage* immask, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, immask, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        geodesic_dilate_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_dilate_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_dilate_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_dilate_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >,

        geodesic_dilate_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_dilate_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_dilate_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_dilate_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;

  }



}}
