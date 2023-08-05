/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_CORE_GRAPH_DISPATCH_HPP__
#define YAYI_COMMON_CORE_GRAPH_DISPATCH_HPP__


/*!@file
 * Dispatcher for variants
 */

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/include/common_graph.hpp>

namespace yayi 
{

  namespace dispatcher
  {
    template <class I, class T, bool B_WRITE_ONLY> struct s_conversion_policy;
    template <class I, class T, bool B_WRITE_ONLY> struct s_runtime_conversion;
    
    struct s_convertible_runtime_time;
    
    template <class V, class E, bool B, bool B_WRITE_ONLY>
    struct s_conversion_policy<yayi::IGraph&, yayi::s_graph<V,E,B>&, B_WRITE_ONLY >
    {
      typedef s_convertible_runtime_time type;
    };
    
    template <class V, class E, bool B>
    struct s_runtime_conversion<yayi::IGraph&, yayi::s_graph<V,E,B>&, false >
    {
      typedef boost::true_type  type;
      typedef yayi::IGraph      graph_t;
      typedef boost::true_type  need_holder_tag;
      
      typedef s_graph<V,E,B>    result_t;
     
      static bool is_convertible(const graph_t& r_) throw()
      {
        BOOST_STATIC_ASSERT((s_variant_type_support<V>::type::value && s_variant_type_support<E>::type::value));
        return s_variant_type_support<V>::type::value && s_variant_type_support<E>::type::value;
      }
      
      static const result_t convert(const graph_t& r_)
      {
        return result_t(r_);
      }
      static result_t convert(graph_t& r_)
      {
        return result_t(r_);
      }
    };
    
    template <class V, class E, bool B>
    struct s_runtime_conversion<yayi::IGraph&, yayi::s_graph<V,E,B>&, true > : s_runtime_conversion<yayi::IGraph&, yayi::s_graph<V,E,B>&, false >
    {
      typedef typename 
        mpl::and_<
          typename s_variant_type_support<V>::type, 
          typename s_variant_type_support<E>::type
        >::type type;
      typedef yayi::IGraph      graph_t;
      typedef boost::true_type  need_holder_tag;
      typedef s_graph<V,E,B>    result_t;
     
      static bool is_convertible(const graph_t& r_) throw()
      {
        return s_variant_type_support<V>::type::value && s_variant_type_support<E>::type::value;
      }
      static result_t convert(graph_t& r_)
      {
        try
        {
          result_t G;
          G = r_;
          return G;
        }
        catch(errors::yaException & )
        {
          return result_t();
        }
      }
    };   
  }
}

#endif /* YAYI_COMMON_CORE_GRAPH_DISPATCH_HPP__ */
