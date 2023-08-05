/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_VARIANT__HPP__
#define YAYI_COMMON_VARIANT__HPP__

/*!@file
 * This file contains the definitions for variant handling
 */

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/include/common_types_T.hpp>
#include <Yayi/core/yayiCommon/common_pixels.hpp>
#include <Yayi/core/yayiCommon/common_pixels_T.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_hyperrectangle.hpp>
#include <Yayi/core/yayiCommon/common_histogram.hpp>
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <boost/utility/enable_if.hpp>

#ifndef NDEBUG
#include <typeinfo>
#endif

namespace yayi {



  //! Types supported by variant. This is more than the types suported by the pixels
  template <class U>
  struct s_variant_type_support
  {
    typedef typename mpl::or_<
      type_support< U >,
      boost::is_same<U, variant>,
      boost::is_same<U, string_type>,
      boost::is_same<U, wide_string_type>
    >::type type;
  };

  //! Types supported by variant, special case of vectors
  template <class U>
  struct s_variant_type_support< std::vector<U> >
  {
    typedef typename s_variant_type_support< U >::type type;
  };

  //! Types supported by variant, special case of maps
  template <class K, class V>
  struct s_variant_type_support< std::map<K, V> >
  {
    typedef typename mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type >::type type;
  };

  //! Types supported by variant, special case of maps
  template <class A, class B>
  struct s_variant_type_support< std::pair<A, B> >
  {
    typedef typename mpl::and_< typename s_variant_type_support< A >::type, typename s_variant_type_support< B >::type >::type type;
  };  
  
  
  //! Types supported by variant, special case of coordinates
  template <int dim>
  struct s_variant_type_support< s_coordinate<dim> >
  {
    typedef mpl::true_ type;
  };

  //! Types supported by variant, special case of coordinates
  template <int dim>
  struct s_variant_type_support< s_hyper_rectangle<dim> >
  {
    typedef mpl::true_ type;
  };


  //! Types supported by variant, special case of maps
  template <class K, class V>
  struct s_variant_type_support< s_histogram_t<K, V> >
  {
    typedef typename mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type >::type type;
  };



  // forward
  template <class U>
  U& variant_field_from_type(variant&);
  
  //! This function cleans the content of a variant (from its runtime type)
  void cleanup_variant(variant& v);
  
  //! This function copies the content of a variant (according to its runtime type)
  void copy_variant(const variant& from, variant& to);
  
  //! This function clones a variant (copy and allocation, without destroying its content)
  void clone_variant_init(const variant& v1, variant& v2);
  
  //! Transformation utility
  template <class U>
  typename boost::enable_if< typename s_variant_type_support<U>::type >::type 
  transform_variant_utility(const U& u, variant &v);
  
  //! Specialization of @transform_variant_utility for vector types
  template <class U>
  typename boost::enable_if< typename s_variant_type_support<U>::type >::type 
  transform_variant_utility(const std::vector<U> &u, variant &v);
  
  //! Specialization of @transform_variant_utility for map types
  template <class K, class V>
  inline typename boost::enable_if< mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type > >::type 
  transform_variant_utility(const std::map<K, V> &u, variant &v);
  
  //! Specialization of @transform_variant_utility for map types
  template <class A, class B>
  inline typename boost::enable_if< typename s_variant_type_support< std::pair<A, B> >::type >::type 
  transform_variant_utility(const std::pair<A, B> &p, variant &v);
  
  //! Specialization of @transform_variant_utility for histogram types
  template <class K, class V>
  inline typename boost::enable_if< mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type > >::type 
  transform_variant_utility(const s_histogram_t<K, V> &u, variant &v);  
  
  //! Specialization of @transform_variant_utility for dimension types
  template <int dim>
  void transform_variant_utility(const s_coordinate<dim>& u, variant &v);

  //! Specialization of @transform_variant_utility for hyperrectangle types
  template <int dim>
  void transform_variant_utility(const s_hyper_rectangle<dim>& u, variant &v);

  
  //void transform_variant_utility(const variant& u, variant &v);
  //! Specialization of @transform_variant_utility for string types
  void transform_variant_utility(const string_type& u, variant &v);
  
  //! Specialization of @transform_variant_utility for wide string types
  void transform_variant_utility(const wide_string_type& u, variant &v);
  
  //! Specialization of @transform_variant_utility for variant types
  //void transform_variant_utility(const variant& u, variant &v);




  
  
  

  //! Structure describing any type of pixel
  struct s_any_type
  {
    type        element_type;
    union
    {
      bool        b_value;
      yaUINT8     ui8_value;
      yaINT8      i8_value;
      yaUINT16    ui16_value;
      yaINT16     i16_value;
      yaUINT32    ui32_value;
      yaINT32     i32_value;
      
      yaUINT64    ui64_value;
      yaINT64     i64_value;
      
      yaF_simple  fs_value;
      yaF_double  fd_value;
      
      std::vector<s_any_type>         *vector_value;
      string_type                     *string_value;
      wide_string_type                *wstring_value;
      
      std::map<int, s_any_type>       *map_value;
      std::list<s_any_type>           *list_value;
      
      s_compound_pixel_t<bool,        mpl::int_<3> >* b_pixel_3;
      s_compound_pixel_t<yaUINT8,     mpl::int_<3> >* ui8_pixel_3;
      s_compound_pixel_t<yaINT8,      mpl::int_<3> >* i8_pixel_3;
      s_compound_pixel_t<yaUINT16,    mpl::int_<3> >* ui16_pixel_3;
      s_compound_pixel_t<yaINT16,     mpl::int_<3> >* i16_pixel_3;
      s_compound_pixel_t<yaUINT32,    mpl::int_<3> >* ui32_pixel_3;
      s_compound_pixel_t<yaINT32,     mpl::int_<3> >* i32_pixel_3;
      s_compound_pixel_t<yaUINT64,    mpl::int_<3> >* ui64_pixel_3;
      s_compound_pixel_t<yaINT64,     mpl::int_<3> >* i64_pixel_3;
      s_compound_pixel_t<yaF_simple,  mpl::int_<3> >* fs_pixel_3;
      s_compound_pixel_t<yaF_double,  mpl::int_<3> >* fd_pixel_3;
      
      s_compound_pixel_t<bool,        mpl::int_<4> >* b_pixel_4;
      s_compound_pixel_t<yaUINT8,     mpl::int_<4> >* ui8_pixel_4;
      s_compound_pixel_t<yaINT8,      mpl::int_<4> >* i8_pixel_4;
      s_compound_pixel_t<yaUINT16,    mpl::int_<4> >* ui16_pixel_4;
      s_compound_pixel_t<yaINT16,     mpl::int_<4> >* i16_pixel_4;
      s_compound_pixel_t<yaUINT32,    mpl::int_<4> >* ui32_pixel_4;
      s_compound_pixel_t<yaINT32,     mpl::int_<4> >* i32_pixel_4;
      s_compound_pixel_t<yaUINT64,    mpl::int_<4> >* ui64_pixel_4;
      s_compound_pixel_t<yaINT64,     mpl::int_<4> >* i64_pixel_4;
      s_compound_pixel_t<yaF_simple,  mpl::int_<4> >* fs_pixel_4;
      s_compound_pixel_t<yaF_double,  mpl::int_<4> >* fd_pixel_4;

