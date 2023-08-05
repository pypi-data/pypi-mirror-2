/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiMeasurements/measurements_min_max.hpp>
#include <Yayi/core/yayiMeasurements/include/measurements_min_max_t.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi
{
  namespace measurements
  {

    yaRC image_meas_min_max(const IImage* imin, variant& out)
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
          image_meas_min_max_t< Image<yaUINT8> >,
          image_meas_min_max_t< Image<yaUINT16> >,
          image_meas_min_max_t< Image<yaUINT32> >,
          image_meas_min_max_t< Image<yaUINT64> >,
          image_meas_min_max_t< Image<yaF_simple> >,
          image_meas_min_max_t< Image<yaF_double> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
      return res;   
    }
  }
}
