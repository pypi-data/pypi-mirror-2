/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiPixelProcessing/image_logics.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_logics_t.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{

  yaRC image_logical_not(const IImage* imin, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        logical_not_images_t< Image<yaUINT8>,     Image<yaUINT8> >,
        logical_not_images_t< Image<yaUINT16>,    Image<yaUINT16> >,
        logical_not_images_t< Image<yaUINT32>,    Image<yaUINT32> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

}
