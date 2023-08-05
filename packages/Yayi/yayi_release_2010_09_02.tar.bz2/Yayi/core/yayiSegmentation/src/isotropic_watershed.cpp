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
#include <ios>
#include <Yayi/core/yayiSegmentation/yayiSegmentation.hpp>
#include <Yayi/core/yayiSegmentation/include/isotropic_watershed_t.hpp>

#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>

namespace yayi { namespace segmentation {

  yaRC isotropic_watershed(const IImage * imin, const se::IStructuringElement* se, IImage* imout)
  {
    if(imin == 0 || imout == 0 || se == 0)
      return yaRC_E_null_pointer;  

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const se::IStructuringElement*, 
      IImage*> dispatch_object(return_value, imin, se, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        isotropic_watershed_t< Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image<yaUINT16> >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;      


  }


  yaRC isotropic_watershed(const IImage * imin, const IImage * imseeds, const se::IStructuringElement* se, IImage* imout)
  {
    if(imin == 0 || imseeds == 0 || imout == 0 || se == 0)
      return yaRC_E_null_pointer;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      const se::IStructuringElement*, 
      IImage*> dispatch_object(return_value, imin, imseeds, se, imout);


    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        isotropic_seeded_watershed_t< Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok) return return_value;
    return res;      

  }

}}
