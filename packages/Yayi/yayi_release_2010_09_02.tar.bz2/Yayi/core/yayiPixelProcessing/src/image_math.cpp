/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/core/yayiPixelProcessing/image_math.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_math_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi
{

  yaRC logarithm(const IImage *imin, IImage *imout)
  {
    yaRC return_value;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, IImage*> dispatch_object(return_value, imin, imout);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        logarithm_t< Image<yaUINT8>,    Image<yaF_double> >,
        logarithm_t< Image<yaF_double>,    Image<yaF_double> >,
        logarithm_t< Image<yaF_simple>,    Image<yaF_simple> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  
  yaRC exponential(const IImage *imin, IImage *imout)
  {
    yaRC return_value;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, IImage*> dispatch_object(return_value, imin, imout);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        exponential_t< Image<yaUINT8>,    Image<yaF_double> >,
        exponential_t< Image<yaF_double>,    Image<yaF_double> >,
        exponential_t< Image<yaF_simple>,    Image<yaF_simple> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }
  
  yaRC power(const IImage *imin, const variant& var, IImage *imout)
  {
    yaRC return_value;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const variant&, IImage*> dispatch_object(return_value, imin, var, imout);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        power_t< Image<yaUINT8>,    Image<yaUINT8> >,
        power_t< Image<yaUINT8>,    Image<yaF_double> >,
        power_t< Image<yaF_double>, Image<yaF_double> >,
        power_t< Image<yaF_simple>, Image<yaF_simple> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC square(const IImage *imin, IImage *imout)
  {
    yaRC return_value;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, IImage*> dispatch_object(return_value, imin, imout);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        square_t< Image<yaUINT8>,    Image<yaUINT8> >,
        square_t< Image<yaUINT8>,    Image<yaUINT16> >,
        square_t< Image<yaUINT8>,    Image<yaF_double> >,
        square_t< Image<yaF_double>,    Image<yaF_double> >,
        square_t< Image<yaF_simple>,    Image<yaF_simple> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }

  yaRC square_root(const IImage *imin, IImage *imout)
  {
    yaRC return_value;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, IImage*> dispatch_object(return_value, imin, imout);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        square_root_t< Image<yaUINT8>,    Image<yaF_double> >,
        square_root_t< Image<yaF_double>,    Image<yaF_double> >,
        square_root_t< Image<yaF_simple>,    Image<yaF_simple> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;

  }

  template <class im_t>
  yaRC patch_for_visual(im_t& im, double mean, double std_dev)
  {
    return generate_gaussian_random_t(im, mean, std_dev);
  }


  yaRC generate_gaussian_random(IImage* imin, double mean, double std_deviation)
  {
    yaRC return_value;
    
    if(imin == 0)
      return yaRC_E_null_pointer;

    
    yayi::dispatcher::s_dispatcher<yaRC, IImage*,yaF_double,yaF_double> dispatch_object(return_value, imin, mean, std_deviation);
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        //generate_gaussian_random_t< Image<yaF_simple> >,
        //generate_gaussian_random_t< Image<yaF_double> >
        patch_for_visual< Image<yaF_simple> >,
        patch_for_visual< Image<yaF_double> >
        )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }


}
