/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#ifndef YAYI_COMMON_ERRORS_HPP__
#define YAYI_COMMON_ERRORS_HPP__

/*!@file
 * @brief Errors and return codes describings
 * 
 */


#include <string>
#include <ios>
#include <exception>
#include <cassert>

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/include/common_string_utilities.hpp>

namespace yayi
{
  
  /*!@namespace 
   * Contains standard error or warning codes
   */
  
  namespace errors
  {


    //! Errors or information type
    enum e_message_type
    {
      e_message_error,
      e_message_warning,
      e_message_information
    };

    
    //! Returns the current error stream
    YCom_ std::ostream& yayi_error_stream();

    /*! @brief Yayi exception class
     *
     * This class should be used for any exception fired within yayi
     * @author Raffi Enficiaud
     */
    struct yaException : public std::exception
    {
    private:
      string_type   str_desc;

    public:
      yaException(const char *str) : str_desc(str){}

      yaException(const string_type &error_description) : str_desc(error_description){}

      yaException(const yaRC& r)
      {
        // to branch to an unit compiled function
        str_desc = static_cast<string_type>(r);
      }
      
      virtual ~yaException() throw() {}
      
      virtual const char *what( ) const throw() {return str_desc.c_str();}
      
      const string_type& message() const {return str_desc;}
    
    };

#define YAYI_DEBUG_MESSAGE(s)\
  std::string("File :\t\t") + std::string(__FILE__) + std::string("\n" \
  "Line :\t\t") + int_to_string(__LINE__) + std::string("\n" \
  "Message :\t") + std::string(s)

#define YAYI_DEBUG_MESSAG_STREAM(s)\
  "File :\t\t" << __FILE__ << "\n" \
  "Line :\t\t" << __LINE__ << "\n" \
  "Message :\t" << s

#define YAYI_ERROR_FORMATER(s)\
  std::string("ASSERTION FAILURE !!!\n") + \
  YAYI_DEBUG_MESSAGE(s)

#define YAYI_THROW(s)\
  throw errors::yaException(YAYI_DEBUG_MESSAGE(s))

#define YAYI_ASSERT(cond, s)\
  if(!(cond)) {YAYI_THROW(s);}


  YCom_ string_type demangle(const char* name);



#ifndef NDEBUG
  #define DEBUG_ONLY_VARIABLE(x)  x
  //! Simple assert for debug
  #define DEBUG_ASSERT(cond, s)   {YAYI_ASSERT(cond, s)}
  #define DEBUG_THROW(s)          {YAYI_THROW(s);}
  #define YAYI_THROW_DEBUG_ONLY__ 
  #define DEBUG_INFO(s)           {errors::yayi_error_stream() << YAYI_DEBUG_MESSAG_STREAM(s) << std::endl;}
#else
  #define DEBUG_ONLY_VARIABLE(x)
  #define DEBUG_ASSERT(cond, s)   {}
  #define DEBUG_THROW(s)          {}
  #define YAYI_THROW_DEBUG_ONLY__ throw()
  #define DEBUG_INFO(s)           {}
#endif

  } // namespace errors

} // namespace yayi


#endif /* YAYI_COMMON_ERRORS_HPP__ */


