/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_FILL_BORDERS_T_HPP__
#define YAYI_PIXEL_IMAGE_FILL_BORDERS_T_HPP__

/*!@file
 * This file contains some useful functions for dealing with the values on the borders
 */

#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_arithmetics_t.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>

#include <boost/function.hpp>
#include <boost/bind.hpp>

namespace yayi
{

  //! Generic function for applying a function object of two arguments on each borders
  //! The function objet first argument is the image, and the second argument is the window of the border on which 
  //! it should be applied. 
  template <class image_inout_t, class op_t>
  yaRC image_apply_function_on_borders_t(image_inout_t& im, op_t& op)
  {
    typename image_inout_t::coordinate_type const s(im.Size());
    typedef s_hyper_rectangle<image_inout_t::coordinate_type::static_dimensions> hrect_t;
    
    for(int i = 0; i < image_inout_t::coordinate_type::static_dimensions; i++)
    {
      if(s[i] <= 2)
        continue;
      
      typename image_inout_t::coordinate_type end(s), start(0);
      end[i] = 1;

      yaRC res = op(im, hrect_t(start, end - start));
      if(res != yaRC_ok)
      {
        DEBUG_INFO("error during call of operator on border (first), dimension " << i <<  " : " << res); 
        return res;
      }
      
      end[i] = start[i] = s[i];
      --start[i];
      res = op(im, hrect_t(start, end - start));
      if(res != yaRC_ok)
      {
        DEBUG_INFO("error during call of operator on border (second), dimension " << i <<  " : " << res);
        return res;
      }
    
    }
    return yaRC_ok;
  
  }
  
  //! Copy the borders of im, and places the result into imout
  template <class image_t>
  yaRC image_copy_borders_t(const image_t& im, image_t& imout)
  {
    typedef s_hyper_rectangle<image_t::coordinate_type::static_dimensions> hrect_t;
    typedef yaRC fp_type(const image_t&, const hrect_t&);
    boost::function<fp_type> f = boost::bind(copy_image_windowed_t<image_t, image_t>, _1, _2, _2, boost::ref(imout));
    
    return image_apply_function_on_borders_t(im, f);
  }  

  //! Fills the borders of im with a constant value
  template <class image_t>
  yaRC image_fill_borders_t(image_t& im, typename image_t::pixel_type const& value)
  {
    typedef s_hyper_rectangle<image_t::coordinate_type::static_dimensions> hrect_t;
    typedef yaRC fp_type(const image_t&, const hrect_t&);
    boost::function<fp_type> f = boost::bind(constant_image_windowed_t<image_t>, boost::cref(value), _2, _1);
    
    return image_apply_function_on_borders_t(im, f);
  }

  //! Complements the borders of im, and places the result into imout
  template <class image_t>
  yaRC image_complement_borders_t(const image_t& im, image_t& imout)
  {
    typedef s_hyper_rectangle<image_t::coordinate_type::static_dimensions> hrect_t;
    typedef yaRC fp_type(const image_t&, const hrect_t&);
    boost::function<fp_type> f = boost::bind(complement_images_windowed_t<image_t, image_t>, _1, _2, _2, boost::ref(imout));
    
    return image_apply_function_on_borders_t(im, f);  
  }

}

#endif /* YAYI_PIXEL_IMAGE_FILL_BORDERS_T_HPP__ */
