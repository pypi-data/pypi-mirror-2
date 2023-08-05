/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COLORPROCESS_LUMA_T_HPP__
#ifndef YAYI_COLORPROCESS_LUMA_T_HPP__


#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiCommon/common_constants.hpp>


/*!@file
 * This file contains the transformations to luminance according to 2 video standards.
 * @author Raffi Enficiaud
 */

namespace yayi
{

  //! Extracts the luminance from an RGB image, according to Rec 601
  template<class pixel_in_t, class pixel_out_t>
  struct s_RGB_to_L601 : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      static const yaF_simple c1 = 0.2989f, c2 = 0.5866f, c3 = 0.1145f;
      return static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c);
    }
  };

  template <class image_in_, class image_out_>
  yaRC color_RGB_to_L601_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_L601<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imo, op);
  }


  //! Extracts the luminance from an RGB image, according to Rec 709 (HDTV/D65)
  template<class pixel_in_t, class pixel_out_t >
  struct s_RGB_to_L709 : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      static const yaF_simple c1 = 0.2126f, c2 = 0.7152f, c3 = 0.0722f;
      return static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c);
    }
  };
  
  template <class image_in_, class image_out_>
  yaRC color_RGB_to_L709_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_L709<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imo, op);
  }  
}
  
#endif /* YAYI_COLORPROCESS_LUMA_T_HPP__ */
