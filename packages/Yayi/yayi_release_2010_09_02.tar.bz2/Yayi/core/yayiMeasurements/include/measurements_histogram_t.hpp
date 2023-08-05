/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__
#define YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
#include <boost/numeric/conversion/bounds.hpp>
#include <Yayi/core/yayiCommon/common_histogram.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <Yayi/core/yayiMeasurements/include/measurements_t.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>

namespace yayi
{
  namespace measurements
  {
    
    template <class T>
    struct s_meas_histogram: public std::unary_function<T, void>
    {
      typedef s_histogram_t<T> result_type;
      result_type h;
      s_meas_histogram() : h() {}
      void operator()(const T& v) throw()
      {
        h[v]++;
      }
      
      result_type const& result() const
      {
        return h;
      }
      
      void clear_result() throw()
      {
        h.clear();
      }      
    };


    
    
    template <class image_in_t>
    yaRC image_meas_histogram_t(const image_in_t& im, s_histogram_t<typename image_in_t::pixel_type>& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_histogram<out_t> operator_type;
    
      s_apply_unary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the histogram: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }


    template <class image_in_t, class image_regions_t>
    yaRC image_meas_histogram_on_region_t(
      const image_in_t& im, 
      const image_regions_t& regions, 
      std::map<typename image_regions_t::pixel_type, s_histogram_t<typename image_in_t::pixel_type> > & out)
    {
      typedef s_meas_histogram<typename image_in_t::pixel_type> region_operator_type;
      typedef s_measurement_on_regions<
        typename image_in_t::pixel_type,
        typename image_regions_t::pixel_type,
        region_operator_type> operator_type;
    
      s_apply_binary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, regions, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the histogram: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }
     
    
  }
}


#endif /* YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__ */
