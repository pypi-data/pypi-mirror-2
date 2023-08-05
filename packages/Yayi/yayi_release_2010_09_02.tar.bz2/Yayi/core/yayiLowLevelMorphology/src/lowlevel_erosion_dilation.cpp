/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/core/yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi { namespace llmm {
    
  yaRC erosion(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        erode_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        erode_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        erode_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        erode_image_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        erode_image_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        erode_image_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        erode_image_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        erode_image_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        erode_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        erode_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        erode_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        erode_image_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        erode_image_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        erode_image_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        erode_image_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        erode_image_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );

    if(res != yaRC_E_not_implemented)
      return res;
    return return_value;

  }

  yaRC dilation(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        dilate_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        dilate_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        dilate_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        dilate_image_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        dilate_image_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        dilate_image_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        dilate_image_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        dilate_image_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        dilate_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        dilate_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        dilate_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        dilate_image_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        dilate_image_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        dilate_image_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        dilate_image_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        dilate_image_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;
  }

  yaRC minkowski_subtraction(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        minkowski_subtraction_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        minkowski_subtraction_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        minkowski_subtraction_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        minkowski_subtraction_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        minkowski_subtraction_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        minkowski_subtraction_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        minkowski_subtraction_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        minkowski_subtraction_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        minkowski_subtraction_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        minkowski_subtraction_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        minkowski_subtraction_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        minkowski_subtraction_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        minkowski_subtraction_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        minkowski_subtraction_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        minkowski_subtraction_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        minkowski_subtraction_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );

    if(res != yaRC_E_not_implemented)
      return res;
    return return_value;

  }


  yaRC minkowski_addition(const IImage* imin, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        minkowski_addition_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        minkowski_addition_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        minkowski_addition_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        minkowski_addition_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        minkowski_addition_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        minkowski_addition_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        minkowski_addition_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        minkowski_addition_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        minkowski_addition_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        minkowski_addition_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        minkowski_addition_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        minkowski_addition_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        minkowski_addition_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        minkowski_addition_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        minkowski_addition_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        minkowski_addition_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );

    if(res != yaRC_E_not_implemented)
      return res;
    return return_value;

  }


}}
