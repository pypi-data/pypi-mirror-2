/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_CONSTANT_T_HPP__
#define YAYI_PIXEL_IMAGE_CONSTANT_T_HPP__

/*!@file
 * This file contains the implementation of the functions setting an image to a constant value
 * @author Raffi Enficiaud
 */

#include <algorithm>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <boost/type_traits/has_trivial_assign.hpp> 
#include <boost/mpl/or.hpp>
#include <boost/mpl/sizeof.hpp>
#include <boost/mpl/if.hpp>
#include <boost/mpl/equal.hpp>

#include <cstdio>
#include <cstring>

namespace yayi
{

  //! Functor for setting the content of an image to a constant value
  template <class pixel_in>
  struct s_constant : public std::unary_function<pixel_in, void>
  {
    const pixel_in value;

    s_constant(const pixel_in &v_) : value(v_){}
    void operator()(pixel_in& p) const
    {
      p = value;
    }
  };
  
  //!@todo add memset implementation for simple types
  
  
  //! Helper structure for values that can be copied with bit copy
  template <class image_in_out_, class b_has_trivial_assign = boost::false_type>
  struct s_constant_image_helper
  {
    yaRC operator()(typename image_in_out_::pixel_type const& value_, image_in_out_& im)
    {
      typedef s_constant<typename image_in_out_::pixel_type>  operator_type;
      s_apply_unary_operator                                  op_processor;
    
      operator_type op(static_cast<typename image_in_out_::pixel_type>(value_));
      return op_processor(im, op);      
    }
  };
  
  
  struct s_set_by_memset
  {
    template <class image_in_out_>
    yaRC operator()(typename image_in_out_::pixel_type const& value_, image_in_out_& im)
    {
      std::memset(&im.pixel(0), value_, total_number_of_points(im.Size()) * sizeof(typename image_in_out_::pixel_type));
      return yaRC_ok;
    }
  };
  
  
  struct s_set_by_successive_copies
  {
    template <class image_in_out_>
    yaRC operator()(typename image_in_out_::pixel_type const& value_, image_in_out_& im)
    {
      typedef typename image_in_out_::pixel_type pixel_type;
      const offset total = total_number_of_points(im.Size());
      offset final = im.Size()[0];
      for(offset current = 0; current < final; current++)
      {
        im.pixel(current) = value_;
      }
      
      while(2*final < total)
      {
        std::memcpy(&im.pixel(final), &im.pixel(0), final * sizeof(pixel_type));
        final *= 2;
      }
      std::memcpy(&im.pixel(final), &im.pixel(0), (total-final/2) * sizeof(pixel_type));
      
      return yaRC_ok;
    }
  };  
  
  //! Specializing for image of trivial copy type with continuous memory
  //! We do some manual things there
  template <class pixel_type, class coordinate_type>
  struct s_constant_image_helper< Image<pixel_type, coordinate_type, s_default_image_allocator<pixel_type, coordinate_type> >, boost::true_type >
  {
    typedef Image<pixel_type, coordinate_type, s_default_image_allocator<pixel_type, coordinate_type> > image_in_out_;
    yaRC operator()(typename image_in_out_::pixel_type const& value_, image_in_out_& im)
    {
      using namespace boost;
      typedef typename mpl::if_<
        mpl::equal<
          typename mpl::sizeof_<typename image_in_out_::pixel_type>::type,
          mpl::int_<8>
        >,
        s_set_by_memset,
        s_set_by_successive_copies
      >::type op_type;
      
      op_type op;
        
      return op(value_, im);
    }
  };
  

  //! Sets the content of an image to a constant value
  template <class image_in_out_>
  yaRC constant_image_t(typename image_in_out_::pixel_type const& value_, image_in_out_& im)
  {
    typedef typename mpl::or_<
      typename boost::has_trivial_assign<typename image_in_out_::pixel_type>::type,
      typename boost::is_pod<typename image_in_out_::pixel_type>::type
      >::type can_optimize;
    s_constant_image_helper<image_in_out_, can_optimize> op_const_helper;
    return op_const_helper(value_, im);
  }

  //! Windowed set constant
  template <class image_in_out_>
  yaRC constant_image_windowed_t(
    typename image_in_out_::pixel_type const& value_, 
    const s_hyper_rectangle<image_in_out_::coordinate_type::static_dimensions> &rect_in, 
    image_in_out_& im)
  {
    typedef s_constant<typename image_in_out_::pixel_type>  operator_type;
    s_apply_unary_operator                                  op_processor;
    
    operator_type op(static_cast<typename image_in_out_::pixel_type>(value_));
    return op_processor(im, rect_in, op);    
  }


}

#endif
