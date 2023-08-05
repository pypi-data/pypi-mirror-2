/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiDistances/include/morphological_distance_t.hpp>
#include <Yayi/core/yayiDistances/morphological_distance.hpp>

#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_variantDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>



namespace yayi
{
  namespace distances
  {
  
    yaRC DistanceFromSetsBoundary(const IImage* input, const se::IStructuringElement* se, IImage* output_distance)
    {    
      if(input == 0 || output_distance == 0 || se == 0)
        return yaRC_E_null_pointer;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const se::IStructuringElement*, 
        IImage*> dispatch_object(return_value, input, se, output_distance);


      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          distance_from_sets_boundary< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
          distance_from_sets_boundary< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,         Image<yaUINT16> >
        )
        );
        
      if(res == yaRC_ok) return return_value;
      
      return res;    
    }


    yaRC GeodesicDistanceFromSetsBoundary(const IImage* input, const IImage* mask, const se::IStructuringElement* se, IImage* output_distance)
    {    
      if(input == 0 || output_distance == 0 || se == 0 || mask == 0)
        return yaRC_E_null_pointer;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const IImage*, 
        const se::IStructuringElement*, 
        IImage*> dispatch_object(return_value, input, mask, se, output_distance);


      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          geodesic_distance_from_sets_boundary< Image<yaUINT8>,  Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
          geodesic_distance_from_sets_boundary< Image<yaUINT8>,  Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,         Image<yaUINT16> >
        )
        );
        
      if(res == yaRC_ok) return return_value;
      
      return res;    
    }    
    
    
    
  }
}

