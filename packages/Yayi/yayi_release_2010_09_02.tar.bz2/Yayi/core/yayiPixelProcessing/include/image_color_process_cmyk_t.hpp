/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COLORPROCESS_CMYK_T_HPP__
#ifndef YAYI_COLORPROCESS_CMYK_T_HPP__


#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiCommon/common_constants.hpp>


/*!@file
 * This file contains the transformations to cmyk space.
 * @author Raffi Enficiaud
 */

namespace yayi
{

  //! Functor for transforming the original RGB (in the range [0,255]) to CMYK (in the range [0,1])
  template<class pixel_in_t, class pixel_out_t>
  struct s_RGB_to_CMYK : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      if (u.a == 0 && u.b == 0 && u.c == 0) 
      {
        return pixel_out_t(0,0,0,1);
      }
     
      // it is possible to reduce the number of divisions here 
      typename pixel_out_t out(1);
      out.a -= u.a/typename pixel_out_t::value_type(255);
      out.b -= u.b/typename pixel_out_t::value_type(255);
      out.c -= u.c/typename pixel_out_t::value_type(255);

      out.d = std::min(out.a, std::min(out.b, out.c));
      typename pixel_out_t::value_type const min_1 = 1 - out.d;
      
      out.a -= out.d;
      out.a /= min_1;
      out.b -= out.d;
      out.b /= min_1;
      out.c -= out.d;
      out.c /= min_1;
      
      return out;
    }
  };

  //! This function transforms a 3-channels RGB image (integer in the range [0, 255]) into a 4-channels CMYK image (range [0,1])
  template <class image_in_, class image_out_>
  yaRC color_RGB_to_CMYK_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_CMYK<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imo, op);
  }
}

#endif /* YAYI_COLORPROCESS_CMYK_T_HPP__ */