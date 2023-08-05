/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_COLORSPACE_HPP__
#define YAYI_COMMON_COLORSPACE_HPP__

/*!@file
 * This file contains the necessary elements for colour information
 *
 * @author Raffi Enficiaud
 */

namespace yayi
{

  struct s_yaColorSpace
  {
    typedef s_yaColorSpace this_type;
    
    typedef enum e_colorspace_major
    {
      ecd_undefined,
      ecd_rgb,
      ecd_hls,
      ecd_lab,
      ecd_xyz,
      ecd_xyY,
      ecd_yuv
    } yaColorSpaceMajor;

    typedef enum e_colorspace_minor
    {
      ecdm_undefined,
      ecdm_hls_l1,
      ecdm_hls_trig
    } yaColorSpaceMinor;

    typedef enum e_illuminant
    {
      ei_undefined,
      ei_d50,
      ei_d55,
      ei_d65,
      ei_d75,
      ei_A, 
      ei_B, 
      ei_C, 
      ei_E 
    } yaIlluminant;

    typedef enum e_rgb_primaries
    {
      ergbp_undefined,
      ergbp_CIE,
      ergbp_sRGB,
      ergbp_AdobeRGB,
      ergbp_AppleRGB,
      ergbp_NTSCRGB,
      ergbp_SecamRGB
    } yaRGBPrimary;

    yaColorSpaceMajor cs_major;
    yaColorSpaceMinor cs_minor;
    yaIlluminant      illuminant;
    yaRGBPrimary      primary;
    

    //! Stringifier
    YCom_ operator string_type() const throw();
    
    //! Streaming
    friend std::ostream& operator<<(std::ostream& o, const this_type& t) {
      o << t.operator string_type(); return o;
    }
    
    
    //! Default constructor
    s_yaColorSpace() 
      : cs_major(ecd_undefined), cs_minor(ecdm_undefined), illuminant(ei_undefined), primary(ergbp_undefined) {}
    
    //! Direct constructor
    s_yaColorSpace(yaColorSpaceMajor mm, yaIlluminant ill = ei_d65, yaRGBPrimary prim = ergbp_sRGB, yaColorSpaceMinor m = ecdm_undefined) 
      : cs_major(mm), cs_minor(m), illuminant(ill), primary(prim) {}
    
  };
  
  typedef s_yaColorSpace yaColorSpace;

  // Some predefined types
  const static yaColorSpace 
    cs_sRGB(yaColorSpace::ecd_rgb),                                                   //!< sRGB
    cs_CIERGB(yaColorSpace::ecd_rgb, yaColorSpace::ei_d65, yaColorSpace::ergbp_CIE),  //!< CIE RGB
    
    //! HLS with l1 norm
    cs_HLSl1(yaColorSpace::ecd_hls, yaColorSpace::ei_undefined, yaColorSpace::ergbp_undefined, yaColorSpace::ecdm_hls_l1)
  ;
}
 
 
#endif /* YAYI_COMMON_COLORSPACE_HPP__ */
