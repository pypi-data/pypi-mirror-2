/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#ifndef YAYI_COMMON_PIXELS_HPP__
#define YAYI_COMMON_PIXELS_HPP__

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/include/common_types_T.hpp>
#include <Yayi/core/yayiCommon/common_pixels_T.hpp>

#include <vector>
#include <map>
#include <list>
#include <complex>
#include <boost/utility/enable_if.hpp>
#include <boost/static_assert.hpp>

//@TODO change the name of this file

namespace yayi
{
  using namespace type_description;


  /*!@brief Helper class for preventing the intanciation of unsupported types
   *
   * Have a look to @ref type_desc for the compilation error this tag may generate.
   * @see type_desc
   * @author Raffi Enficiaud
   */
  template <class U> struct s_identity {
    typedef U support_value_type;
  };


  namespace type_description
  {	


  template <> struct type_support<yaBool> :  public boost::mpl::true_ , public s_identity<yaBool> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_bool;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };

  //! Specializing of type_support for yaUINT8 type
  template <> struct type_support<yaUINT8> :  public boost::mpl::true_ , public s_identity<yaUINT8> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_ui8;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };
  //! Specializing of type_support for yaINT8 type
  template <> struct type_support<yaINT8> :   public boost::mpl::true_ , public s_identity<yaINT8> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_i8;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name(); 
  };

  //! Specializing of type_support for yaUINT16 type
  template <> struct type_support<yaUINT16> :  public boost::mpl::true_ , public s_identity<yaUINT16> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_ui16;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };
  //! Specializing of type_support for yaINT16 type
  template <> struct type_support<yaINT16> :   public boost::mpl::true_ , public s_identity<yaINT16> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_i16;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name(); 
  };

  //! Specializing of type_support for yaUINT32 type
  template <> struct type_support<yaUINT32> :  public boost::mpl::true_ , public s_identity<yaUINT32> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_ui32;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };
  //! Specializing of type_support for yaINT32 type
  template <> struct type_support<yaINT32> :   public boost::mpl::true_ , public s_identity<yaINT32> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_i32;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name(); 
  };

  //! Specializing of type_support for yaUINT64 type
  template <> struct type_support<yaUINT64> :  public boost::mpl::true_ , public s_identity<yaUINT64> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_ui64;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };
  //! Specializing of type_support for yaINT64 type
  template <> struct type_support<yaINT64> :   public boost::mpl::true_ , public s_identity<yaINT64> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_i64;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name(); 
  };

  //! Specializing of type_support for yaF_simple type
  template <> struct type_support<yaF_simple> :  public boost::mpl::true_ , public s_identity<yaF_simple> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_float;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name();
  };
  //! Specializing of type_support for yaF_double type
  template <> struct type_support<yaF_double> :   public boost::mpl::true_ , public s_identity<yaF_double> {
    static const yayi::type::scalar_type scalar    = yayi::type::s_double;
    static const yayi::type::compound_type compound= yayi::type::c_scalar;
    YCom_ static const string_type& name(); 
  };

  //! Specializing of type_support for vector container type
  template <class U> struct type_support< std::vector<U> > : public type_support<U>  {
    static const yayi::type::scalar_type scalar    = type_support<U>::scalar;
    static const yayi::type::compound_type compound= yayi::type::c_vector;
    static const string_type& name();
  };
  
  template <class U> 
    const string_type& type_support< std::vector<U> >::name(){ 
    static const string_type s = "vector<" + type_support<U>::name() + std::string(">");
    return s; 
  }

  //! Specializing of type_support for map container type
  template <class U, class V> struct type_support< std::map<U, V> > : public type_support<U>, public type_support<V>  {
    typedef typename mpl::and_<typename type_support<U>::type, typename type_support<V>::type>::type type;
    typedef type support_value_type;                                                                                // dummy for compile time error check
    static const yayi::type::scalar_type scalar    = yayi::type::s_object/*type_support<U>::compound != type::c_scalar ? s_object : type_support<U>::scalar*/;
    static const yayi::type::compound_type compound= yayi::type::c_map;
    static const string_type& name();
  };
  
  template <class U, class V> 
    const string_type& type_support< std::map<U,V> >::name(){ 
    static const string_type s = "map<" + type_support<U>::name() + std::string(", ") + type_support<V>::name() + std::string(">");
    return s; 
  }



  //! Specializing of type_support for complex container type
  //! @note one should prevent other types than complex<yaF_simple> or complex<yaF_double>
  template <class U> struct type_support< std::complex<U> > : 
    public /*type_support<U>*/mpl::if_<mpl::or_<boost::is_same<U, yaF_simple>, boost::is_same<U, yaF_double> >, type_support<U>, void>::type
  {
    BOOST_STATIC_ASSERT((mpl::or_<boost::is_same<U, yaF_simple>, boost::is_same<U, yaF_double> >::type::value));
    static const yayi::type::scalar_type scalar;
    static const yayi::type::compound_type compound;
    static const string_type& name();
  };
  
  // Raffi: I do not understand why, but GCC cannot make a proper in-body init of the static accross the so/dll boundaries
  // It should be the same for other classes
  // (for instance in types_and_variant_tests.cpp, scalar and compound are refered directly in the source and indirectly from the
  // common_variant.hpp transform_variant function for complexes, the latter being the origin of the problem)
  template <class U> const yayi::type::scalar_type type_support< std::complex<U> >::scalar = type_support<U>::scalar;
  template <class U> const yayi::type::compound_type type_support< std::complex<U> >::compound = yayi::type::c_complex;
  template <class U> 
    const string_type& type_support< std::complex<U> >::name(){ 
    static const string_type s = "complex<" + type_support<U>::name() + std::string(">");
    return s;
  }




  //! Specializing of type_support for generic pixels s_compound_pixel_t container type  (dimension 3)
  template <class U> struct type_support< s_compound_pixel_t<U, mpl::int_<3> > > : public type_support<U>  {
    static const yayi::type::scalar_type scalar    ;//= type_support<U>::scalar;
    static const yayi::type::compound_type compound;//= yayi::type::c_3;
    static const string_type& name();
  };
  template <class U> const yayi::type::scalar_type type_support< s_compound_pixel_t<U, mpl::int_<3> > >::scalar = type_support<U>::scalar;
  template <class U> const yayi::type::compound_type type_support< s_compound_pixel_t<U, mpl::int_<3> > >::compound = yayi::type::c_3;
  template <class U> 
  const string_type& type_support< s_compound_pixel_t<U, mpl::int_<3> > >::name(){ 
    static const string_type s = "s_compound_pixel_t<" + type_support<U>::name() + std::string(", 3>"); 
    return s; 
  }

  //! Specializing of type_support for generic pixels s_compound_pixel_t container type (dimension 4)
  template <class U> struct type_support< s_compound_pixel_t<U, mpl::int_<4> > > : public type_support<U>  {
    static const yayi::type::scalar_type scalar    ;//= type_support<U>::scalar;
    static const yayi::type::compound_type compound;//= yayi::type::c_4;
    static const string_type& name();
  };
  template <class U> const yayi::type::scalar_type type_support< s_compound_pixel_t<U, mpl::int_<4> > >::scalar = type_support<U>::scalar;
  template <class U> const yayi::type::compound_type type_support< s_compound_pixel_t<U, mpl::int_<4> > >::compound = yayi::type::c_4;
  template <class U> 
  const string_type& type_support< s_compound_pixel_t<U, mpl::int_<4> > >::name(){ 
    static const string_type s = "s_compound_pixel_t<" + type_support<U>::name() + std::string(", 4>");
    return s; 
  }


  
  
  
  
  }

}


#endif


