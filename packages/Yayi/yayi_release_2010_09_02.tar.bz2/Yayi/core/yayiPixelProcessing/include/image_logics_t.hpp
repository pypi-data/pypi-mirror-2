/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_IMAGE_LOGIC_T_HPP__
#define YAYI_PIXEL_IMAGE_LOGIC_T_HPP__

/*!@file
 * This file defines the logic template operations on images
 */
 
#include <boost/call_traits.hpp>
#include <functional>
#include <Yayi/core/yayiPixelProcessing/image_arithmetics.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp> // to remove

namespace yayi
{

  //! Complements a pixel (binary complement)
  template <class U, class V = U>
  struct s_logical_not : public std::unary_function<U, V>
  {
    //typedef operator_type_unary operator_tag;
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const throw()
    {
      return !u;
    }
    
  };

  template <class image_in1_, class image_out_>
  yaRC logical_not_images_t(
    const image_in1_& imin1, 
    image_out_& imo)
  {
    typedef s_logical_not<
      typename image_in1_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin1, imo, op);
  }
  
  



}

#endif /* YAYI_PIXEL_IMAGE_LOGIC_T_HPP__ */
