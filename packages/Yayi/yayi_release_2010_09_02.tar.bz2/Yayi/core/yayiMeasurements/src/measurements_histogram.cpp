/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiMeasurements/measurements_histogram.hpp>
#include <Yayi/core/yayiMeasurements/include/measurements_histogram_t.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_variantDispatch.hpp>

namespace yayi
{
  namespace measurements
  {

    yaRC image_meas_histogram(const IImage* imin, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      

      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        variant&> dispatch_object(return_value, imin, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_histogram_t< Image<yaUINT8> >,
          image_meas_histogram_t< Image<yaUINT16> >,
          image_meas_histogram_t< Image<yaUINT32> >,
          image_meas_histogram_t< Image<yaUINT64> >,
          image_meas_histogram_t< Image<yaF_simple> >,
          image_meas_histogram_t< Image<yaF_double> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;

      // pixel3
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_histogram_t< Image<pixel8u_3>  >,
          image_meas_histogram_t< Image<pixel16u_3> >,
          image_meas_histogram_t< Image<pixelFs_3>  >,
          image_meas_histogram_t< Image<pixelFd_3>  >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;

      // 3D
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_histogram_t< Image<yaUINT8,    s_coordinate<3> > >,
          image_meas_histogram_t< Image<yaUINT16,   s_coordinate<3> > >,
          image_meas_histogram_t< Image<yaUINT32,   s_coordinate<3> > >,
          image_meas_histogram_t< Image<yaUINT64,   s_coordinate<3> > >,
          image_meas_histogram_t< Image<yaF_simple, s_coordinate<3> > >,
          image_meas_histogram_t< Image<yaF_double, s_coordinate<3> > >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;


      return res;   
    }

    yaRC image_meas_histogram_on_regions(const IImage* imin, const IImage* imregions, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      

      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const IImage*,
        variant&> dispatch_object(return_value, imin, imregions, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_histogram_on_region_t< Image<yaUINT8> , Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<yaUINT16>, Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<yaUINT32>, Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<yaUINT64>, Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<yaF_simple>, Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<yaF_double>, Image<yaUINT16> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
        
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_histogram_on_region_t< Image<pixel8u_3>,  Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<pixel16u_3>, Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<pixelFs_3>,  Image<yaUINT16> >,
          image_meas_histogram_on_region_t< Image<pixelFd_3>,  Image<yaUINT16> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;        
      return res;   
    }
    
    
  }
}
