/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <Yayi/core/yayiPixelProcessing/image_copy.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi
{

  yaRC copy(const IImage* imin, IImage* imout)
  {
    yaRC return_value, res;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, IImage*> dispatch_object(return_value, imin, imout);
    
    switch(imin->DynamicType().c_type)
    {
    
    case type::c_scalar:
    {
    
      // 2D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_t< Image<yaUINT8>, Image<yaUINT8 > >,
          copy_image_t< Image<yaUINT8>, Image<yaUINT16> >,
          copy_image_t< Image<yaUINT8>, Image<yaUINT32> >,
          copy_image_t< Image<yaUINT8>, Image<yaUINT64> >,

          copy_image_t< Image<yaUINT8>, Image<yaINT8 > >,
          copy_image_t< Image<yaUINT8>, Image<yaINT16> >,
          copy_image_t< Image<yaUINT8>, Image<yaINT32> >,
          copy_image_t< Image<yaUINT8>, Image<yaINT64> >,

          copy_image_t< Image<yaUINT8>, Image<yaF_simple> >,
          copy_image_t< Image<yaUINT8>, Image<yaF_double> >));


      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}
        
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_t< Image<yaUINT16  >, Image<yaUINT16  > >,
          copy_image_t< Image<yaUINT32  >, Image<yaUINT32  > >,
          copy_image_t< Image<yaF_simple>, Image<yaF_simple> >,
          copy_image_t< Image<yaF_double>, Image<yaF_double> >,
          
          copy_image_t< Image<yaUINT16  >, Image<yaUINT8   > >,
          copy_image_t< Image<yaUINT32  >, Image<yaUINT8   > >,

          copy_image_t< Image<yaF_simple>, Image<yaUINT8   > >,
          copy_image_t< Image<yaF_simple>, Image<yaUINT16  > >,
          copy_image_t< Image<yaF_double>, Image<yaUINT8   > >
          ));

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}


      // 3D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT8,  s_coordinate<3> > >,
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >,
          //copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT64, s_coordinate<3> > >,

          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT8,   s_coordinate<3> > >,
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT16,  s_coordinate<3> > >,
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT32,  s_coordinate<3> > >,
          //copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT64,  s_coordinate<3> > >,

          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> > >,
          copy_image_t< Image<yaUINT8, s_coordinate<3> >, Image<yaF_double, s_coordinate<3> > >,
          copy_image_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> > >,
          copy_image_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> > >
        ));

      
      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}


     // 3D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_t< Image<yaF_simple, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> > >,
          copy_image_t< Image<yaF_double, s_coordinate<3> >, Image<yaF_double, s_coordinate<3> > >,
          copy_image_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >,
          copy_image_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >
        ));

      if(res == yaRC_E_not_implemented) {return res;}
      return return_value;
    }
    
    case type::c_3:
    {
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > >, Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > >,
          copy_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > >, Image<s_compound_pixel_t<yaUINT16,   mpl::int_<3> > > >,

          copy_image_t< Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > >, Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > >,
          copy_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > >, Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > >,
          copy_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > >, Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > >,
          
          copy_image_t< Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > >, Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > > >,
          copy_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > >, Image<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > >,
          copy_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > >, Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > > >
          ));

      if(res == yaRC_ok) return return_value;
      return res;
    }    
    
    default:
      return yaRC_E_not_implemented;
    }


  }





}