      std::complex<yaF_simple>        *fs_complex;
      std::complex<yaF_double>        *fd_complex;
      
      offset                          offset_value;
      
    } element;
    
    
    //! Default constructor
    s_any_type() : element_type(type_undefined) {}
    
    //! Copy constructor
    s_any_type(const s_any_type& c) {
      clone_variant_init(c, *this);
    }
    
    
    /*! Template constructor from any supported type
     * The second argument is not used (dummy). It is here to prevent the instanciation of the constructor
     * with unsupported types, such as s_any_type itself.
     */
    template <class U>
    s_any_type(const U& u, typename boost::enable_if< typename s_variant_type_support< U >::type >::type* dummy = 0) : element_type(type_undefined)
    {
      transform_variant_utility(u, *this);
    }
    
    //! Assignment operator
    s_any_type& operator=(const s_any_type& c)
    {
      copy_variant(c, *this);
      return *this;
    }
    
    //! Destructor
    ~s_any_type()
    {
      cleanup_variant(*this);
    }
    
    
    //! Conversion for default types
    template <class U> operator U() const;
  };
  
  
  // Default behaviour
  //! This template allows to access to a specific field of the variant from the provided type. 
  //! The mapping is exact 1 to 1.
  template <class U>  U& variant_field_from_type(variant&)
  {
    #ifndef NDEBUG
    YAYI_THROW("Unsupported type : " + errors::demangle(typeid(U).name()));
    #else
    YAYI_THROW("Unsupported type");
    #endif
  }
  template <class U>  const U& variant_field_from_type(const variant&)
  {
    #ifndef NDEBUG
    YAYI_THROW("Unsupported type : " + errors::demangle(typeid(U).name()));
    #else
    YAYI_THROW("Unsupported type");
    #endif
  }
  
  
  // Scalar accessors
  template <> inline bool&                variant_field_from_type<bool>       (variant& v)          {return v.element.b_value;    }
  template <> inline yaUINT8&             variant_field_from_type<yaUINT8>    (variant& v)          {return v.element.ui8_value;  }
  template <> inline yaINT8&              variant_field_from_type<yaINT8>     (variant& v)          {return v.element.i8_value;   }
  template <> inline yaUINT16&            variant_field_from_type<yaUINT16>   (variant& v)          {return v.element.ui16_value; }
  template <> inline yaINT16&             variant_field_from_type<yaINT16>    (variant& v)          {return v.element.i16_value;  }
  template <> inline yaUINT32&            variant_field_from_type<yaUINT32>   (variant& v)          {return v.element.ui32_value; }
  template <> inline yaINT32&             variant_field_from_type<yaINT32>    (variant& v)          {return v.element.i32_value;  }
  template <> inline yaUINT64&            variant_field_from_type<yaUINT64>   (variant& v)          {return v.element.ui64_value; }
  template <> inline yaINT64&             variant_field_from_type<yaINT64>    (variant& v)          {return v.element.i64_value;  }
  template <> inline yaF_simple&          variant_field_from_type<yaF_simple> (variant& v)          {return v.element.fs_value;   }
  template <> inline yaF_double&          variant_field_from_type<yaF_double> (variant& v)          {return v.element.fd_value;   }
  
  template <> inline const bool&          variant_field_from_type<bool>       (const variant& v)    {return v.element.b_value;    }
  template <> inline const yaUINT8&       variant_field_from_type<yaUINT8>    (const variant& v)    {return v.element.ui8_value;  }
  template <> inline const yaINT8&        variant_field_from_type<yaINT8>     (const variant& v)    {return v.element.i8_value;   }
  template <> inline const yaUINT16&      variant_field_from_type<yaUINT16>   (const variant& v)    {return v.element.ui16_value; }
  template <> inline const yaINT16&       variant_field_from_type<yaINT16>    (const variant& v)    {return v.element.i16_value;  }
  template <> inline const yaUINT32&      variant_field_from_type<yaUINT32>   (const variant& v)    {return v.element.ui32_value; }
  template <> inline const yaINT32&       variant_field_from_type<yaINT32>    (const variant& v)    {return v.element.i32_value;  }
  template <> inline const yaUINT64&      variant_field_from_type<yaUINT64>   (const variant& v)    {return v.element.ui64_value; }
  template <> inline const yaINT64&       variant_field_from_type<yaINT64>    (const variant& v)    {return v.element.i64_value;  }
  template <> inline const yaF_simple&    variant_field_from_type<yaF_simple> (const variant& v)    {return v.element.fs_value;   }
  template <> inline const yaF_double&    variant_field_from_type<yaF_double> (const variant& v)    {return v.element.fd_value;   }
  
  
  
  // String accessors
  template <> inline string_type&                     variant_field_from_type<string_type>      (variant& v)          {DEBUG_ASSERT(v.element.string_value != 0, "null element");  return *v.element.string_value;   }
  template <> inline wide_string_type&                variant_field_from_type<wide_string_type> (variant& v)          {DEBUG_ASSERT(v.element.wstring_value != 0, "null element"); return *v.element.wstring_value;  }
  
  template <> inline const string_type&               variant_field_from_type<string_type>      (const variant& v)    {DEBUG_ASSERT(v.element.string_value != 0, "null element");  return *v.element.string_value;   }
  template <> inline const wide_string_type&          variant_field_from_type<wide_string_type> (const variant& v)    {DEBUG_ASSERT(v.element.wstring_value != 0, "null element"); return *v.element.wstring_value;  }
  
  // Complex accessors
  template <> inline std::complex<yaF_simple>&        variant_field_from_type< std::complex<yaF_simple> > (variant& v)          {DEBUG_ASSERT(v.element.fs_complex != 0, "null element");  return *v.element.fs_complex;   }
  template <> inline std::complex<yaF_double>&        variant_field_from_type< std::complex<yaF_double> > (variant& v)          {DEBUG_ASSERT(v.element.fd_complex != 0, "null element");  return *v.element.fd_complex;   }
  
  template <> inline const std::complex<yaF_simple>&  variant_field_from_type< std::complex<yaF_simple> > (const variant& v)    {DEBUG_ASSERT(v.element.fs_complex != 0, "null element");  return *v.element.fs_complex;   }
  template <> inline const std::complex<yaF_double>&  variant_field_from_type< std::complex<yaF_double> > (const variant& v)    {DEBUG_ASSERT(v.element.fd_complex != 0, "null element");  return *v.element.fd_complex;   }

  // Vector
  template <> inline std::vector<s_any_type>&         variant_field_from_type< std::vector<s_any_type> > (variant& v)           {DEBUG_ASSERT(v.element.vector_value != 0, "null element"); return *v.element.vector_value;   }
  template <> inline const std::vector<s_any_type>&   variant_field_from_type< std::vector<s_any_type> > (const variant& v)     {DEBUG_ASSERT(v.element.vector_value != 0, "null element"); return *v.element.vector_value;   }
  

  
  
