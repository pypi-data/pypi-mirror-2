/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_TYPES_T_HPP__
#define YAYI_COMMON_TYPES_T_HPP__



#include <boost/mpl/bool.hpp>
#include <boost/type_traits.hpp>
#include <boost/mpl/comparison.hpp>
#include <boost/mpl/sizeof.hpp>
#include <boost/mpl/eval_if.hpp>
#include <boost/mpl/logical.hpp>
#include <boost/mpl/identity.hpp>
#include <boost/numeric/conversion/conversion_traits.hpp>
#include <boost/static_assert.hpp>


#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>



namespace yayi
{
  
  namespace type_description
  {

    /*!@group meta_utility
     * @brief Metaprogramming utilities
     *
     *@{
     */


    /*!@brief Meta-utility class : always throws
     * Utility to prevent the instance creation of the daughter classes.
     *
     * @ingroup meta_utility
     * @author Raffi Enficiaud
     */
    template <class T>
    struct s_always_throw
    {
      BOOST_STATIC_ASSERT(sizeof(T) == 0);
      s_always_throw()
      {
        YAYI_THROW("s_always_throw invoqued");
      }
    };

    /*!@brief Meta-utility class : never throws
     * @ingroup meta_utility
     *
     * This class does nothing particular (to oppose to s_always_throw)
     *
     * @author Raffi Enficiaud
     */
    struct s_never_throw{};


    /*!@brief Meta-utility class : type information
     * @ingroup meta_utility
     *
     * The purpose of this class is to prevent the use of unsupported types in the library. Each new supported type should be enquired by a
     * specializing of this class. 
     * 
     * @note Instances for unsupported types throw
     * @author Raffi Enficiaud
     */
    template <class U> struct type_support : public boost::mpl::false_
    {
      static const yayi::type::scalar_type scalar     = yayi::type::s_undefined;      //!< The scalar type
      static const yayi::type::compound_type compound = yayi::type::c_unknown;        //!< The compound type
      static const string_type& name() {
        static const string_type s = "";
        return s;
      }

      //typedef typename type_support<U>::generate_error type_error;
    };


    //! Utility transforming a template type to a type object
    //! @ref type
    template <class T> type to_type() {
      return type(type_support<T>::compound, type_support<T>::scalar);
    }




		/*!@brief Type description structure
		 *
     * The class U should be specialized by a specific @ref type_support
     * @author Raffi Enficiaud
		 */
		template <class U> 
      struct type_desc : 
        public boost::mpl::if_<typename type_support<U>::type, s_never_throw, s_always_throw<bool> >::type,
        public type_support<U>
		{
#ifdef YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
    private:
      //! The following typedef generates a compiler error for unsupported types instanciation
      typedef typename type_support<U>::support_value_type    generate_error;
#endif
    
    public:
      typedef boost::is_pod<U>                                is_pod;
      typedef typename boost::remove_cv<U>::type              type_remove_cv;
      typedef U                                               type;
		};


		//! Returns the types that may encode both types
		template <class U, class V> struct s_supertype : 
			public boost::mpl::if_<
				typename boost::mpl::and_<
					typename boost::is_scalar<U>::type, 
					typename boost::is_scalar<V>::type 
          >::type,
				s_always_throw<bool>,
				s_never_throw 
				>::type
		{
      typedef typename boost::numeric::conversion_traits<U,V>::supertype type;
		};


		//! Returns an appropriate representation for summing a sequence of type U
		template <typename U> struct s_sum_supertype {
			typedef yaF_double type;
		};


	} // namespace type_description
} // namespace yayi

#endif /* YAYI_COMMON_TYPES_T_HPP__ */


