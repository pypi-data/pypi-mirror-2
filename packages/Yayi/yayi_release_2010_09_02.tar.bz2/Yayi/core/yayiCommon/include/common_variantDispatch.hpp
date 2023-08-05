/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_CORE_VARIANT_DISPATCH_HPP__
#define YAYI_COMMON_CORE_VARIANT_DISPATCH_HPP__


/*!@file
 * Dispatcher for variants
 */

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>


namespace yayi 
{

  namespace dispatcher
  {
    template <class I, class T, bool B_WRITE_ONLY> struct s_conversion_policy;
    template <class I, class T, bool B_WRITE_ONLY> struct s_runtime_conversion;
    
    struct s_convertible_runtime_time;
    
    template <class T, bool B_WRITE_ONLY>
    struct s_conversion_policy<yayi::variant&, T, B_WRITE_ONLY >
    {
      typedef s_convertible_runtime_time type;
    };
    

    //! Specializing of s_runtime_conversion for special case of variant "interface" type, input/output version
    template <class T>
    struct s_runtime_conversion<yayi::variant&, T, false >
    {
      typedef typename remove_reference<T>::type T_noref;
      typedef typename s_variant_type_support<T_noref>::type type;
      typedef yayi::variant variant_t;
      typedef boost::true_type need_holder_tag;
      
      
     
      static bool is_convertible(const variant_t& r_) throw()
      {
        // this is ok for unitialized ? For my opinion, we should distinguish const and non const outputs
        //if(r_.element_type == type_undefined)
        //  return true;
        
        // This test is a little bit costy, but it allows to rely on one unique implementation
        // rather than doing an exhaustive inventory of the allowed transformations inside a structure
        
        // Possible optimization: we can put a static std::set or std::map with r_.element_type as key (and bool as value for std::map)
        // but we should take care of the concurrent accesses.
        try 
        {
          /*T_noref const val = */r_.operator T_noref();
          return true;
        }
        catch(errors::yaException& DEBUG_ONLY_VARIABLE(e)) {
          DEBUG_INFO("variant dispatch error: " << e.message());
          return false;
        }
        
      }
      
      static const T_noref convert(const variant_t& r_)
      {
        return r_.operator T_noref();
      }
      static T_noref convert(variant_t& r_)
      {
        return r_.operator T_noref();
      }
    };
    
    //! Specializing of s_runtime_conversion for special case of variant "interface" type, output only version
    template <class T>
    struct s_runtime_conversion<yayi::variant&, T, true > : s_runtime_conversion<yayi::variant&, T, false >
    {
      typedef typename remove_reference<T>::type T_no_ref;
      typedef typename s_variant_type_support<T_no_ref>::type type;
      typedef yayi::variant variant_t;
      typedef boost::true_type need_holder_tag;
      
     
      static bool is_convertible(const variant_t& r_) throw()
      {
        BOOST_STATIC_ASSERT((s_variant_type_support<T_no_ref>::type::value)); // easier to debug
        return s_variant_type_support<T_no_ref>::type::value;
      }
      static T_no_ref convert(variant_t& r_)
      {
        // This is an ugly trick since the variant may be uninitialized (write only)
        try 
        {
          return r_.operator T_no_ref();
        }
        catch(errors::yaException& /*e*/) {
          return T_no_ref();
        }
      }
    };    
    
  }
}

#endif
