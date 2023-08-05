/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_MIN_MAX_T_HPP__
#define YAYI_MEASUREMENTS_MIN_MAX_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
//#include <boost/limits.hpp>
#include <boost/numeric/conversion/bounds.hpp>

#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>


namespace yayi
{
  namespace measurements
  {
    
    template <class T>
    struct s_meas_min_max: public std::unary_function<T, void>
    {
      typedef std::pair<T, T> result_type;

      T min_, max_;
      s_meas_min_max() : min_(boost::numeric::bounds<T>::highest()), max_(boost::numeric::bounds<T>::lowest()) {}
      void operator()(const T& v) throw()
      {
        min_ = std::min(v, min_);
        max_ = std::max(v, max_);
      }

      result_type result() const
      {
        return std::make_pair(min_, max_);
      }

      void clear_result() throw()
      {
        min_ = boost::numeric::bounds<T>::highest();
        max_ = boost::numeric::bounds<T>::lowest();
      }     
    };
    
    
    template <class image_in_t>
    yaRC image_meas_min_max_t(const image_in_t& im, variant& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_min_max<out_t> operator_type;
    
      s_apply_unary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the min/max: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }
     
    
  }
}


#endif /* YAYI_MEASUREMENTS_MIN_MAX_T_HPP__ */
