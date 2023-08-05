/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_COPY_T_HPP__
#define YAYI_PIXEL_IMAGE_COPY_T_HPP__



#include <algorithm>
#include <boost/call_traits.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>

#include <cstring>

namespace yayi
{

  template <class pixel_in, class pixel_out>
  struct s_copy : public std::unary_function<pixel_in, pixel_out>
  {
    pixel_out operator()(typename boost::call_traits<pixel_in>::param_type p) const throw()
    {
      return static_cast<pixel_out>(p);
    }
  };

  template <class pixel_in>
  struct s_copy<pixel_in, pixel_in> : public std::unary_function<pixel_in, pixel_in>
  {
    const pixel_in& operator()(const pixel_in& p) const throw()
    {
      return p;
    }
  };
  
  template <bool b_trivial_copy>
  struct s_copy_helper
  {
  
    template <class image_in_, class image_out_>
    yaRC operator()(const image_in_& imin, image_out_& imo)
    {
      typedef s_copy<
        typename image_in_::pixel_type, 
        typename image_out_::pixel_type>  operator_type;
      
      s_apply_unary_operator op_processor;
      
      operator_type op;
      return op_processor(imin, imo, op);       
    }
  
  };

  template <>
  struct s_copy_helper<true> : s_copy_helper<false>
  {
    typedef s_copy_helper<false> parent_type;
  
    template <class image_in_, class image_out_>
    yaRC operator()(const image_in_& imin, image_out_& imo)
    {
      if(total_number_of_points(imin.Size()) == total_number_of_points(imo.Size()))
      {
        void *p = std::memcpy(&imo.pixel(0), &imin.pixel(0), sizeof(typename image_in_::pixel_type) * total_number_of_points(imin.Size()));
        return ((p == (void*)&imo.pixel(0)) ? yaRC_ok : yaRC_E_unknown);
      }
      else
        return parent_type::operator()(imin, imo);
    }  
  };


  //! Simple copy
  template <class image_in_, class image_out_>
  yaRC copy_image_t(const image_in_& imin, image_out_& imo)
  {
    s_copy_helper<
      boost::mpl::and_<
        typename boost::is_same<typename image_in_::pixel_type, typename image_out_::pixel_type>,
        typename boost::has_trivial_assign<typename image_in_::pixel_type>::type,
        typename boost::has_trivial_assign<typename image_out_::pixel_type>::type
      >::type::value 
    > op_helper;
    return op_helper(imin, imo);
  }

  



  //! Windowed copy
  template <class image_in_, class image_out_>
    yaRC copy_image_windowed_t(
    const image_in_& imin, 
    const s_hyper_rectangle<image_in_::coordinate_type::static_dimensions> &rect_in, 
    const s_hyper_rectangle<image_out_::coordinate_type::static_dimensions> &rect_out, 
    image_out_& imo)
  {
    typedef s_copy<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, rect_in, imo, rect_out, op);    
  }
  
  
  
  
  
  
}

#endif

