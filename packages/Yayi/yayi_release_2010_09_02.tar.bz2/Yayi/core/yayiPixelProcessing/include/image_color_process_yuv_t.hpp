/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COLORPROCESS_YUV_T_HPP__
#ifndef YAYI_COLORPROCESS_YUV_T_HPP__


#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiCommon/common_constants.hpp>


/*!@file
 * This file contains the transformations to YUV according to the standard.
 * @author Raffi Enficiaud
 */

namespace yayi
{

  //! Functor implementing the tranformation from RGB to YUV
  template<class pixel_in_t, class pixel_out_t>
  struct s_RGB_to_YUV : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      typedef typename pixel_out_t::value_type value_type;
      
      static const yaF_simple 
        yc1 = 0.299f,   yc2 = 0.587f,     yc3 = 0.114f,
        uc1 = -0.147f,  uc2 = -0.289f,    uc3 = 0.437f,
        vc1 = 0.615f,   vc2 = -0.515f,    vc3 = -0.1f;
      return 
        pixel_out_t(
          static_cast<value_type>(yc1 * u.a + yc2 * u.b + yc3 * u.c),
          static_cast<value_type>(uc1 * u.a + uc2 * u.b + uc3 * u.c),
          static_cast<value_type>(vc1 * u.a + vc2 * u.b + vc3 * u.c));
    }
  };


  //! Transforms an RGB image into an YUV image
  template <class image_in_, class image_out_>
  yaRC color_RGB_to_YUV_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_YUV<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imo, op);
  }





  template<class pixel_in_t, class pixel_out_t>
  struct s_YUV_to_RGB : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      typedef typename pixel_out_t::value_type value_type;
      
      // Refaire la matrice d'inversion
      static const yaF_simple 
        c11 = 1.f,      c12 = -0.000039f, c13 = 1.13983f,
        c21 = 1.00039f, c22 = -0.39381f,  c23 = -0.580501f,
        c31 = 0.997972f,c32 = 2.02788f,   c33 = -0.0004804f;
        
      return 
        pixel_out_t(
          static_cast<value_type>(c11 * u.a + c12 * u.b + c13 * u.c),
          static_cast<value_type>(c21 * u.a + c22 * u.b + c23 * u.c),
          static_cast<value_type>(c31 * u.a + c32 * u.b + c33 * u.c));
    }
  };

  //! Transforms an YUV image into an RGB image (reverse transform of @ref color_RGB_to_YUV_t)
  template <class image_in_, class image_out_>
  yaRC color_YUV_to_RGB_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_YUV_to_RGB<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op;
    return op_processor(imin, imo, op);
  }




}

#endif /* YAYI_COLORPROCESS_YUV_T_HPP__ */
