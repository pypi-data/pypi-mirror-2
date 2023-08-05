/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COLORPROCESS_XYZ_T_HPP__
#ifndef YAYI_COLORPROCESS_XYZ_T_HPP__


#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiCommon/common_constants.hpp>


/*!@file
 * This file contains the transformations to xyz spaces.
 * @author Raffi Enficiaud
 */

namespace yayi
{

  //! Transforms a pixel 3 according to a matrix
  //! Currently only pixel3 are supported (9 elements in the matrix)
  template<class pixel_in_t, class pixel_out_t, class coefficient_t = yaF_simple>
  struct s_matrix_transform : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    coefficient_t const * const coefficients;
    s_matrix_transform(coefficient_t const * coefficients_) : coefficients(coefficients_) {}
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      return 
        pixel_out_t(
          static_cast<value_type>(coefficients[0] * u.a + coefficients[1] * u.b + coefficients[2] * u.c),
          static_cast<value_type>(coefficients[3] * u.a + coefficients[4] * u.b + coefficients[5] * u.c),
          static_cast<value_type>(coefficients[6] * u.a + coefficients[7] * u.b + coefficients[8] * u.c));
    }
  };

  //! Transforms a pixel 3 by applying a gamma correction followed by a matrix multiplication (see @ref s_matrix_transform)
  //! Currently only pixel3 are supported (9 elements in the matrix)
  template<class pixel_in_t, class pixel_out_t, class coefficient_t = yaF_simple>
  struct s_matrix_transform_with_gamma_correction : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    s_power<pixel_in_t, pixel_out_t, coefficient_t> const gamma_op;
    s_matrix_transform<pixel_out_t, pixel_out_t, coefficient_t> const matrix_op;

    s_matrix_transform_with_gamma_correction(double gamma_, coefficient_t const * coefficients_) : gamma_op(gamma_), matrix_op(coefficients_) {}
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      return matrix_op(gamma_op(u));
    }
  };


  //! Transforms an RGB image into an XYZ image, considering reference white E and CIE primitives for RGB
  template <class image_in_, class image_out_>
  yaRC color_CIERGB_to_XYZ_refE_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] = 
      { 0.488718f,  0.310680f, 0.200602f,
        0.176204f,  0.812985f, 0.0108109f,
        0.0f,       0.0102048f,0.989795f };
    static const yaF_double gamma = 2.2;
  
    typedef s_matrix_transform_with_gamma_correction<
      typename image_in_::pixel_type, 
      typename image_out_::pixel_type>  operator_type;
    
    s_apply_unary_operator op_processor;
    
    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }




}

#endif /* YAYI_COLORPROCESS_XYZ_T_HPP__ */
