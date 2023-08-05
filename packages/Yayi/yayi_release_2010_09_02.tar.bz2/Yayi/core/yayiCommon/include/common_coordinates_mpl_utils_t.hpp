/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_COORDINATES_UTILS_T_HPP__
#define YAYI_COMMON_COORDINATES_UTILS_T_HPP__

/*!@file
 * Utility structure for initializing the coordinates from template sequences,
 * such as mpl sequences (vectors)
 */

#include <Yayi/core/yayiCommon/common_coordinates.hpp>

#include <boost/mpl/vector_c.hpp>
#include <boost/mpl/at.hpp>
#include <boost/mpl/range_c.hpp>
#include <boost/mpl/vector.hpp>
#include <boost/mpl/zip_view.hpp>
#include <boost/mpl/size.hpp>

namespace yayi
{
  template <class Seq>
  struct from_mpl_to_coordinate
  {
    typedef mpl::size<Seq> vector_lenght_t;
    typedef yayi::s_coordinate<vector_lenght_t::value> result_type;
    
    struct assign_value_to_dimension
    {
      result_type &res;
      assign_value_to_dimension(result_type& res_) : res(res_){}
      template< typename U > void operator()(U& )
      {
        res[mpl::at_c<U, 0>::type::value] = mpl::at_c<U, 1>::type::value;
      }
    };
    
    static result_type get()
    {
      typedef mpl::range_c<int, 0, vector_lenght_t::value> range_t;
      typedef mpl::zip_view< mpl::vector<range_t, Seq > > zipped_type;
      result_type res;
      mpl::for_each<zipped_type>(assign_value_to_dimension(res));
      return res;
    }
    
    /*
    static const result_type& result()
    {
      static const result_type res = init();
      return res;
    }*/
  };
  
}

#endif /* YAYI_COMMON_COORDINATES_UTILS_T_HPP__ */
