/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiCommon/include/common_types_T.hpp>
#include <Yayi/core/yayiCommon/common_pixels.hpp>

#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_colorspace.hpp>

#include <iostream>

namespace yayi
{
  using namespace errors;
  
  yaColorSpace::operator string_type() const throw()
  {
    string_type out;
    switch(cs_major)
    {
    case ecd_rgb: out += "rgb"; break;
    case ecd_hls: out += "hls"; break;
    
    case ecd_undefined:
    default:
      out += "undefined";break;
    }
  
    out += " color space";

    string_type r;  
    switch(cs_minor)
    {
    case ecdm_hls_l1:   r += "l1 norm";  break;
    case ecdm_hls_trig: r += "trig";     break;
    default:
      break;
    }
    if(r != "")
      out += " - version: " + r;

    r.clear();
    switch(illuminant)
    {
    case ei_d50:          r += "D50"; break;
    case ei_d55:          r += "D55"; break;
    case ei_d65:          r += "D65"; break;
    case ei_d75:          r += "D75"; break;
    case ei_A:            r += "A";   break;
    case ei_B:            r += "B";   break;
    case ei_C:            r += "C";   break;
    case ei_E:            r += "E";   break;
    case ei_undefined:
    default:
      break;
    }
    
    if(r != "")
      out += " - illuminant: " + r;

    r.clear();
    switch(primary)
    {
    case ergbp_CIE:          r += "CIE";      break;
    case ergbp_sRGB:         r += "sRGB";     break;
    case ergbp_AdobeRGB:     r += "AdobeRGB"; break;
    case ergbp_AppleRGB:     r += "AppleRGB"; break;
    case ergbp_NTSCRGB:      r += "NTSC";     break;
    case ergbp_SecamRGB:     r += "Secam";    break;
    case ergbp_undefined:
    default:
      break;
    }
    
    if(r != "")
      out += " primaries: " + r;
        

    return out;
  
  }
  
}
