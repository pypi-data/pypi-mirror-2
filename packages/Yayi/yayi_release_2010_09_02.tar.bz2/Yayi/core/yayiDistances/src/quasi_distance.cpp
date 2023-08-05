/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiDistances/include/quasi_distance_T.hpp>

#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_variantDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>

namespace yayi
{

  namespace distances
  {
    yaRC quasi_distance(const IImage* input, const se::IStructuringElement* se, IImage* output_distance, IImage* output_residual) {
    
      if(input == 0 || output_distance == 0 || output_residual == 0 || se == 0)
        return yaRC_E_null_pointer;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const se::IStructuringElement*, 
        IImage*, 
        IImage*> dispatch_object(return_value, input, se, output_distance, output_residual);


      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          quasi_distance_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>, Image<yaUINT8>  >,
          quasi_distance_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,         Image<yaUINT16>, Image<yaUINT8>  >,
          quasi_distance_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,         Image<yaUINT16>, Image<yaUINT16> >,

          quasi_distance_t< Image<yaUINT8, s_coordinate<3> >,  se::s_neighborlist_se_hexa_x< s_coordinate<3> >,  Image<yaUINT16, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> >  >,
          quasi_distance_t< Image<yaUINT8, s_coordinate<3> >,  se::s_neighborlist_se< s_coordinate<3> >,         Image<yaUINT16, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> >  >,
          quasi_distance_t< Image<yaF_simple, s_coordinate<3> >,  se::s_neighborlist_se_hexa_x< s_coordinate<3> >,  Image<yaUINT16, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> >  >,
          quasi_distance_t< Image<yaF_simple, s_coordinate<3> >,  se::s_neighborlist_se< s_coordinate<3> >,         Image<yaUINT16, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> >  >,
          quasi_distance_t< Image<yaUINT16, s_coordinate<3> >,  se::s_neighborlist_se< s_coordinate<3> >,          Image<yaUINT16, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> >  >
        )
        );
        
      if(res == yaRC_ok) return return_value;
      
      return res;    
    }
  
    
    yaRC quasi_distance_weighted(const IImage* input, const se::IStructuringElement* se, const variant& v_weights, IImage* output_distance, IImage* output_residual) {
    
      if(input == 0 || output_distance == 0 || output_residual == 0 || se == 0)
        return yaRC_E_null_pointer;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const se::IStructuringElement*, 
        const variant&, 
        IImage*, 
        IImage*> dispatch_object(return_value, input, se, v_weights, output_distance, output_residual);


      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          quasi_distance_weighted_t< Image<yaUINT8>,                        se::s_neighborlist_se< s_coordinate<2> >,        Image<yaUINT16>,                   Image<yaUINT8>  >,
          quasi_distance_weighted_t< Image<yaUINT16>,                       se::s_neighborlist_se< s_coordinate<2> >,        Image<yaUINT16>,                   Image<yaUINT16> >,
          quasi_distance_weighted_t< Image<yaUINT8>,                        se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image<yaUINT16>,                   Image<yaUINT8>  >,
          quasi_distance_weighted_t< Image<yaF_simple, s_coordinate<3> >,   se::s_neighborlist_se_hexa_x< s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> >  >,
          quasi_distance_weighted_t< Image<yaF_simple, s_coordinate<3> >,   se::s_neighborlist_se< s_coordinate<3> >,        Image<yaUINT16, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> >  >,
          quasi_distance_weighted_t< Image<yaUINT16, s_coordinate<3> >,     se::s_neighborlist_se< s_coordinate<3> >,        Image<yaUINT16, s_coordinate<3> >, Image<yaUINT16,   s_coordinate<3> >  >
        )
        );
        
      if(res == yaRC_ok) return return_value;
      
      return res;    
    }    
    
    
    yaRC DistancesRegularization(const IImage* input_distance, const se::IStructuringElement* se, IImage* output_distance) {
    
      if(input_distance == 0 || output_distance == 0 || se == 0)
        return yaRC_E_null_pointer;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const se::IStructuringElement*, 
        IImage*> dispatch_object(return_value, input_distance, se, output_distance);


      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          QuasiDistanceRegularization_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> > >,
          QuasiDistanceRegularization_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> > >,

          QuasiDistanceRegularization_t< Image<yaUINT8,  s_coordinate<3> >, se::s_neighborlist_se_hexa_x< s_coordinate<3> > >,
          QuasiDistanceRegularization_t< Image<yaUINT16, s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> > >
        )
        );
        
      if(res == yaRC_ok) return return_value;
      return res;    
    }
    
  
  
  }


}
