/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiPixelProcessing/image_constant.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_variantDispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi
{

  yaRC constant(IImage* imin, const variant& value)
  {
    using namespace dispatcher;
    BOOST_MPL_ASSERT((s_convertor_wrapper<IImage*, Image<yaUINT8, s_coordinate<2>, s_default_image_allocator<yaUINT8, s_coordinate<2> > >& >::convertor_type::type));

    yaRC return_value, res;
    
    if(imin == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const variant&, IImage*> dispatch_object(return_value, value, imin);
    
    //yaRC res = dispatch_object(constant_image_t< Image<yaUINT8>, yaUINT8 >);

    switch(imin->DynamicType().c_type)
    {
    
    case type::c_scalar:
    {
    
      // 2D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          constant_image_t< Image<yaUINT8 > >,
          constant_image_t< Image<yaUINT16> >,
          constant_image_t< Image<yaUINT32> >,
          constant_image_t< Image<yaUINT64> >,

          constant_image_t< Image<yaINT8 > >,
          constant_image_t< Image<yaINT16> >,
          constant_image_t< Image<yaINT32> >,
          constant_image_t< Image<yaINT64> >,

          constant_image_t< Image<yaF_simple> >,
          constant_image_t< Image<yaF_double> >));

      if(res == yaRC_ok) return return_value;

      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          constant_image_t< Image<yaUINT8 , s_coordinate<3> > >,
          constant_image_t< Image<yaUINT16, s_coordinate<3> > >,
          constant_image_t< Image<yaUINT32, s_coordinate<3> > >,
          constant_image_t< Image<yaUINT64, s_coordinate<3> > >,

          constant_image_t< Image<yaINT8 , s_coordinate<3> > >,
          constant_image_t< Image<yaINT16, s_coordinate<3> > >,
          constant_image_t< Image<yaINT32, s_coordinate<3> > >,
          constant_image_t< Image<yaINT64, s_coordinate<3> > >,

          constant_image_t< Image<yaF_simple, s_coordinate<3> > >,
          constant_image_t< Image<yaF_double, s_coordinate<3> > >));

      if(res == yaRC_ok) return return_value;
      return res;
    }
    
    case type::c_3:
    {
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          constant_image_t< Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > >,
          constant_image_t< Image<s_compound_pixel_t<yaUINT16,   mpl::int_<3> > > >,
          constant_image_t< Image<s_compound_pixel_t<yaINT8,     mpl::int_<3> > > >,
          constant_image_t< Image<s_compound_pixel_t<yaINT16,    mpl::int_<3> > > >,
          constant_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > >,
          constant_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > > >
          ));

      if(res == yaRC_ok) return return_value;
      return res;
    }    
    
    default:
      return yaRC_E_not_implemented;
    }

  }





}

