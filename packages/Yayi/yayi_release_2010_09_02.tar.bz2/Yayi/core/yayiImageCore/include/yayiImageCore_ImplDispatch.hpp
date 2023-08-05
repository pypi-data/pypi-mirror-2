/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_IMAGE_CORE_IMPLDISPATCH_HPP__
#define YAYI_IMAGE_CORE_IMPLDISPATCH_HPP__

#include <Yayi/core/yayiCommon/common_variant.hpp>
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>


/*!@file
 * Dispatcher for images
 */

namespace yayi 
{


  namespace dispatcher
  {
    template <class I, class T, bool B_WRITE_ONLY> struct s_conversion_policy;
    template <class I, class T, bool B_WRITE_ONLY> struct s_runtime_conversion;
    
    struct s_convertible_runtime_time;
    
    template <class T, class coordinate_type, class allocator_type, bool B>
    struct s_conversion_policy<IImage*, Image<T, coordinate_type, allocator_type>&, B >
    {
      typedef s_convertible_runtime_time type;
    };
    
    template <class T, class coordinate_type, class allocator_type, bool B>
    struct s_runtime_conversion<IImage*, Image<T, coordinate_type, allocator_type>&, B >
    {
      typedef boost::true_type type;
      
      typedef Image<T, coordinate_type, allocator_type> image_type;
      typedef IImage                                    image_type_interface;
      
      
      typedef typename remove_const<typename remove_reference<image_type>::type>::type    T_without_const_ref;
      typedef typename add_reference<typename add_const<T_without_const_ref>::type>::type T_const_ref;
      
      static bool is_convertible(const image_type_interface* r_) YAYI_THROW_DEBUG_ONLY__
      {
        YAYI_DBG_DISPATCH("is_convertible to: " << std::endl << "\t" << std::string(image_type::Type()) << std::endl);
        YAYI_DBG_DISPATCH("\t from: " << std::string(r_->DynamicType()) << std::endl);
        YAYI_DBG_DISPATCH("\t bool=" << (r_->DynamicType() == image_type::Type()) << std::endl);
        if(r_ == 0) 
          return false;
        DEBUG_ASSERT(
         !(((r_->DynamicType() == image_type::Type()) && (r_->GetDimension() == coordinate_type::static_dimensions)) ^ (dynamic_cast<const image_type*>(r_) != 0)), 
         "type corresponds but not dynamic cast ??"
         "\n\tinput image type : " + errors::demangle(typeid(*r_).name()) + " //// " + typeid(*r_).name() + 
         "\n\ttarget image type : " + errors::demangle(typeid(image_type).name()) + " //// " + typeid(image_type).name() +
         "\n\tr_->DynamicType() == image_type::Type() : " + (r_->DynamicType() == image_type::Type() ? "true":"false") +
         "\n\tr_->GetDimension() == coordinate_type::static_dimensions : " + (r_->GetDimension() == coordinate_type::static_dimensions ? "true":"false") +
         "\n\tdynamic_cast<const image_type*>(r_) != 0 : " + (dynamic_cast<const image_type*>(r_) != 0 ? "true":"false")
         );
        return (r_->DynamicType() == image_type::Type()) && (r_->GetDimension() == coordinate_type::static_dimensions);
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
  }
  
} // namespace yayi

#endif /*YAYI_IMAGE_CORE_IMPLDISPATCH_HPP__*/

