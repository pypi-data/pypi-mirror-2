/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <iostream>
#include <Yayi/core/yayiPixelProcessing/image_color_process.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_color_process_hls_T.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi {

  yaRC RGB_to_HLS_l1(const IImage* imin, IImage* imout) {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
      
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_RGB_to_HLSl1_t< Image<pixel8u_3>, Image<pixelFs_3> >, 
        color_RGB_to_HLSl1_t< Image<pixel8u_3>, Image<pixelFd_3> >/*,
        color_RGB_to_HLSl1_t< Image<pixelFs_3>, Image<pixelFs_3> >, // non sense
        color_RGB_to_HLSl1_t< Image<pixelFd_3>, Image<pixelFd_3> >*/
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }


  yaRC HLS_l1_to_RGB(const IImage* imin, IImage* imout) {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_HLSl1_to_RGB_t< Image<pixelFs_3>, Image<pixel8u_3> >,
        color_HLSl1_to_RGB_t< Image<pixelFd_3>, Image<pixel8u_3> >/*,
        color_HLSl1_to_RGB_t< Image<pixelFs_3>, Image<pixelFs_3> >,
        color_HLSl1_to_RGB_t< Image<pixelFd_3>, Image<pixelFd_3> >*/
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }

}
