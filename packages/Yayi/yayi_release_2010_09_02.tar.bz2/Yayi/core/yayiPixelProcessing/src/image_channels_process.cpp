/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <Yayi/core/yayiPixelProcessing/include/image_channels_process_T.hpp>
#include <Yayi/core/yayiPixelProcessing/image_channels_process.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi {

  yaRC copy_one_channel_to_another(const IImage* imin, const unsigned int channel_input, const unsigned int channel_output, IImage* imout) {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const unsigned int, 
      const unsigned int, 
      IImage*> dispatch_object(return_value, imin, channel_input, channel_output, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        copy_one_channel_image_into_another_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > >,                   Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > >,
        copy_one_channel_image_into_another_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > >,                   Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > > >,
        copy_one_channel_image_into_another_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> >, s_coordinate<3> >,  Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > , s_coordinate<3> > >,
        copy_one_channel_image_into_another_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> >, s_coordinate<3> >,  Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > , s_coordinate<3> > >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;
  
  }




  yaRC copy_one_channel(const IImage* imin, const unsigned int channel_input, IImage* imout) {
  
    yaRC return_value;
    
    //std::cout << "in channel input = " << channel_input << std::endl;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const unsigned int, 
      IImage*> dispatch_object(return_value, imin, channel_input, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > >,                   Image<yaUINT8> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > >,                   Image<yaUINT8> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> >, s_coordinate<3> >,  Image<yaUINT8, s_coordinate<3> > >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> >, s_coordinate<3> >,  Image<yaUINT8, s_coordinate<3> > >,

        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > >,                   Image<yaF_simple> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<4> > >,                   Image<yaF_simple> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> >, s_coordinate<3> >,  Image<yaF_simple, s_coordinate<3> > >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<4> >, s_coordinate<3> >,  Image<yaF_simple, s_coordinate<3> > >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    
    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > >,                   Image<yaF_double> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<4> > >,                   Image<yaF_double> >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> >, s_coordinate<3> >,  Image<yaF_double, s_coordinate<3> > >,
        copy_one_channel_image_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<4> >, s_coordinate<3> >,  Image<yaF_double, s_coordinate<3> > >
      )
      );      

    if(res == yaRC_ok)
      return return_value;
    return res;
  
  }


  yaRC copy_to_channel(const IImage* imin, const unsigned int channel_output, IImage* imout) {
  
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const unsigned int, 
      IImage*> dispatch_object(return_value, imin, channel_output, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        copy_into_channel_image_t< Image<yaUINT8>,                    Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > >,
        copy_into_channel_image_t< Image<yaUINT8>,                    Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > > >,
        copy_into_channel_image_t< Image<yaUINT8, s_coordinate<3> >,  Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> >, s_coordinate<3> > >,
        copy_into_channel_image_t< Image<yaUINT8, s_coordinate<3> >,  Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> >, s_coordinate<3> > >,

        copy_into_channel_image_t< Image<yaF_simple>,                   Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > >,
        copy_into_channel_image_t< Image<yaF_simple>,                   Image<s_compound_pixel_t<yaF_simple, mpl::int_<4> > > >,
        copy_into_channel_image_t< Image<yaF_simple, s_coordinate<3> >, Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> >, s_coordinate<3> > >,
        copy_into_channel_image_t< Image<yaF_simple, s_coordinate<3> >, Image<s_compound_pixel_t<yaF_simple, mpl::int_<4> >, s_coordinate<3> > >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    
    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        copy_into_channel_image_t< Image<yaF_double>,                   Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > > >,
        copy_into_channel_image_t< Image<yaF_double>,                   Image<s_compound_pixel_t<yaF_double, mpl::int_<4> > > >,
        copy_into_channel_image_t< Image<yaF_double, s_coordinate<3> >, Image<s_compound_pixel_t<yaF_double, mpl::int_<3> >, s_coordinate<3> > >,
        copy_into_channel_image_t< Image<yaF_double, s_coordinate<3> >, Image<s_compound_pixel_t<yaF_double, mpl::int_<4> >, s_coordinate<3> > >
      )
      );

    if(res == yaRC_ok)
      return return_value;
    return res;
  
  }

  yaRC copy_split_channels(const IImage* imin, IImage* imout1, IImage* imout2, IImage* imout3) {
  
    yaRC return_value;
    
    //std::cout << "in channel input = " << channel_input << std::endl;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*,IImage*,IImage*> dispatch_object(return_value, imin, imout1, imout2, imout3);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        channels_split_t< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > >,    Image<yaUINT8> >,
        channels_split_t< Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > >, Image<yaF_simple> >,
        channels_split_t< Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > >, Image<yaF_double> >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  
  }


  yaRC copy_compose_channels(const IImage* imin1, const IImage* imin2, const IImage* imin3, IImage* imout) {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, const IImage*, const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imin3, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        channels_compose_t< Image<yaUINT8>,     Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > >,
        channels_compose_t< Image<yaF_simple>,  Image<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > >,
        channels_compose_t< Image<yaF_double>,  Image<s_compound_pixel_t<yaF_double, mpl::int_<3> > > >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  
  }


}

