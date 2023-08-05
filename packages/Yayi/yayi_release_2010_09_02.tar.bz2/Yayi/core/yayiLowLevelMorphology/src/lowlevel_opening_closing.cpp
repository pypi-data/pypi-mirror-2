/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiLowLevelMorphology/lowlevel_opening_closing.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_opening_closing_t.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi { namespace llmm {
    
  yaRC open(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        open_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        open_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        open_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        open_image_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        open_image_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        open_image_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        open_image_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        open_image_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        open_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        open_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        open_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        open_image_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        open_image_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        open_image_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        open_image_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        open_image_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );

    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        open_image_t< Image<yaUINT8,  s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT8,  s_coordinate<3> > >,
        open_image_t< Image<yaUINT16, s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT16, s_coordinate<3> > >,
        open_image_t< Image<yaUINT32,s_coordinate<3>  >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT32, s_coordinate<3> > >
      )
      );

    if(res == yaRC_ok) return return_value;
    return res;

  }


  yaRC close(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        close_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        close_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        close_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        close_image_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        close_image_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        close_image_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        close_image_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        close_image_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        close_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        close_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        close_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        close_image_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        close_image_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        close_image_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        close_image_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        close_image_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );

    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        close_image_t< Image<yaUINT8,  s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT8,  s_coordinate<3> > >,
        close_image_t< Image<yaUINT16, s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT16, s_coordinate<3> > >,
        close_image_t< Image<yaUINT32,s_coordinate<3>  >, se::s_neighborlist_se< s_coordinate<3> >,  Image<yaUINT32, s_coordinate<3> > >
      )
      );

      
    if(res == yaRC_ok) return return_value;
    return res;

  }





}}
