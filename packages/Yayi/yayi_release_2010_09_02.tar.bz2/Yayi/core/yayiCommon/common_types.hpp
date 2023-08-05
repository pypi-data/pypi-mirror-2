/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_TYPES_HPP__
#define YAYI_COMMON_TYPES_HPP__


/*!@file
 * @brief Common types used accross the library
 *
 */

#include <string>
#include <ios>
#include <sstream>
#include <boost/cstdint.hpp>


#include <Yayi/core/yayiCommon/yayiCommon.hpp>

#ifdef YAYI_TRACE_UNCHECKED_ERRORS
#pragma message(" -- unchecked error trace activated")
#endif


#ifdef YAYI_ERROR_FOR_UNSET_PIXELS
#pragma message(" -- unset pixel access detection activated")
#endif


namespace yayi
{
  typedef bool                    yaBool;                                     //!< classical boolean

  typedef unsigned char           yaUINT8;                                    //!< 8bits unsigned integer
  typedef signed char             yaINT8;                                     //!< 8bits signed integer

  typedef unsigned short int      yaUINT16;                                   //!< 16bits unsigned integer
  typedef signed short int        yaINT16;                                    //!< 16bits signed integer

  typedef boost::uint32_t         yaUINT32;                                   //!< 32bits unsigned integer
  typedef boost::int32_t          yaINT32;                                    //!< 32bits signed integer

  typedef float                   yaF_simple;                                 //!< Floating point, simple precision
  typedef double                  yaF_double;                                 //!< Floating point, double precision

#ifdef _WIN32
  typedef __int64                 yaINT64;                                    //!< 64bits unsigned integer
  typedef unsigned __int64        yaUINT64;                                   //!< 64bits signed integer
#else
  typedef long long int           yaINT64;
  typedef unsigned long long int  yaUINT64;
#endif

  typedef yaINT32                 scalar_coordinate;
  typedef yaF_simple              scalar_real_coordinate;
  typedef yaINT32                 offset;

  typedef std::string             string_type;
  typedef std::wstring            wide_string_type;

  struct s_any_type;              // Forward declaration
  typedef s_any_type              variant;                                    //!< The main variant type


  typedef bool (*order_function_type)(const variant&, const variant&);        //!< Generic order function type



  /*!@brief Type description structure
   *
   */
  struct s_type_description
  {
    typedef enum e_scalar_type
    {
      s_undefined,
      s_bool,
      s_ui8, s_ui16, s_ui32, s_ui64,
      s_i8, s_i16, s_i32, s_i64,
      s_float, s_double, 
      s_object, s_variant,
      s_string, s_wstring,
      s_image,

      s_order_function
    } scalar_type;


    typedef enum e_compound_type
    {
      c_unknown,
      c_generic, 
      c_variant,                                                  //!< An unknown variant type
      c_image,
      c_iterator,                                                 //!< An iterator over a container
      c_coordinate,                                               //!< coordinate type
      c_scalar, c_complex, c_3, c_4,                              //!< Generic and typed pixels
      c_vector, c_map,                                            //!< stl equivalent
      c_container,                                                //!< generic container
      c_function,                                                 //!< generic function type
      c_structuring_element,                                      //!< structuring element
      c_neighborhood                                              //!< a neighborhood
    } compound_type;

    scalar_type         s_type;                                   //!< Scalar definition of the type
    compound_type       c_type;                                   //!< Compound definition of the type
    
    bool operator==(const s_type_description& r) const {
      return s_type == r.s_type && c_type == r.c_type;
    }

    bool operator!=(const s_type_description& r) const {
      return !(*this == r);
    }
        
    //! Stringifier
    YCom_ operator string_type() const throw();
    
    //! Type "factory" (from a string)
    YCom_ static s_type_description Create(const string_type&) throw();
    
    //! Streaming
    friend std::ostream& operator<<(std::ostream& o, const s_type_description& t) {
      o << t.operator string_type(); return o;
    }
    
    
    //! Default constructor
    s_type_description() {}
    
    //! Direct constructor
    s_type_description(compound_type c, scalar_type s) : s_type(s), c_type(c) {}
    
    
  };


  typedef s_type_description type;
  
