/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiReconstruction/morphological_reconstruction.hpp>
#include <Yayi/core/yayiReconstruction/include/morphological_reconstruction_t.hpp>


#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{
  namespace reconstructions
  {
  
    yaRC opening_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, im_marker, im_mask, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          opening_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
          opening_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          opening_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;
      
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          opening_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
          opening_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          opening_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }

    yaRC closing_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, im_marker, im_mask, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          closing_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
          closing_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          closing_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;
      
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          closing_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
          closing_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          closing_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }

  }
}