  // Pixel 3 channels accessor
  template <> inline s_compound_pixel_t<bool,       mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<bool,       mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.b_pixel_3 != 0,    "null element");  return *v.element.b_pixel_3;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.ui8_pixel_3 != 0,  "null element");  return *v.element.ui8_pixel_3;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.i8_pixel_3 != 0,   "null element");  return *v.element.i8_pixel_3;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.ui16_pixel_3 != 0, "null element");  return *v.element.ui16_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.i16_pixel_3 != 0,  "null element");  return *v.element.i16_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.ui32_pixel_3 != 0, "null element");  return *v.element.ui32_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.i32_pixel_3 != 0,  "null element");  return *v.element.i32_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.ui64_pixel_3 != 0, "null element");  return *v.element.ui64_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.i64_pixel_3 != 0,  "null element");  return *v.element.i64_pixel_3;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.fs_pixel_3 != 0,   "null element");  return *v.element.fs_pixel_3;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<3> >&  variant_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<3> > > (variant& v)   {DEBUG_ASSERT(v.element.fd_pixel_3 != 0,   "null element");  return *v.element.fd_pixel_3;   }

  template <> inline s_compound_pixel_t<bool,       mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<bool,       mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.b_pixel_3 != 0,    "null element");  return *v.element.b_pixel_3;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui8_pixel_3 != 0,  "null element");  return *v.element.ui8_pixel_3;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.i8_pixel_3 != 0,   "null element");  return *v.element.i8_pixel_3;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui16_pixel_3 != 0, "null element");  return *v.element.ui16_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.i16_pixel_3 != 0,  "null element");  return *v.element.i16_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui32_pixel_3 != 0, "null element");  return *v.element.ui32_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.i32_pixel_3 != 0,  "null element");  return *v.element.i32_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui64_pixel_3 != 0, "null element");  return *v.element.ui64_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.i64_pixel_3 != 0,  "null element");  return *v.element.i64_pixel_3;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.fs_pixel_3 != 0,   "null element");  return *v.element.fs_pixel_3;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<3> > const&  variant_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<3> > > (variant const& v)   {DEBUG_ASSERT(v.element.fd_pixel_3 != 0,   "null element");  return *v.element.fd_pixel_3;   }
  
  // Pixel 4 channels accessor
  template <> inline s_compound_pixel_t<bool,       mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<bool,       mpl::int_<4> > > (variant& v)   {return *v.element.b_pixel_4;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<4> > > (variant& v)   {return *v.element.ui8_pixel_4;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<4> > > (variant& v)   {return *v.element.i8_pixel_4;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<4> > > (variant& v)   {return *v.element.ui16_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<4> > > (variant& v)   {return *v.element.i16_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<4> > > (variant& v)   {return *v.element.ui32_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<4> > > (variant& v)   {return *v.element.i32_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<4> > > (variant& v)   {return *v.element.ui64_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<4> > > (variant& v)   {return *v.element.i64_pixel_4;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<4> > > (variant& v)   {return *v.element.fs_pixel_4;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<4> >&  variant_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<4> > > (variant& v)   {return *v.element.fd_pixel_4;   }
  
  template <> inline s_compound_pixel_t<bool,       mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<bool,       mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.b_pixel_4 != 0,    "null element"); return *v.element.b_pixel_4;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui8_pixel_4 != 0,  "null element"); return *v.element.ui8_pixel_4;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.i8_pixel_4 != 0,   "null element"); return *v.element.i8_pixel_4;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui16_pixel_4 != 0, "null element"); return *v.element.ui16_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.i16_pixel_4 != 0,  "null element"); return *v.element.i16_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui32_pixel_4 != 0, "null element"); return *v.element.ui32_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.i32_pixel_4 != 0,  "null element"); return *v.element.i32_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.ui64_pixel_4 != 0, "null element"); return *v.element.ui64_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.i64_pixel_4 != 0,  "null element"); return *v.element.i64_pixel_4;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.fs_pixel_4 != 0,   "null element"); return *v.element.fs_pixel_4;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<4> > const&  variant_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<4> > > (variant const& v)   {DEBUG_ASSERT(v.element.fd_pixel_4 != 0,   "null element"); return *v.element.fd_pixel_4;   }
  
  
  template <class T> inline T*& pointer_field_from_type(variant& v); // no implementation  
  // String accessors to pointers
  template <> inline string_type*&                     pointer_field_from_type<string_type>      (variant& v)                    {return v.element.string_value;   }
  template <> inline wide_string_type*&                pointer_field_from_type<wide_string_type> (variant& v)                    {return v.element.wstring_value;  }
  
  // Complex accessors to pointers
  template <> inline std::complex<yaF_simple>*&        pointer_field_from_type< std::complex<yaF_simple> > (variant& v)          {return v.element.fs_complex;   }
  template <> inline std::complex<yaF_double>*&        pointer_field_from_type< std::complex<yaF_double> > (variant& v)          {return v.element.fd_complex;   }
  
  // Vector to pointers
  template <> inline std::vector<s_any_type>*&         pointer_field_from_type< std::vector<s_any_type> > (variant& v)           {return v.element.vector_value;   }
  

  
  
  // Pixel 3 channels accessor to pointers
  template <> inline s_compound_pixel_t<bool,       mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<bool,       mpl::int_<3> > > (variant& v)   {return v.element.b_pixel_3;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<3> > > (variant& v)   {return v.element.ui8_pixel_3;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<3> > > (variant& v)   {return v.element.i8_pixel_3;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<3> > > (variant& v)   {return v.element.ui16_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<3> > > (variant& v)   {return v.element.i16_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<3> > > (variant& v)   {return v.element.ui32_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<3> > > (variant& v)   {return v.element.i32_pixel_3;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<3> > > (variant& v)   {return v.element.ui64_pixel_3; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<3> > > (variant& v)   {return v.element.i64_pixel_3;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<3> > > (variant& v)   {return v.element.fs_pixel_3;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<3> >*&  pointer_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<3> > > (variant& v)   {return v.element.fd_pixel_3;   }
  
  // Pixel 4 channels accessor to pointers
  template <> inline s_compound_pixel_t<bool,       mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<bool,       mpl::int_<4> > > (variant& v)   {return v.element.b_pixel_4;    }
  template <> inline s_compound_pixel_t<yaUINT8,    mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT8,    mpl::int_<4> > > (variant& v)   {return v.element.ui8_pixel_4;  }
  template <> inline s_compound_pixel_t<yaINT8,     mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT8,     mpl::int_<4> > > (variant& v)   {return v.element.i8_pixel_4;   }
  template <> inline s_compound_pixel_t<yaUINT16,   mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT16,   mpl::int_<4> > > (variant& v)   {return v.element.ui16_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT16,    mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT16,    mpl::int_<4> > > (variant& v)   {return v.element.i16_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT32,   mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT32,   mpl::int_<4> > > (variant& v)   {return v.element.ui32_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT32,    mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT32,    mpl::int_<4> > > (variant& v)   {return v.element.i32_pixel_4;  }
  template <> inline s_compound_pixel_t<yaUINT64,   mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaUINT64,   mpl::int_<4> > > (variant& v)   {return v.element.ui64_pixel_4; }
  template <> inline s_compound_pixel_t<yaINT64,    mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaINT64,    mpl::int_<4> > > (variant& v)   {return v.element.i64_pixel_4;  }
  template <> inline s_compound_pixel_t<yaF_simple, mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaF_simple, mpl::int_<4> > > (variant& v)   {return v.element.fs_pixel_4;   }
  template <> inline s_compound_pixel_t<yaF_double, mpl::int_<4> >*&  pointer_field_from_type<s_compound_pixel_t<yaF_double, mpl::int_<4> > > (variant& v)   {return v.element.fd_pixel_4;   }
  


  template <class U>
  inline void clean_stack_element(variant& v)
  {
    U* &u = pointer_field_from_type<U>(v);
    delete u;
    u = 0;
    v.element_type.c_type = type::c_unknown;
    v.element_type.s_type = type::s_undefined;
  }
         
  inline void cleanup_variant(variant& v)
  {
    //! TODO a completer
    switch(v.element_type.c_type){
      case type::c_unknown:
      case type::c_scalar:
        switch(v.element_type.s_type)
        {
          case type::s_string:
            clean_stack_element< string_type >(v);
            break;
          case type::s_wstring:
            clean_stack_element< wide_string_type >(v);
            break;
          default:
            break;
        }
        break;
      
      case type::c_3:
        switch(v.element_type.s_type)
        {
          case type::s_bool:      clean_stack_element< s_compound_pixel_t<bool,       mpl::int_<3> > >(v); break;
          case type::s_ui8:       clean_stack_element< s_compound_pixel_t<yaUINT8,    mpl::int_<3> > >(v); break;
          case type::s_i8:        clean_stack_element< s_compound_pixel_t<yaINT8,     mpl::int_<3> > >(v); break;
          case type::s_ui16:      clean_stack_element< s_compound_pixel_t<yaUINT16,   mpl::int_<3> > >(v); break;
          case type::s_i16:       clean_stack_element< s_compound_pixel_t<yaINT16,    mpl::int_<3> > >(v); break;
          case type::s_ui32:      clean_stack_element< s_compound_pixel_t<yaUINT32,   mpl::int_<3> > >(v); break;
          case type::s_i32:       clean_stack_element< s_compound_pixel_t<yaINT32,    mpl::int_<3> > >(v); break;
          case type::s_ui64:      clean_stack_element< s_compound_pixel_t<yaUINT64,   mpl::int_<3> > >(v); break;
          case type::s_i64:       clean_stack_element< s_compound_pixel_t<yaINT64,    mpl::int_<3> > >(v); break;
          case type::s_float:     clean_stack_element< s_compound_pixel_t<yaF_simple, mpl::int_<3> > >(v); break;
          case type::s_double:    clean_stack_element< s_compound_pixel_t<yaF_double, mpl::int_<3> > >(v); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v.element_type));
            break;
        }
        break;      
      case type::c_4:
        switch(v.element_type.s_type)
        {
          case type::s_bool:      clean_stack_element< s_compound_pixel_t<bool,       mpl::int_<4> > >(v); break;
          case type::s_ui8:       clean_stack_element< s_compound_pixel_t<yaUINT8,    mpl::int_<4> > >(v); break;
          case type::s_i8:        clean_stack_element< s_compound_pixel_t<yaINT8,     mpl::int_<4> > >(v); break;
          case type::s_ui16:      clean_stack_element< s_compound_pixel_t<yaUINT16,   mpl::int_<4> > >(v); break;
          case type::s_i16:       clean_stack_element< s_compound_pixel_t<yaINT16,    mpl::int_<4> > >(v); break;
          case type::s_ui32:      clean_stack_element< s_compound_pixel_t<yaUINT32,   mpl::int_<4> > >(v); break;
          case type::s_i32:       clean_stack_element< s_compound_pixel_t<yaINT32,    mpl::int_<4> > >(v); break;
          case type::s_ui64:      clean_stack_element< s_compound_pixel_t<yaUINT64,   mpl::int_<4> > >(v); break;
          case type::s_i64:       clean_stack_element< s_compound_pixel_t<yaINT64,    mpl::int_<4> > >(v); break;
          case type::s_float:     clean_stack_element< s_compound_pixel_t<yaF_simple, mpl::int_<4> > >(v); break;
          case type::s_double:    clean_stack_element< s_compound_pixel_t<yaF_double, mpl::int_<4> > >(v); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v.element_type));
            break;
        }
        break;      
      case type::c_vector:
        clean_stack_element< std::vector<s_any_type> >(v);
        break;
      case type::c_complex:
        switch(v.element_type.s_type)
        {
          case type::s_float:     clean_stack_element< std::complex<yaF_simple> >(v); break;
          case type::s_double:    clean_stack_element< std::complex<yaF_double> >(v); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v.element_type));
            break;
        }
        break;
        
      default:

        YAYI_THROW("Undefined type " + string_type(v.element_type));
        break;
    }
  }
  


  //! Checks if the element of the variant is of the same type
  inline bool variants_same_type(const variant& v1, const variant& v2) {
    return v1.element_type == v2.element_type;
  }
  
  inline bool variants_same_type(const variant& v1, const type& t) {
    return v1.element_type == t;
  }
  
  inline bool variants_same_type(const variant& v1, const type::e_scalar_type& s, const type::e_compound_type& c) {
    return v1.element_type.s_type == s && v1.element_type.c_type == c;
  }
  
  
  namespace 
  {

    template <class T>
    void variant_copy_helper(variant const &v1, variant &v2, bool cleanup)
    {
      if(cleanup)
        pointer_field_from_type<T>(v2) = new T(variant_field_from_type<T>(v1));
      else
        variant_field_from_type<T>(v2) = variant_field_from_type<T>(v1);    
    }

    template <class T>
    void variant_init_clone_helper(variant const &v1, variant &v2)
    {
      pointer_field_from_type<T>(v2) = new T(variant_field_from_type<T>(v1));
    }
  }
  
  inline void copy_variant(const variant& v1, variant& v2) {
    if(v1.element_type == type_undefined)
    {
      cleanup_variant(v2);
      v2.element_type = v1.element_type;
      return;
    }  
    // Simple cases before
    if(v1.element_type.c_type == type::c_scalar)
    {
      if((v2.element_type.c_type != type::c_scalar) && (v2.element_type.c_type != type::c_unknown) )
      {
        cleanup_variant(v2);
        // v2.element_type = v1.element_type;
      }
      
       // TODO faire un test unitaire sur ce bug       
      if(v1.element_type.s_type == type::s_string)
      {
        if(v2.element_type.s_type != type::s_string)
          cleanup_variant(v2);
        variant_copy_helper<string_type>(v1, v2, v2.element_type.s_type != type::s_string);
        //v2.element.string_value = new string_type(*v1.element.string_value); // <- ici on écase un pointer
      }
      else if(v1.element_type.s_type == type::s_wstring)
      {
        if(v2.element_type.s_type != type::s_wstring)
          cleanup_variant(v2);
        variant_copy_helper<wide_string_type>(v1, v2, v2.element_type.s_type != type::s_string);
        //v2.element.wstring_value = new wide_string_type(*v1.element.wstring_value); // pareil
      }
      else
      {
        v2.element = v1.element;
      }
      
      v2.element_type = v1.element_type;
      
      return;
    }

    // we perform the cleanup if and only if the types are different (which avoids one allocation)
    bool b_cleanup = (v1.element_type != v2.element_type);
    if(b_cleanup)
      cleanup_variant(v2);

    switch(v1.element_type.c_type)
    {
    case type::c_vector:
      if(b_cleanup)
        v2.element.vector_value = new std::vector<variant>();
      variant_field_from_type< std::vector<s_any_type> >(v2) = variant_field_from_type< std::vector<s_any_type> >( v1 );
      break;
    case type::c_complex:
    {
      switch(v1.element_type.s_type)
      {
        case type::s_float: variant_copy_helper< std::complex<yaF_simple> >(v1, v2, b_cleanup); break;
        case type::s_double: variant_copy_helper< std::complex<yaF_double> >(v1, v2, b_cleanup); break;
        default:
          YAYI_THROW("Undefined type " + string_type(v1.element_type));
          break;
      }
      break;
    }
    case type::c_3:
    {
      switch(v1.element_type.s_type)
      {
          case type::s_bool:      variant_copy_helper< s_compound_pixel_t<bool,       mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_ui8:       variant_copy_helper< s_compound_pixel_t<yaUINT8,    mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_i8:        variant_copy_helper< s_compound_pixel_t<yaINT8,     mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_ui16:      variant_copy_helper< s_compound_pixel_t<yaUINT16,   mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_i16:       variant_copy_helper< s_compound_pixel_t<yaINT16,    mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_ui32:      variant_copy_helper< s_compound_pixel_t<yaUINT32,   mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_i32:       variant_copy_helper< s_compound_pixel_t<yaINT32,    mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_ui64:      variant_copy_helper< s_compound_pixel_t<yaUINT64,   mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_i64:       variant_copy_helper< s_compound_pixel_t<yaINT64,    mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_float:     variant_copy_helper< s_compound_pixel_t<yaF_simple, mpl::int_<3> > >(v1, v2, b_cleanup); break;
          case type::s_double:    variant_copy_helper< s_compound_pixel_t<yaF_double, mpl::int_<3> > >(v1, v2, b_cleanup); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v1.element_type));
            break;
      }
      break;
    }
    case type::c_4:
    {
      switch(v1.element_type.s_type)
      {
          case type::s_bool:      variant_copy_helper< s_compound_pixel_t<bool,       mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_ui8:       variant_copy_helper< s_compound_pixel_t<yaUINT8,    mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_i8:        variant_copy_helper< s_compound_pixel_t<yaINT8,     mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_ui16:      variant_copy_helper< s_compound_pixel_t<yaUINT16,   mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_i16:       variant_copy_helper< s_compound_pixel_t<yaINT16,    mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_ui32:      variant_copy_helper< s_compound_pixel_t<yaUINT32,   mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_i32:       variant_copy_helper< s_compound_pixel_t<yaINT32,    mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_ui64:      variant_copy_helper< s_compound_pixel_t<yaUINT64,   mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_i64:       variant_copy_helper< s_compound_pixel_t<yaINT64,    mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_float:     variant_copy_helper< s_compound_pixel_t<yaF_simple, mpl::int_<4> > >(v1, v2, b_cleanup); break;
          case type::s_double:    variant_copy_helper< s_compound_pixel_t<yaF_double, mpl::int_<4> > >(v1, v2, b_cleanup); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v1.element_type));
            break;
      }
      break;
    }

    default:
      YAYI_THROW("Undefined type " + string_type(v1.element_type));
      break;
    }
    v2.element_type = v1.element_type;    
  }
  
   
  
  inline void clone_variant_init(const variant& v1, variant& v2) {
    if(v1.element_type == type_undefined)
    {
      v2.element_type = type_undefined;
      return;
    }
    
    // Simple cases before
    if(v1.element_type.c_type == type::c_scalar) {
      
      if(v1.element_type.s_type == type::s_string)
      {
        variant_init_clone_helper<string_type>(v1, v2);
      }
      else if(v1.element_type.s_type == type::s_wstring)
      {
        variant_init_clone_helper<wide_string_type>(v1, v2);
      }
      else
        v2.element = v1.element;
      v2.element_type = v1.element_type;      
      return;
    }
    
    switch(v1.element_type.c_type)
    {
    case type::c_vector:
      v2.element.vector_value = new std::vector<variant>();
      variant_field_from_type< std::vector<s_any_type> >(v2) = variant_field_from_type< std::vector<s_any_type> >( v1 );
      break;
   
    case type::c_complex:
    {
      switch(v1.element_type.s_type)
      {
        case type::s_float:  variant_init_clone_helper< std::complex<yaF_simple> >(v1, v2); break;
        case type::s_double: variant_init_clone_helper< std::complex<yaF_double> >(v1, v2); break;
        default:
          YAYI_THROW("Undefined type " + string_type(v1.element_type));
          break;
      }
      break;
    }
    case type::c_3:
    {
      switch(v1.element_type.s_type)
      {
          case type::s_bool:      variant_init_clone_helper< s_compound_pixel_t<bool,       mpl::int_<3> > >(v1, v2); break;
          case type::s_ui8:       variant_init_clone_helper< s_compound_pixel_t<yaUINT8,    mpl::int_<3> > >(v1, v2); break;
          case type::s_i8:        variant_init_clone_helper< s_compound_pixel_t<yaINT8,     mpl::int_<3> > >(v1, v2); break;
          case type::s_ui16:      variant_init_clone_helper< s_compound_pixel_t<yaUINT16,   mpl::int_<3> > >(v1, v2); break;
          case type::s_i16:       variant_init_clone_helper< s_compound_pixel_t<yaINT16,    mpl::int_<3> > >(v1, v2); break;
          case type::s_ui32:      variant_init_clone_helper< s_compound_pixel_t<yaUINT32,   mpl::int_<3> > >(v1, v2); break;
          case type::s_i32:       variant_init_clone_helper< s_compound_pixel_t<yaINT32,    mpl::int_<3> > >(v1, v2); break;
          case type::s_ui64:      variant_init_clone_helper< s_compound_pixel_t<yaUINT64,   mpl::int_<3> > >(v1, v2); break;
          case type::s_i64:       variant_init_clone_helper< s_compound_pixel_t<yaINT64,    mpl::int_<3> > >(v1, v2); break;
          case type::s_float:     variant_init_clone_helper< s_compound_pixel_t<yaF_simple, mpl::int_<3> > >(v1, v2); break;
          case type::s_double:    variant_init_clone_helper< s_compound_pixel_t<yaF_double, mpl::int_<3> > >(v1, v2); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v1.element_type));
            break;
      }
      break;
    }
    case type::c_4:
    {
      switch(v1.element_type.s_type)
      {
          case type::s_bool:      variant_init_clone_helper< s_compound_pixel_t<bool,       mpl::int_<4> > >(v1, v2); break;
          case type::s_ui8:       variant_init_clone_helper< s_compound_pixel_t<yaUINT8,    mpl::int_<4> > >(v1, v2); break;
          case type::s_i8:        variant_init_clone_helper< s_compound_pixel_t<yaINT8,     mpl::int_<4> > >(v1, v2); break;
          case type::s_ui16:      variant_init_clone_helper< s_compound_pixel_t<yaUINT16,   mpl::int_<4> > >(v1, v2); break;
          case type::s_i16:       variant_init_clone_helper< s_compound_pixel_t<yaINT16,    mpl::int_<4> > >(v1, v2); break;
          case type::s_ui32:      variant_init_clone_helper< s_compound_pixel_t<yaUINT32,   mpl::int_<4> > >(v1, v2); break;
          case type::s_i32:       variant_init_clone_helper< s_compound_pixel_t<yaINT32,    mpl::int_<4> > >(v1, v2); break;
          case type::s_ui64:      variant_init_clone_helper< s_compound_pixel_t<yaUINT64,   mpl::int_<4> > >(v1, v2); break;
          case type::s_i64:       variant_init_clone_helper< s_compound_pixel_t<yaINT64,    mpl::int_<4> > >(v1, v2); break;
          case type::s_float:     variant_init_clone_helper< s_compound_pixel_t<yaF_simple, mpl::int_<4> > >(v1, v2); break;
          case type::s_double:    variant_init_clone_helper< s_compound_pixel_t<yaF_double, mpl::int_<4> > >(v1, v2); break;
          default:
            YAYI_THROW("Undefined type " + string_type(v1.element_type));
            break;
      }
      break;
    }
    default:
      YAYI_THROW("Undefined type " + string_type(v1.element_type));
      break;
    }
    
    v2.element_type = v1.element_type;
  }
  
  
  
  
  /*!@brief Assign a variant from the provided variable
   *
   * The variant is given the value and the type of the input value u
   */
  template <class U>  
  inline typename boost::enable_if< typename s_variant_type_support<U>::type >::type 
  transform_variant_utility(const U& u, variant &v)
  {
    cleanup_variant(v);
    v.element_type.c_type = type_support<U>::compound;
    v.element_type.s_type = type_support<U>::scalar;
    variant_field_from_type<U>(v) = u;
  }
  
  template <class U>
  inline typename boost::enable_if< typename s_variant_type_support< U >::type >::type 
  transform_variant_utility(const std::vector<U> &u, variant &v) 
  {
    if(!variants_same_type(v, type::s_undefined, type::c_vector)) {
      if(v.element_type.c_type != type::c_scalar)
        cleanup_variant(v);
      v.element_type.c_type = type::c_vector;
      v.element_type.s_type = type::s_undefined;
      v.element.vector_value = new std::vector<variant>(u.begin(), u.end());            
    }
    else {
      if(!v.element.vector_value)
        v.element.vector_value = new std::vector<variant>(u.begin(), u.end());
      else
        v.element.vector_value->assign(u.begin(), u.end());
    }

    /*
    // TODO : faire un constructeur par recopie + assignation pour variant
    for(typename std::vector<U>::size_type i = 0, j = u.size(); i < j; i++)
    {
      (*v.element.vector_value).push_back(u[i]);
    }
    */
  }
  
  template <int dim>
  void transform_variant_utility(const s_coordinate<dim>& u, variant &v)
  {
    typedef s_coordinate<dim> coordinate_type;
    std::vector<typename coordinate_type::scalar_coordinate_type> vv;
    for(int i = 0, j = u.dimension(); i < j; i++)
      vv.push_back(u[i]); // dimension here, we cannot rely on dim because of the 0
    transform_variant_utility(vv, v);
  }


  template <int dim>
  void transform_variant_utility(const s_hyper_rectangle<dim>& u, variant &v)
  {
    std::vector<variant> vect;
    vect.push_back(u.lowerleft_corner);
    vect.push_back(u.Size());
    transform_variant_utility(vect, v);
  }





  template <class U>
  inline typename boost::enable_if< typename s_variant_type_support< std::complex<U> >::type >::type 
  transform_variant_utility(const std::complex<U> &u, variant &v) 
  {
    typedef std::complex<U> complex_t;
    if(!variants_same_type(v, type_description::type_support< complex_t >::scalar, type_description::type_support< complex_t >::compound)) {
      cleanup_variant(v);
      v.element_type.c_type = type_description::type_support< complex_t >::compound;
      v.element_type.s_type = type_description::type_support< complex_t >::scalar;
      pointer_field_from_type<complex_t>(v) = new complex_t(u);            
    }
    else 
    {
      if(!pointer_field_from_type<complex_t>(v))
        pointer_field_from_type<complex_t>(v) = new complex_t(u); 
      else
        variant_field_from_type<complex_t>(v) = u;
    }
  }

  template <class U, class D>
  inline typename boost::enable_if< typename s_variant_type_support< s_compound_pixel_t<U, D> >::type >::type 
  transform_variant_utility(const s_compound_pixel_t<U, D> &u, variant &v) 
  {
    typedef s_compound_pixel_t<U, D> pixel_t;
    if(!variants_same_type(v, type_description::type_support< pixel_t >::scalar, type_description::type_support< pixel_t >::compound)) {
      cleanup_variant(v);
      v.element_type.c_type = type_description::type_support< pixel_t >::compound;
      v.element_type.s_type = type_description::type_support< pixel_t >::scalar;
      pointer_field_from_type<pixel_t>(v) = new pixel_t(u);            
    }
    else 
    {
      if(!pointer_field_from_type<pixel_t>(v))
        pointer_field_from_type<pixel_t>(v) = new pixel_t(u); 
      else
        variant_field_from_type<pixel_t>(v) = u;
    }
  }


  template <class K, class V>
  inline typename boost::enable_if< mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type > >::type 
  transform_variant_utility(const std::map<K, V> &u, variant &v) 
  {
    if(!variants_same_type(v, type::s_undefined, type::c_vector)) {
      if(v.element_type.c_type != type::c_scalar)
        cleanup_variant(v);
      v.element_type.c_type = type::c_vector;
      v.element_type.s_type = type::s_undefined;
      v.element.vector_value = new std::vector<variant>();            
    }
    else {
      if(!v.element.vector_value)
        v.element.vector_value = new std::vector<variant>();
      else
        v.element.vector_value->clear();
    }

    // TODO : faire un constructeur par recopie + assignation pour variant
    for(typename std::map<K, V>::const_iterator it(u.begin()), ite(u.end()); it != ite; ++it)
    {
      std::vector<variant> vv;
      vv.push_back(it->first);
      vv.push_back(it->second);
      v.element.vector_value->push_back(variant(vv));
    }
  }
  
  
  
  namespace {
    template <class hist_t, class repr_t>
    struct s_histogram_variant_utility
    {
      void operator()(const hist_t& h, variant &v)
      {
        std::vector<variant> vv;
        for(typename hist_t::const_iterator it(h.begin()), ite(h.end()); it != ite; ++it)
        {
          vv.push_back(variant(std::make_pair(it->first, it->second)));
        }
        v = vv;
      }    
    };

    template <class hist_t, class U>
    struct s_histogram_variant_utility< hist_t, std::vector<U> >
    {
      void operator()(const hist_t& h, variant &v)
      {
        std::vector<variant> vv;
        for(typename hist_t::bin_type i = h.min_bin(), j = h.max_bin(); i < j; i++)
        {
          if(h[i] > 0)
          {
            vv.push_back(variant(std::make_pair(i, h[i])));
          }
        }
        v = vv;
      }
    
    };
  
  }
  
  
  
  template <class K, class V>
  inline typename boost::enable_if< mpl::and_< typename s_variant_type_support< K >::type, typename s_variant_type_support< V >::type > >::type 
  transform_variant_utility(const s_histogram_t<K, V> &u, variant &v) 
  {
    typedef s_histogram_t<K, V> hist_t;
    s_histogram_variant_utility<hist_t, typename hist_t::representation_type> helper;
    helper(u, v);
  }
  
  
  template <class A, class B>
  inline typename boost::enable_if< typename s_variant_type_support< std::pair<A, B> >::type >::type 
  transform_variant_utility(const std::pair<A, B>&u, variant &v) 
  {
    std::vector<variant> vect;
    vect.push_back(u.first);
    vect.push_back(u.second);
    transform_variant_utility(vect, v);
  }
  
  inline void transform_variant_utility(const string_type& u, variant &v)
  {
    if(!variants_same_type(v, type::s_string, type::c_scalar))
      cleanup_variant(v);
    v.element_type.c_type = type::c_scalar;
    v.element_type.s_type = type::s_string;
    v.element.string_value = new string_type(u);
  }
  
  inline void transform_variant_utility(const wide_string_type& u, variant &v)
  {
    if(!variants_same_type(v, type::s_wstring, type::c_scalar))
      cleanup_variant(v);
    v.element_type.c_type = type::c_scalar;
    v.element_type.s_type = type::s_wstring;
    v.element.wstring_value = new wide_string_type(u);
  }
  
  
  
#if 0
  template <class U>  typename boost::disable_if< typename s_variant_type_support<U>::type >::type transform_variant_utility(U, variant &)
  { 
#ifdef YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
    BOOST_STATIC_ASSERT(false);
#endif
    YAYI_THROW(std::string("Unsupported type for variant conversion : ") + typeof(U).name());
  }
#endif
  
  
  template <class U>
  struct s_variant_partial_specialization_helper
  {

    U operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_scalar)
        YAYI_THROW("The containted type is not scalar !: contained type is " + string_type(v.element_type));
    
      // Any scalar type should be convertible to U
      BOOST_STATIC_ASSERT((is_convertible<yaUINT32, U>::value));
    
      switch(v.element_type.s_type)
      {
      case type::s_bool:
          return static_cast<U>(  variant_field_from_type<yaBool>     (v) );
      case type::s_ui8:
          return static_cast<U>(  variant_field_from_type<yaUINT8>    (v) );
      case type::s_i8:
          return static_cast<U>(  variant_field_from_type<yaINT8>     (v) );
      case type::s_ui16:
          return static_cast<U>(  variant_field_from_type<yaUINT16>   (v) );
      case type::s_i16:
          return static_cast<U>(  variant_field_from_type<yaINT16>    (v) );
      case type::s_ui32:
          return static_cast<U>(  variant_field_from_type<yaUINT32>   (v) );
      case type::s_i32:
          return static_cast<U>(  variant_field_from_type<yaINT32>    (v) );
      case type::s_ui64:
          return static_cast<U>(  variant_field_from_type<yaUINT64>   (v) );
      case type::s_i64:
          return static_cast<U>(  variant_field_from_type<yaINT64>    (v) );
      case type::s_float:
          return static_cast<U>(  variant_field_from_type<yaF_simple> (v) );
      case type::s_double:
          return static_cast<U>(  variant_field_from_type<yaF_double> (v) );
      default:
          YAYI_THROW("Undefined type " + string_type(v.element_type));
      }
    }
  
  };

  template <>
  struct s_variant_partial_specialization_helper<bool>
  {
    typedef bool U;

    U operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_scalar)
        YAYI_THROW("The containted type is not scalar !: contained type is " + string_type(v.element_type));
    
      switch(v.element_type.s_type)
      {
      case type::s_bool:
          return static_cast<U>(  variant_field_from_type<yaBool>     (v) );
      case type::s_ui8:
          return static_cast<U>(  variant_field_from_type<yaUINT8>    (v) != 0);
      case type::s_i8:
          return static_cast<U>(  variant_field_from_type<yaINT8>     (v) != 0);
      case type::s_ui16:
          return static_cast<U>(  variant_field_from_type<yaUINT16>   (v) != 0);
      case type::s_i16:
          return static_cast<U>(  variant_field_from_type<yaINT16>    (v) != 0);
      case type::s_ui32:
          return static_cast<U>(  variant_field_from_type<yaUINT32>   (v) != 0);
      case type::s_i32:
          return static_cast<U>(  variant_field_from_type<yaINT32>    (v) != 0);
      case type::s_ui64:
          return static_cast<U>(  variant_field_from_type<yaUINT64>   (v) != 0);
      case type::s_i64:
          return static_cast<U>(  variant_field_from_type<yaINT64>    (v) != 0);
      default:
          YAYI_THROW("Undefined type " + string_type(v.element_type));
      }
    }
  
  };


  
  template <class U, class dimension>
  struct s_variant_partial_specialization_helper< yayi::s_compound_pixel_t<U, dimension> >
  {
    typedef s_compound_pixel_t<U, dimension> return_type;
    
    return_type operator()(const variant& v) const
    {
      if(v.element_type.c_type != type_description::type_support<return_type>::compound)
        YAYI_THROW("The contained type is not a pixel type (" + type_description::type_support<return_type>::name() + ")! contained type is " + string_type(v.element_type));
      
      switch(v.element_type.s_type)
      {
        case type::s_ui8:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaUINT8, dimension> >    (v) );
        case type::s_i8:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaINT8, dimension> >     (v) );
        case type::s_ui16:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaUINT16, dimension> >   (v) );
        case type::s_i16:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaINT16, dimension> >    (v) );
        case type::s_ui32:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaUINT32, dimension> >   (v) );
        case type::s_i32:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaINT32, dimension> >    (v) );
        case type::s_ui64:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaUINT64, dimension> >   (v) );
        case type::s_i64:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaINT64, dimension> >    (v) );
      case type::s_float:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaF_simple, dimension> > (v) );
      case type::s_double:
          return static_cast<return_type>(  variant_field_from_type<s_compound_pixel_t<yaF_double, dimension> > (v) );
      default:
          YAYI_THROW("Undefined type " + string_type(v.element_type));
      }
    }
  };
  
  
  template <class U>
  struct s_variant_partial_specialization_helper< std::complex<U> >
  {
    typedef std::complex<U> return_type;

    return_type operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_complex && v.element_type.c_type != type::c_scalar)
        YAYI_THROW("The contained type is not complex nor scalar ! (contained type is " + string_type(v.element_type) + ")");
    
      switch(v.element_type.s_type)
      {
        case type::s_float:
          return static_cast<return_type>(  variant_field_from_type< std::complex<yaF_simple> >(v));
        case type::s_double:
          return static_cast<return_type>(  variant_field_from_type< std::complex<yaF_double> >(v));
        default:
          YAYI_THROW("Unsupported type " + int_to_string(v.element_type.s_type));
      }
    }
  };



  
  
  template <class U>
  struct s_variant_partial_specialization_helper< std::vector<U> >
  {
    typedef std::vector<U> return_type;
  
    return_type operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_vector)
        YAYI_THROW("Unable to transform a type " + string_type(v.element_type) + std::string(" into a vector type"));
    
      DEBUG_ASSERT(v.element.vector_value != 0, "The vector has not been initialized");
      std::vector<U> out;
      for(typename std::vector<s_any_type>::size_type i = 0, j = v.element.vector_value->size(); i < j; i++)
      {
        out.push_back( (*v.element.vector_value)[i] );
      }
      return out;
    }
  }; 

  template <int dim>
  struct s_variant_partial_specialization_helper< s_coordinate<dim> >
  {
    typedef s_coordinate<dim> return_type;
  
    return_type operator()(const variant& v) const
    {
      typedef std::vector<typename return_type::scalar_coordinate_type> intermediate_t;
      s_variant_partial_specialization_helper< intermediate_t > op;
      intermediate_t vect = op(v);
      return_type out;
      out.set_dimension(vect.size());
      
      for(int i = 0, j = vect.size(); i < j; i++)
      {
        out[i] = vect[i];
      }
      return out;
    }
  }; 

  template <int dim>
  struct s_variant_partial_specialization_helper< s_hyper_rectangle<dim> >
  {
    typedef s_hyper_rectangle<dim> return_type;
  
    return_type operator()(const variant& v) const
    {
      std::vector< s_coordinate<dim> > vect = v;
      if(vect.size() != 2)
        YAYI_THROW("Unable to transform a type " + string_type(v.element_type) + std::string(" into a hyperrectangle type"));
      return return_type(vect[0], vect[1]);
    }
  }; 

  
  template <class K, class V>
  struct s_variant_partial_specialization_helper< std::map<K, V> >
  {
    typedef std::map<K, V> return_type;
  
    return_type operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_vector)// && v.element_type.c_type != type::c_map) // map not supported here
        YAYI_THROW("Unable to transform a type " + string_type(v.element_type) + std::string(" into a map type"));
    
    
      if(v.element_type.c_type == type::c_vector)
      {
        DEBUG_ASSERT(v.element.vector_value != 0, "The vector has not been initialized");
        return_type out;
        s_variant_partial_specialization_helper<typename return_type::mapped_type>  value_op;
        s_variant_partial_specialization_helper<typename return_type::key_type>     key_op;
        for(typename std::vector<s_any_type>::size_type i = 0, j = v.element.vector_value->size(); i < j; i++)
        {
          const s_any_type& current = (*v.element.vector_value)[i];
          if(current.element_type.c_type != type::c_vector)
            YAYI_THROW("Unable to transform a type " + string_type(current.element_type) + string_type(" into a vector type (inner type of a map type for element " + int_to_string(i) + ")"));
          
          if(current.element.vector_value == 0 || current.element.vector_value->size() != 2)
            YAYI_THROW("Bad element configuration for inner vector of a map (element " + int_to_string(i) + ") : either null or of bad size");
          
          typename return_type::value_type val = std::make_pair(key_op((*current.element.vector_value)[0]), value_op((*current.element.vector_value)[1]));
          out.insert( val );
        }
        return out;
      }
      YAYI_THROW("Should never execute here");
    }
  }; 
  
  template <class A, class B>
  struct s_variant_partial_specialization_helper< std::pair<A, B> >
  {
    typedef std::pair<A, B> return_type;
  
    return_type operator()(const variant& v) const
    {
      if(v.element_type.c_type != type::c_vector)
        YAYI_THROW("Unable to transform a type " + string_type(v.element_type) + std::string(" into a map type"));
    
      if(v.element_type.c_type == type::c_vector)
      {
        if(v.element.vector_value == 0 || v.element.vector_value->size() != 2)
          YAYI_THROW("Vectore uninitialized or bad number of elements");
        
        DEBUG_ASSERT(v.element.vector_value != 0, "The vector has not been initialized");
        
        s_variant_partial_specialization_helper<typename return_type::first_type>   a_op;
        s_variant_partial_specialization_helper<typename return_type::second_type>  b_op;
        
        return std::make_pair(a_op((*v.element.vector_value)[0]), b_op((*v.element.vector_value)[1]));
      }
      YAYI_THROW("Should never execute here");
    }
  }; 

  template <>
  struct s_variant_partial_specialization_helper<string_type>
  {

    const string_type& operator()(const variant& v) const
    {
      if(v.element_type.s_type != type::s_string)
        YAYI_THROW("The containted type is not a string !: contained type is " + string_type(v.element_type));
        
      return variant_field_from_type<string_type>(v);
    }
  
  };

  template <>
  struct s_variant_partial_specialization_helper<wide_string_type>
  {

    const wide_string_type& operator()(const variant& v) const
    {
      if(v.element_type.s_type != type::s_wstring)
        YAYI_THROW("The containted type is not a string !: contained type is " + string_type(v.element_type));
        
      return variant_field_from_type<wide_string_type>(v);
    }
  
  };


  template <class bin_t, class count_t>
  struct s_variant_partial_specialization_helper< s_histogram_t<bin_t, count_t> >
  {
    typedef s_histogram_t<bin_t, count_t> return_type;
    template <class T> struct s_helper
    {
      void operator()(const variant& v, return_type& ret) const
      {
        typedef std::map<bin_t, count_t> map_t;
        map_t map_ = v;
        for(typename map_t::const_iterator it(map_.begin()), ite(map_.end()); it != ite; ++it)
        {
          ret[it->first] = it->second;
        }
      }    
    };
    
    template <class U> struct s_helper< std::vector<U> >
    {
      void operator()(const variant& v, return_type& ret) const
      {
        std::map<bin_t, count_t> map_ = v;
        for(bin_t i = 0; i < std::numeric_limits<bin_t>::max(); i++)
        {
          ret[i] = map_.count(i) ? map_[i]: 0;
        }
      }
    };
    
    return_type operator()(const variant& v) const
    {
      s_helper<typename return_type::representation_type> help;
      return_type ret;
      help(v, ret);
      return ret;
    }
  
  };

    
  
  template <class U>
  variant::operator U() const
  {
    s_variant_partial_specialization_helper<U> op;
    return op(*this);
  }
  
  
  
 
}

#endif /* YAYI_COMMON_VARIANT__HPP__ */