  // Some predefined types
  const static type 
    type_undefined(type::c_unknown, type::s_undefined),              //!< The undefined type
    type_scalar_uint8(type::c_scalar, type::s_ui8)                   //!< scalar unsigned int 8 bit
  ;







  /*!@brief Return code class offering some functionnalities for description
   * 
   * Behaves differently according to the YAYI_TRACE_UNCHECKED_ERRORS macro (for debugging purposes).
   * @author Raffi Enficiaud
   */
  struct s_return_code
  {
  public:
    typedef s_return_code   this_type;
    typedef yaINT16         repr_type;
    repr_type               code;

#ifdef YAYI_TRACE_UNCHECKED_ERRORS
  private:
    mutable bool m_b_has_been_chk_before_assignement;
  
  public:
    this_type& operator=(const this_type& r_)
    {
      if(!m_b_has_been_chk_before_assignement)
        yayi_error_stream << "unchecked error : " << this->operator std::string() << std::endl;
      code = r_.code;
    }
#endif


  public:
    s_return_code(){}

    s_return_code(repr_type c) : 
      code(c)
#ifdef YAYI_TRACE_UNCHECKED_ERRORS
      , m_b_has_been_chk_before_assignement( c == 0 )
#endif
    {}

    bool operator==(const this_type& r) const throw()
    {
#ifdef YAYI_TRACE_UNCHECKED_ERRORS
      m_b_has_been_chk_before_assignement = true;
#endif
      return code == r.code;
    }

    bool operator!=(const this_type& r) const throw()
    {
      return !this->operator==(r);
    }

    /*!@brief Stringizer operator
     * Returns a string describing the error (if the error is known)
     */
    YCom_ operator string_type() const throw();
    
    //! Streaming function for return code
    friend std::ostream& operator<< (std::ostream &s, const s_return_code& r)
    {
      s << r.operator string_type(); return s;
    }
  };

  //! Return code type
  typedef s_return_code yaRC; 

 

  
  /*!@brief Return codes namespace
   * Every error or warning should be described within this namespace
   */
  namespace return_code_constants
  {
    enum e_standard_result
    {
      e_Yr_ok,
      e_Yr_E,
      e_Yr_E_allocation,
      e_Yr_E_already_allocated,
      e_Yr_E_not_allocated,
      e_Yr_E_bad_input_type,
      e_Yr_E_bad_cast,
      e_Yr_E_bad_parameters,
      e_Yr_E_null_pointer,
      e_Yr_E_not_null_pointer,
      e_Yr_E_bad_size,
      e_Yr_E_not_implemented,
      e_Yr_E_file_io_error,
      e_Yr_E_bad_colour,
      e_Yr_E_memory,
      e_Yr_E_overflow,
      e_Yr_E_locked,
      e_Yr_E_unknown
    };

    const s_return_code yaRC_ok                 (e_Yr_ok);
    const s_return_code yaRC_E_allocation       (e_Yr_E_allocation);
    const s_return_code yaRC_E_already_allocated(e_Yr_E_already_allocated);
    const s_return_code yaRC_E_not_allocated    (e_Yr_E_not_allocated);
    const s_return_code yaRC_E_not_implemented  (e_Yr_E_not_implemented);
    const s_return_code yaRC_E_file_io_error    (e_Yr_E_file_io_error);
    const s_return_code yaRC_E_bad_parameters   (e_Yr_E_bad_parameters);
    const s_return_code yaRC_E_null_pointer     (e_Yr_E_null_pointer);
    const s_return_code yaRC_E_not_null_pointer (e_Yr_E_not_null_pointer);
    const s_return_code yaRC_E_unknown          (e_Yr_E_unknown);
    const s_return_code yaRC_E_bad_size         (e_Yr_E_bad_size);
    const s_return_code yaRC_E_memory           (e_Yr_E_memory);
    const s_return_code yaRC_E_overflow         (e_Yr_E_overflow);
    const s_return_code yaRC_E_bad_colour       (e_Yr_E_bad_colour);
    const s_return_code yaRC_E_locked           (e_Yr_E_locked);
    
  };
  
  using namespace return_code_constants;









} // namespace yayi




#endif


