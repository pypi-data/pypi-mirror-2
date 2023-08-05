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


#include <iostream>

namespace yayi
{
  using namespace errors;
  
  
  const string_type& type_support<yaBool>::name()    {static const string_type s = "yaBool";      return s;}
  const string_type& type_support<yaUINT8>::name()   {static const string_type s = "yaUINT8";     return s;}
  const string_type& type_support<yaINT8>::name()    {static const string_type s = "yaINT8";      return s;}
  const string_type& type_support<yaUINT16>::name()  {static const string_type s = "yaUINT16";    return s;}
  const string_type& type_support<yaINT16>::name()   {static const string_type s = "yaINT16";     return s;}
  const string_type& type_support<yaUINT32>::name()  {static const string_type s = "yaUINT32";    return s;}
  const string_type& type_support<yaINT32>::name()   {static const string_type s = "yaINT32";     return s;}
  const string_type& type_support<yaUINT64>::name()  {static const string_type s = "yaUINT64";    return s;}
  const string_type& type_support<yaINT64>::name()   {static const string_type s = "yaINT64";     return s;}
  const string_type& type_support<yaF_simple>::name(){static const string_type s = "yaF_simple";  return s;}
  const string_type& type_support<yaF_double>::name(){static const string_type s = "yaF_double";  return s;}


  s_return_code::operator string_type() const throw()
  {
    switch(this->code)
    {
    case e_Yr_ok:                           return "no error";
    case e_Yr_E_not_implemented:            return "function not implemented";
    case e_Yr_E_allocation:                 return "allocation error";
    case e_Yr_E_already_allocated:          return "already allocated";
    case e_Yr_E_not_allocated:              return "not allocated";
    case e_Yr_E:                            return "unknown error";
    case e_Yr_E_bad_parameters:             return "bad parameters";
    case e_Yr_E_null_pointer:               return "null pointer";
    case e_Yr_E_not_null_pointer:           return "not a null pointer";
    case e_Yr_E_file_io_error:              return "file I/O error";
    case e_Yr_E_bad_colour:                 return "bad color space";
    case e_Yr_E_memory:                     return "memory error";
    case e_Yr_E_unknown:                    return "unknown error";
    case e_Yr_E_overflow:                   return "data overflow";
    case e_Yr_E_locked:                     return "object locked";
    default:                                return "unfilled error : value = " + int_to_string(code);
    }
    //throw yaException("Should never appear !");
  }
  
  

  
  
  
  string_type s_type_help(type::scalar_type s) {
    
 
    switch(s) {
      case type::s_undefined: {const static string_type s = "undefined type";           return s;}

      case type::s_object:    {const static string_type s = "object";                   return s;}

      case type::s_bool:      {const static string_type s = "boolean";                  return s;}
      
      case type::s_ui8:       {const static string_type s = "unsigned int 8 bits";      return s;}
      case type::s_ui16:      {const static string_type s = "unsigned int 16 bits";     return s;}
      case type::s_ui32:      {const static string_type s = "unsigned int 32 bits";     return s;}

      case type::s_i8:        {const static string_type s = "int 8 bits";               return s;}
      case type::s_i16:       {const static string_type s = "int 16 bits";              return s;}
      case type::s_i32:       {const static string_type s = "int 32 bits";              return s;}
      
      case type::s_float:     {const static string_type s = "float single precision";   return s;}
      case type::s_double:    {const static string_type s = "float double precision";   return s;}
      
      case type::s_string:    {const static string_type s = "string";                   return s;}
      case type::s_wstring:   {const static string_type s = "wide string";              return s;}
      
      case type::s_variant:   {const static string_type s = "variant";                  return s;}
      
      /* s_object, s_image, s_order_function  */
      default : return "unfilled scalar type #" + int_to_string(s);
    }
  }



  type::operator string_type() const throw() {
    switch(c_type)
    {
      case type::c_image:                 return "image";
      case type::c_vector:                return "vector (of variant)";
      case type::c_structuring_element:   return "structuring element";
      case type::c_unknown:               return "unknown";
      case type::c_scalar:                return "scalar of "      + s_type_help(s_type);
      case type::c_3:                     return "pixel3 of "      + s_type_help(s_type);
      case type::c_complex:               return "complex of "     + s_type_help(s_type);
      case type::c_coordinate:            return "coordinate of "  + s_type_help(s_type);
      case type::c_4:                     return "pixel4 of "      + s_type_help(s_type);
      default:                            return "unfilled #"      + int_to_string(c_type);
    }
   
  }

  type type::Create(const string_type& s) throw() {
  
    type ret = type_undefined;
    string_type::size_type i0 = s.find(" ");
    if(i0 == string_type::npos)
      return ret;
    
    string_type ss = s.substr(0, i0);
    if(ss == "scalar")
      ret.c_type = type::c_scalar;
    else if(ss == "coordinate") { 
      ret.c_type = type::c_coordinate;
    }
    else
      return type_undefined;
      
    ss = s.substr(i0);
    
    string_type::size_type i1 = ss.find("of");
    if(i1 == string_type::npos) {
      i1 = ss.find("#");
      if(i1 == string_type::npos) 
        return type_undefined;
        
      // we do nothing there
    }
    if(ss.find("single", i1) != string_type::npos) {
      ret.s_type = type::s_float;
    } else if(ss.find("double", i1) != string_type::npos) {
      ret.s_type = type::s_double;
    } else if(ss.find("unsigned", i1) != string_type::npos) {
      if(ss.find("8", i1) != string_type::npos) {
        ret.s_type = s_ui8;
      } else if(ss.find("16", i1) != string_type::npos) {
        ret.s_type = s_ui16;
      } else {
        ret.s_type = s_ui32;
      } 
    } else {
      if(ss.find("8", i1) != string_type::npos) {
        ret.s_type = s_i8;
      } else if(ss.find("16", i1) != string_type::npos) {
        ret.s_type = s_i16;
      } else {
        ret.s_type = s_i32;
      }     
    }
    
    
    return ret;
  
  }

}

