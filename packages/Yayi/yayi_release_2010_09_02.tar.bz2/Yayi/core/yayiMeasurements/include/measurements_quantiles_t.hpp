/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_QUANTILES_T_HPP__
#define YAYI_MEASUREMENTS_QUANTILES_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/median.hpp>
#include <boost/numeric/conversion/bounds.hpp>

#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>


namespace yayi
{
  namespace measurements
  {
    namespace bacc = boost::accumulators;

    template <class T, class result_type_t = T>
    struct s_meas_median: public std::unary_function<T, void>
    {
      typedef bacc::accumulator_set<T, bacc::stats<bacc::tag::median(bacc::with_p_square_quantile) > > acc_t;
      acc_t acc;

      typedef result_type_t result_type;
      s_meas_median() {}
      void operator()(const T& v) throw()
      {
        acc(v);
      }
      
      result_type const result()
      {
        return static_cast<result_type>(bacc::median(acc));
      }

      void clear_result()
      {
        acc = acc_t();
      }


    };
    
    
    template <class image_in_t>
    yaRC image_meas_median_t(const image_in_t& im, variant& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_median<out_t> operator_type;
    
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


#endif /* YAYI_MEASUREMENTS_QUANTILES_T_HPP__ */
