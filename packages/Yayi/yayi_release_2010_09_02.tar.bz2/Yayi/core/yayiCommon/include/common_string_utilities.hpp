/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_STRING_UTILITIES_HPP__
#define YAYI_COMMON_STRING_UTILITIES_HPP__


/*!@file 
 * @brief Contains some string utilities
 *
 */


#include <string>
#include <ios>
#include <sstream>
#include <ctime>
#include <limits>

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>

namespace yayi
{


  //! Formats an int to a string
  inline string_type int_to_string(const int v, const int format_size = 0, const char format_char = '0')
  {
    std::ostringstream o;
    if(format_size > 0) {o.width(format_size); o.fill(format_char);}
    o << v;
    return o.str();
  }


  /*!@brief Formats any object to its string representation
   *
   * @param[in]   u             the object instance
   * @param[in]   format_size   the minimal number of characters the output string should have
   * @param[in]   format_char   the filling character should the output string size be lower than required
   *
   * @author Raffi Enficiaud
   */
  template <class U>
  inline string_type any_to_string(const U& u, const int format_size = 0, const char format_char = '0')
  {
    std::ostringstream o;
    if(format_size > 0) {o.width(format_size); o.fill(format_char);}
    o << u;
    return o.str();
  }



  
  
  /*!@brief Extract an object from a stream
   *
   * @param[in]   s             the stream
   * @param[out]  u             the object
   *
   * @author Raffi Enficiaud
   */
  template <class stream_t, class U> 
  inline bool any_from_string(stream_t& s, U& u)
  {
    s >> u;
    return !s.fail();
  }
  
  template <class stream_t> 
  inline bool any_from_string(stream_t& s, char& u)
  {
    int ut;
    s >> ut;
    bool ret = !s.fail();
    if(!ret) return false;
    // no reference to common_error to avoid cyclic dependencies
    assert(ut <= std::numeric_limits<char>::max() && ut >= std::numeric_limits<char>::min());
    u = static_cast<char>(ut);
    return true;
  }

  template <class stream_t> 
  inline bool any_from_string(stream_t& s, unsigned char& u)
  {
    unsigned int ut;
    s >> ut;
    bool ret = !s.fail();
    if(!ret) return false;
    // no reference to common_error to avoid cyclic dependencies
    assert(ut <= std::numeric_limits<unsigned char>::max() && ut >= std::numeric_limits<unsigned char>::min());
    u = static_cast<unsigned char>(ut);
    return true;
  }  


  //! Utility functor that can be called in by "std::for_each", gathering the
  //! string representation for each element of the container (in the member "s")
  struct s_any_to_string_for_container
  {
    std::string s;
    int format;
    char fill;
    char sep;
    const std::string sep2;
    
    s_any_to_string_for_container(
      const std::string &init_s = "", 
      int init_format = 0, 
      char init_fill = '0', 
      char sep_ = ' ',
      const std::string sep2_ = " -- ") : s(init_s), format(init_format), fill(init_fill), sep(sep_), sep2(sep2_)
    {}
    
    template <class T>
    void operator()(const T& t)
    {
      s += sep;
      s += any_to_string(t, format, fill);
    }
    
    template <class T>
    void operator()(const T* const & t)
    {
      s += sep;
      s += any_to_string(*t, format, fill);
    }      
    
    template <class T, class U>
    void operator()(const std::pair<T,U>& t)
    {
      s += sep2;
      s += any_to_string(t.first, format, fill);
      s += sep;
      s += any_to_string(t.second, format, fill);
    }
  };




  /*!@brief Extracts an integer from a string
   *
   * @author Raffi Enficiaud
   */
  template <class string_type_t>
  int integer_extractor(string_type_t &str, int default_value, typename string_type_t::value_type delim = ' ')
  {
    typename string_type_t::size_type s = std::string::npos;
    string_type sub;
    if(delim == 0)
    {
      sub = str;
    }
    else
    {
      s = str.find(delim);
      if(s == std::string::npos || s <= 0)
        return default_value;

      sub = str.substr(0, s);
    }

    std::basic_istringstream<typename string_type_t::value_type> is(sub);
    int i = 0;
    is >> i;
    if(s != std::string::npos) str = str.substr(s + 1);
    return i;
  }



  //! Transforms a date formatted string into a date object
  template <class string_type_t>
  std::tm from_string_to_date(const string_type_t& str)
  {
    std::tm out;
    string_type_t date(str);

    out.tm_wday   = 1;
    out.tm_yday   = 1;

    out.tm_year   = integer_extractor(date, 2000, '-');
    out.tm_mon    = integer_extractor(date, 01,   '-');
    out.tm_mday   = integer_extractor(date, 01,   ' ');
    
    out.tm_hour   = integer_extractor(date, 00,   ':');
    out.tm_min    = integer_extractor(date, 00,   ':');
    out.tm_sec    = integer_extractor(date, 00,   '\0');
    return out;

  }





} // namespace yayi



#endif /* YAYI_COMMON_STRING_UTILITIES_HPP__ */

