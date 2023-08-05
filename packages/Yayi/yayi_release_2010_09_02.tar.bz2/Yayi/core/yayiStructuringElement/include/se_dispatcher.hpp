/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_SE_IMPLDISPATCH_HPP__
#define YAYI_SE_IMPLDISPATCH_HPP__


#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>

/*!@file
 * Dispatcher for structuring elements
 */

namespace yayi 
{


  namespace dispatcher
  {
    
    template <class coordinate_type, class element_t, class se_specific_>
    struct s_conversion_policy<se::IStructuringElement*, se::s_neighborlist_se_hexa_x<coordinate_type, element_t, se_specific_>&, false >
    {
      typedef s_convertible_dynamic_cast type;
    };
    
    template <class coordinate_type, class element_t, class se_specific_>
    struct s_conversion_policy<se::IStructuringElement*, se::s_neighborlist_se<coordinate_type, element_t, se_specific_>&, false >
    {
      typedef s_convertible_dynamic_cast type;
    };
        
    #if 0
    template <class T, class coordinate_type, class allocator_type>
    struct s_runtime_conversion<IImage*, Image<T, coordinate_type, allocator_type>&, false >
    {
      typedef boost::true_type type;
      
      typedef Image<T, coordinate_type, allocator_type> image_type;
      typedef IImage                                    image_type_interface;
      
      
      typedef typename remove_const<typename remove_reference<image_type>::type>::type    T_without_const_ref;
      typedef typename add_reference<typename add_const<T_without_const_ref>::type>::type T_const_ref;
      
      static bool is_convertible(const image_type_interface* r_) throw()
      {
        if(r_ == 0) 
          return false;
        DEBUG_ASSERT(r_->DynamicType() == image_type::Type() && dynamic_cast<const image_type*>(r_) != 0, "type corresponds but not dynamic cast ??");
        return r_->DynamicType() == image_type::Type();
      }
      
      static const image_type& convert(const image_type_interface* r_)
      {
        return dynamic_cast<const image_type&>(*r_);
      }
      static image_type& convert(image_type_interface* r_)
      {
        return dynamic_cast<image_type&>(*r_);
      }
    };
    #endif
  }
  
} // namespace yayi

#endif /*YAYI_SE_IMPLDISPATCH_HPP__*/

