/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_MATH_T_HPP__
#define YAYI_PIXEL_IMAGE_MATH_T_HPP__

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>

#include <Yayi/core/yayiImageCore/include/ApplyToImage_zeroary_t.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>

#include <boost/math/distributions/normal.hpp>
#include <boost/random/uniform_01.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/numeric/conversion/bounds.hpp>
#include <boost/numeric/conversion/conversion_traits.hpp>

#include <float.h>


/*!@file
 * This file contains the implementation of several mathematical function (log, power, sqrt, random...)
 */

namespace yayi
{

  template <class U, class V = U>
  struct s_log : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return ::log(u);
    }
  };
  
  template <class V>
  struct s_log<yaUINT8, V> : public std::unary_function<yaUINT8, V>
  {
    typedef yaUINT8 U;
    typedef std::vector<V> value_type;
    static const value_type values;
    
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return values[u];
    }
    
    static value_type generate()
    {
      std::vector<V> out(boost::numeric::bounds<U>::highest() + 1);
      out.push_back(-std::numeric_limits<V>::infinity());
      for(U i = 1; i < boost::numeric::bounds<U>::highest(); i++)
        out.push_back(std::log(float(i)));
      
      return out;
    }
  };
  template <class V>
  typename s_log<yaUINT8, V>::value_type const s_log<yaUINT8, V>::values = s_log<yaUINT8, V>::generate();
  

  //! Computes the logarithm of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC logarithm_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_log<
      typename imin_t::pixel_type, 
      typename imout_t::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imout, op);  
  }
  



  template <class U, class V = U, bool B = false>
  struct s_exp : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,V> t_to_v_traits;

      return static_cast<result_type>(std::exp(typename t_to_v_traits::supertype(u))); // Raffi: check here !
    }
  };
  
  template <class U, class V>
  struct s_exp<U, V, true> : public std::unary_function<U, V>
  {
    typedef std::vector<V> value_type;
    static const value_type values;
    
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return values[u];
    }
    
    static value_type generate()
    {
      value_type out(boost::numeric::bounds<U>::highest() - boost::numeric::bounds<U>::lowest() + 1);
      for(U i = boost::numeric::bounds<U>::lowest(); i < boost::numeric::bounds<U>::highest(); i++)
        out.push_back(::exp(i));
      
      return out;
    }
  };

  template <class U, class V>
  typename s_exp<U, V, true>::value_type const s_exp<U, V, true>::values = s_exp<U, V, true>::generate();
  
  
  
  
  
  //! Computes the exponential of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC exponential_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_exp<
      typename imin_t::pixel_type, 
      typename imout_t::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imout, op);   
  }
  
  
  
  template <class U, class V = U>
  struct s_power : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    double const value;
    s_power(double value_) : value(value_){}
    s_power(const s_power& r_) : value(r_.value){}
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,double> t_to_v_traits;
      return static_cast<result_type>(std::pow(typename t_to_v_traits::supertype(u), value));// Raffi: check here !
    }
  };  

  template <class U, class V>
  struct s_power<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> > > : 
    public std::unary_function<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> > >
  {
    typedef s_compound_pixel_t<U, mpl::int_<3> > pixel_in_t;
    typedef s_compound_pixel_t<V, mpl::int_<3> > pixel_out_t;
    typedef typename std::unary_function<pixel_in_t, pixel_out_t>::result_type result_type;
    double const value;
    s_power(double value_) : value(value_){}
    s_power(const s_power& r_) : value(r_.value){}
    result_type operator()(const U &u) const
    {
      return result_type(::pow(u.a, value), ::pow(u.b, value), ::pow(u.c, value));
    }
  };  
  
  //! Computes the power of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC power_t(const imin_t &imin, const double var, imout_t &imout)
  {
    typedef s_power<
      typename imin_t::pixel_type, 
      typename imout_t::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op(var);
    return op_processor(imin, imout, op);   
  }


  template <class U, class V = U>
  struct s_square : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return u*u;
    }
  };
  
  //! Computes the square of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC square_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_square<
      typename imin_t::pixel_type, 
      typename imout_t::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imout, op);     
  }


  //@todo make internal tables
  template <class U, class V = U>
  struct s_square_root : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,V> t_to_v_traits;
      return static_cast<result_type>(std::sqrt(typename t_to_v_traits::supertype(u)));
    }
  };
  
  //! Computes the square root of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC square_root_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_square_root<
      typename imin_t::pixel_type, 
      typename imout_t::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imout, op);   
  }
  
  
  //! Returns a random value between 0 and 1
  inline yaF_double random_value_double()
  {
    typedef boost::mt19937 random_generator_type;
    //typedef boost::uniform_01<yaF_double> distribution_type;
    typedef boost::uniform_01<random_generator_type, yaF_double> distribution_generator_t;
    static distribution_generator_t generator = distribution_generator_t(random_generator_type());  // add time there ?
    
    return generator();
  }
  
  
  //! Generic distribution generator functor
  template <class T = yaF_double, class distribution = boost::math::normal >
  struct s_generic_distribution
  {
    typedef T result_type;
    distribution dist;
    s_generic_distribution() : dist(){}
    s_generic_distribution(const distribution& dist_) : dist(dist_){}
    result_type operator()() const
    {
      return static_cast<result_type>(boost::math::quantile(dist, random_value_double()));
    }
  };

  //! Generates the pixels of the image as being drawn from a gaussian distribution
  template <class iminout_t>
  yaRC generate_gaussian_random_t(iminout_t &imin, yaF_double mean = 0., yaF_double std_deviation = 1.)
  {
    typedef boost::math::normal distribution_t;
    typedef s_generic_distribution<
      typename iminout_t::pixel_type,
      distribution_t>  operator_type;
    
    s_apply_zeroary_operator op_processor;
    
    operator_type op(distribution_t(mean, std_deviation));
    return op_processor(imin, op);     
  }


}

#endif

