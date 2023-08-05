/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef MEASUREMENTS_MEAN_VARIANCE_T_HPP__
#define MEASUREMENTS_MEAN_VARIANCE_T_HPP__


#include <boost/call_traits.hpp>
#include <functional>
#include <boost/numeric/conversion/bounds.hpp>
#include <Yayi/core/yayiCommon/common_histogram.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <Yayi/core/yayiMeasurements/include/measurements_t.hpp>

// for the identity functor (does it exist in stl or boost ?)
#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>

namespace yayi
{
  namespace measurements
  {
    
    //! Simple functor for computing the mean as a result of the "result" method. 
    template <class T, class R = typename s_sum_supertype<T>::type>
    struct s_meas_mean: public std::unary_function<T, void>
    {
      typedef typename s_sum_supertype<T>::type acc_t;
      typedef R result_type;
      
      acc_t acc;
      offset count;
      
      s_meas_mean() : acc(0.), count(0) {}
      void operator()(const T& v) throw()
      {
        count++;
        acc += v;
      }
      
      result_type result() const throw()
      {
        return static_cast<result_type>(acc / count);
      }
      
      void clear_result() throw()
      {
        acc  = 0.;
        count =0 ;
      }      
    };


    //! Simple functor for computing the mean for circular data, as a result of the "result" method. 
    template <class T>
    struct s_meas_circular_mean_and_concentration: public std::unary_function<T, void>
    {
      typedef std::complex<typename s_sum_supertype<T>::type> acc_t;
      typedef acc_t result_type;
      
      acc_t acc;
      offset count;
      
      s_meas_circular_mean_and_concentration() : acc(0.), count(0) {}
      void operator()(const T& v) throw()
      {
        count++;
        acc += std::polar(1, v);
      }
      
      acc_t result() const throw()
      {
        return std::arg(acc / count);
      }
      
      void clear_result() throw()
      {
        acc  = 0.;
        count =0 ;
      }
    };


    //! Specializing of s_meas_circular_mean_and_concentration for pixel3. The circular dimension on which the mean is computer is the first one (index 0)
    template <class U>
    struct s_meas_circular_mean_and_concentration< s_compound_pixel_t<U, mpl::int_<3> > >: 
      public std::unary_function<s_compound_pixel_t<U, mpl::int_<3> >, void>
    {
      typedef s_compound_pixel_t<U, mpl::int_<3> > T;
      typedef std::complex<typename s_sum_supertype<U>::type> acc_t;
      typedef acc_t result_type;
      
      acc_t acc;
      offset count;
      
      s_meas_circular_mean_and_concentration() : acc(0.), count(0) {}
      void operator()(const T& v) throw()
      {
        count++;
        acc += std::polar(U(1), v[0]);
      }
      
      acc_t result() const throw()
      {
        return acc / typename acc_t::value_type(count);
      }
      
      void clear_result() throw()
      {
        acc  = 0.;
        count =0 ;
      }
    };


    //! Weighted version of s_meas_mean_circular by the second channel
    template <class U, class op_weight_t = s_copy<typename U::value_type, typename U::value_type> >
    struct s_meas_weighted_circular_mean_and_concentration;

    //! Specializing of s_meas_weighted_circular_mean_and_concentration for pixel3. 
    //! The circular dimension on which the mean is computer is the first one (index 0). The weight parameter is given by the third channel (index 3).
    //! The weight function is given by the functor type op_weight_t (should return a type compatible with U).
    template <class U, class op_weight_t>
    struct s_meas_weighted_circular_mean_and_concentration< s_compound_pixel_t<U, mpl::int_<3> >, op_weight_t >: 
      public std::unary_function<s_compound_pixel_t<U, mpl::int_<3> >, void>
    {
      typedef s_compound_pixel_t<U, mpl::int_<3> > T;
      typedef std::complex<typename s_sum_supertype<U>::type> acc_t;
      typedef acc_t result_type;
      
      acc_t acc, acc_w;
      op_weight_t op;
      s_meas_weighted_circular_mean_and_concentration() : acc(0.), acc_w(0) {}
      void operator()(const T& v) throw()
      {
        const U vv = op(v[2]);
        acc_w += vv;
        acc += std::polar(vv, v[0]);
      }
      
      acc_t result() const throw()
      {
        return std::arg(acc / acc_w);
      }
      
      void clear_result() throw()
      {
        acc  = 0.;
        acc_w =0 ;
      }
    };


    
    
    //! Computes the mean over the image
    template <class image_in_t>
    yaRC image_meas_mean_t(
      const image_in_t& im, 
      typename s_sum_supertype<typename image_in_t::pixel_type>::type& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_mean<out_t> operator_type;
    
      s_apply_unary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the mean: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }


    //! Computes the mean on each region of the image
    template <class image_in_t, class image_regions_t>
    yaRC image_meas_mean_on_region_t(
      const image_in_t& im, 
      const image_regions_t& regions, 
      std::map<
        typename image_regions_t::pixel_type, 
        typename s_sum_supertype<typename image_in_t::pixel_type>::type > & out)
    {
      typedef s_meas_mean<typename image_in_t::pixel_type> region_operator_type;
      typedef s_measurement_on_regions<
        typename image_in_t::pixel_type,
        typename image_regions_t::pixel_type,
        region_operator_type> operator_type;
    
      s_apply_binary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, regions, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the mean on regions: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }


    //! Computes the circular mean on each region of the image (circular channel is H/first channel)
    template <class image_in_t, class image_regions_t>
    yaRC image_meas_circular_mean_and_concentration_on_region_t(
      const image_in_t& im, 
      const image_regions_t& regions, 
      std::map<
        typename image_regions_t::pixel_type, 
        typename s_meas_circular_mean_and_concentration<typename image_in_t::pixel_type>::result_type
      > & out)
    {
      typedef s_meas_circular_mean_and_concentration<typename image_in_t::pixel_type> region_operator_type;
      typedef s_measurement_on_regions<
        typename image_in_t::pixel_type,
        typename image_regions_t::pixel_type,
        region_operator_type> operator_type;
    
      s_apply_binary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, regions, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the mean (circular) on regions: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }

    //! Computes the linearly weighted circular mean on each region of the image (circular channel is H/first channel, weight channel is S/third)
    template <class image_in_t, class image_regions_t>
    yaRC image_meas_weighted_circular_mean_and_concentration_on_region_t(
      const image_in_t& im, 
      const image_regions_t& regions, 
      std::map<
        typename image_regions_t::pixel_type, 
        typename s_meas_weighted_circular_mean_and_concentration<typename image_in_t::pixel_type>::result_type
      > & out)
    {
      typedef s_meas_weighted_circular_mean_and_concentration<typename image_in_t::pixel_type> region_operator_type;
      typedef s_measurement_on_regions<
        typename image_in_t::pixel_type,
        typename image_regions_t::pixel_type,
        region_operator_type> operator_type;
    
      s_apply_binary_operator op_processor;
    
      operator_type op;
      yaRC res = op_processor(im, regions, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the mean (circular) on regions: " << res);
        return res;
      }
      
      out = op.result();
      return yaRC_ok;
    }
    
    
    

     
    
  }
}



#endif /* MEASUREMENTS_MEAN_VARIANCE_T_HPP__ */

