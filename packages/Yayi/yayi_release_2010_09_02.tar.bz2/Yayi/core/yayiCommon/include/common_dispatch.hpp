/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_DISPATCH_UTILITIES_HPP__
#define YAYI_COMMON_DISPATCH_UTILITIES_HPP__

/*!@file
 * This file contains the main dispatching mechanism. To manipulate with care.
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiCommon/common_config.hpp>
#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_pixels.hpp>
#include <Yayi/core/yayiCommon/include/common_object.hpp>
#include <Yayi/core/yayiCommon/common_coordinates.hpp>

#include <typeinfo>

#include <boost/version.hpp>
#include <boost/ref.hpp>


// Reference to boost::function_types
#include <boost/function_types/function_type.hpp>
#include <boost/function_types/result_type.hpp>
#include <boost/function_types/parameter_types.hpp>
#include <boost/function_types/function_arity.hpp>
#include <boost/function_types/is_member_pointer.hpp>

// Reference to boost::type_traits
#include <boost/type_traits.hpp>

// Reference to boost::mpl
#include <boost/mpl/comparison.hpp>
#include <boost/mpl/sizeof.hpp>
#include <boost/mpl/eval_if.hpp>
#include <boost/mpl/logical.hpp>
#include <boost/mpl/identity.hpp>
#include <boost/mpl/upper_bound.hpp>
#include <boost/mpl/remove.hpp>
#include <boost/mpl/transform.hpp>
#include <boost/mpl/zip_view.hpp>
#include <boost/mpl/transform_view.hpp>
#include <boost/mpl/range_c.hpp>
#include <boost/mpl/placeholders.hpp>
#include <boost/mpl/void.hpp>

#ifndef NDEBUG
#include <boost/mpl/find.hpp>
#endif


// Reference to boost::fusion
#include <boost/fusion/sequence.hpp>
#include <boost/fusion/view/filter_view.hpp>
#include <boost/fusion/include/filter_view.hpp>
#include <boost/fusion/view.hpp>
#include <boost/fusion/include/filter_if.hpp>
#include <boost/fusion/include/transform.hpp>
#include <boost/fusion/include/transform_view.hpp>
#include <boost/fusion/functional.hpp>
#include <boost/fusion/include/accumulate.hpp>
#include <boost/fusion/include/at_c.hpp>


#include <boost/fusion/adapted/mpl.hpp>
#include <boost/fusion/include/mpl.hpp>

#include <boost/fusion/algorithm/transformation/remove_if.hpp>
#include <boost/fusion/functional/generation/make_fused.hpp>
#include <boost/fusion/algorithm/iteration/for_each.hpp>
#include <boost/fusion/container/generation.hpp>
#include <boost/fusion/view/filter_view.hpp>
#include <boost/fusion/iterator/value_of.hpp>
#include <boost/fusion/support/deduce_sequence.hpp>

#include <boost/fusion/container/generation/vector_tie.hpp>
#include <boost/fusion/include/vector_tie.hpp>

//#define YAYI_DBG_DISPATCH(x) {std::cout << x;}
#define YAYI_DBG_DISPATCH(x)

namespace yayi
{

  namespace dispatcher
  {

    template <class T>
    inline std::string print_only_ints(const T& i) {
      return "";
    }


    template <>
    inline std::string print_only_ints<int>(const int& i) {
      return int_to_string(i);
    }

    template <>
    inline std::string print_only_ints<unsigned int>(const unsigned int& i) {
      return int_to_string(i);
    }

    //! Tag for compile time deductible convertors
    struct s_convertible_compile_time {};

    //! Tag for runtime deductible convertors
    struct s_convertible_runtime_time {};

    //! Tag for dynamic cast deductible convertors
    struct s_convertible_dynamic_cast {};

    

      
    //! Default dummy convertor
    //! Is instanciated when no convertor has been specified for the input types pair. Throws.
    template <class I, class T, bool B_WRITE_ONLY = false> struct s_no_conversion {
      typedef boost::false_type type;
      typedef typename remove_const<I>::type Icv;
      typedef typename add_reference<typename add_const<I>::type>::type I_;

      static inline bool  is_convertible  (I_ )           {YAYI_THROW("Should not be called");}
      static inline T     convert         (Icv )          {YAYI_THROW("Should not be called");}
    };


    /*! Default dummy runtime convertor: unless specialized, does exactly the same as s_no_conversion
     * This structure defines the runtime convertor.
     * @author Raffi Enficiaud
     */
    template <class I, class T, bool B_WRITE_ONLY = false> struct s_runtime_conversion : public s_no_conversion<I, T, B_WRITE_ONLY> {
    };


    /*! Dynamic cast convertor
     * This convertor simply calls the dynamic_cast operator from I to T to perform the conversion.
     * @author Raffi Enficiaud
     */
    template <class I, class T, bool B_WRITE_ONLY = false> struct s_dynamic_cast_conversion {
      typedef boost::true_type type;
      
      typedef typename remove_const<I>::type Icv;
      typedef typename add_reference<I>::type Iref;
      typedef typename add_reference<T>::type Tref;
      typedef typename add_reference<
        typename add_const<
            typename remove_reference<I>::type
          >::type
      >::type Icref;
  
      typedef typename add_pointer<
        typename add_const<
          typename remove_reference<T>::type
        >::type
      >::type const_pointer;

      // Dynamic cast conversions do not need holders
      typedef mpl::false_ need_holder;
      typedef mpl::void_  holder_type;
      typedef mpl::true_  internal_reference;

      static inline bool is_convertible(Icref u) throw() 
      {
        YAYI_DBG_DISPATCH("is_convertible dynamic_cast called for I: " + errors::demangle(typeid(I).name()) + " and T:" + errors::demangle(typeid(T).name()) );
        try
        {
          YAYI_DBG_DISPATCH("is convertible REGULAR DISPATCH" << std::endl);
          return dynamic_cast<const_pointer>(u) != 0;
        }
        catch(std::bad_cast &)
        {
          return false;
        }
        return true;
      }
      
      static inline Tref convert(Iref u)
      {
        DEBUG_ASSERT(is_convertible(u), "Non convertible for u of type " + errors::demangle(typeid(u).name()));
        return dynamic_cast<const_pointer>(u);
      }
    };


    /*! Dynamic cast convertor implementation for special combination of types I* to T&
     * @see s_dynamic_cast_conversion
     * @author Raffi Enficiaud
     */
    template <class I, class T> struct s_dynamic_cast_conversion<I*, T&, false> {
      typedef boost::true_type type;
      
      typedef typename remove_const<I>::type Icv;
      typedef typename add_reference<I>::type Iref;
      typedef typename add_reference<typename remove_const<T>::type>::type Tref;
      typedef typename add_reference<typename add_const<T>::type>::type Tcref;
      typedef typename add_reference<
        typename add_pointer<
          typename add_const<
            I//typename remove_reference<I>::type
            >::type
          >::type
      >::type Icref;

      typedef typename add_pointer<
        typename remove_const<
          T//typename remove_reference<T>::type
        >::type
      >::type non_const_pointer;
  
      typedef typename add_pointer<
        typename add_const<
          T//typename remove_reference<T>::type
        >::type
      >::type const_pointer;

      // Dynamic cast conversions do not need holders
      typedef mpl::false_ need_holder;
      typedef mpl::void_  holder_type;
      typedef mpl::true_  internal_reference;

      static inline bool is_convertible(Icref u) throw() 
      {
        YAYI_DBG_DISPATCH("is_convertible dynamic_cast (2) called for I: " + errors::demangle(typeid(I*).name()) + " and T:" + errors::demangle(typeid(T&).name()) << std::endl);
      
        try
        {
          YAYI_DBG_DISPATCH("is convertible REGULAR DISPATCH (2)" << std::endl);
          YAYI_DBG_DISPATCH("dynamic_cast result from " 
            << errors::demangle(typeid(Icref).name()) 
            << " to " 
            << errors::demangle(typeid(const_pointer).name())
            << (dynamic_cast<const_pointer>(u) != 0 ? "true":"false")
            << std::endl);

          YAYI_DBG_DISPATCH("real type of input is " 
            << errors::demangle(typeid(*u).name()) 
            << std::endl);

          return dynamic_cast<const_pointer>(u) != 0;
        }
        catch(std::bad_cast &)
        {
          YAYI_DBG_DISPATCH("is convertible REGULAR DISPATCH (2): bad cast" << std::endl);
          return false;
        }
        return true;
      }
      
      static inline Tref convert(Iref u)
      {
        DEBUG_ASSERT(is_convertible(u), "Non convertible for u of type " + errors::demangle(typeid(u).name()));
        return *dynamic_cast<non_const_pointer>(u);
      }

      static inline Tcref convert(Icref u)
      {
        DEBUG_ASSERT(is_convertible(u), "Non convertible for u of type " + errors::demangle(typeid(u).name()));
        return *dynamic_cast<const_pointer>(u);
      }
    };



    /*! Compile time convertor.
     * This operator asserts at compilation time the fact that I is convertible to T.
     * @author Raffi Enficiaud
     */    
    template <class I, class T, bool B_WRITE_ONLY = false> 
    struct s_compile_time_conversion 
    {
      //typedef boost::true_type type;
      typedef typename boost::is_convertible<I, T>::type type;
      typedef s_compile_time_conversion<I, T, B_WRITE_ONLY> this_type;
      
      typedef
        typename add_reference<
          typename remove_const<
            typename remove_reference<I>::type
          >::type
        >::type Iref;
      typedef
        typename add_reference<
          typename add_const<
            typename remove_reference<I>::type
          >::type
        >::type Icref;

      typedef
          typename remove_const<
            typename remove_reference<T>::type
        >::type To;
      typedef
          typename remove_const<
            typename remove_reference<T>::type
        >::type Tco;

              
      typedef typename add_reference<typename add_const<I>::type>::type I_;

      static inline bool is_convertible(Icref /*u*/) throw() 
      {
        YAYI_DBG_DISPATCH("Demangling : " << errors::demangle(typeid(this_type).name()) << std::endl);
        BOOST_STATIC_ASSERT((boost::is_convertible<I, T>::value));
        return true;
      }
      
      // T cannot be a reference if it is not I/Icv
      static inline Tco convert(Icref u)
      {
        YAYI_DBG_DISPATCH("s_compile_time_conversion::convert : " << errors::demangle(typeid(this_type).name()) << std::endl);
        YAYI_DBG_DISPATCH("\tfrom: " << u << " -- to -- " << static_cast<Tco>(u) << std::endl);
        return static_cast<Tco>(u);
      }
      static inline To convert(Iref u)
      {
        YAYI_DBG_DISPATCH("s_compile_time_conversion::convert : " << errors::demangle(typeid(this_type).name()) << std::endl);
        YAYI_DBG_DISPATCH("\tfrom: " << u << " -- to -- " << static_cast<To>(u) << std::endl);
        return static_cast<To>(u);
      }
      
    };

    //! If the program is correctly written, this should not be instanciated
    template <class I> 
    struct s_compile_time_conversion<I,I, false> 
    {
      typedef s_compile_time_conversion<I, I, false> this_type;
      typedef boost::true_type type;
      typedef
        typename add_reference<
          typename remove_const<
            typename remove_reference<I>::type
          >::type
        >::type Iref;
      typedef
        typename add_reference<
          typename add_const<
            typename remove_reference<I>::type
          >::type
        >::type Icref;

      typedef mpl::true_  internal_reference;

      static inline bool is_convertible(Icref /*u*/) throw() 
      {
        YAYI_DBG_DISPATCH("Demangling : " << errors::demangle(typeid(this_type).name()) << std::endl);
        return true;
      }
      static inline Iref convert(Iref u)
      {
        YAYI_DBG_DISPATCH("Converting value = " << u << std::endl);
        return u;
      }
      static inline Icref convert(Icref u)
      {
        YAYI_DBG_DISPATCH("Converting const value = " << u << std::endl);
        return u;
      }
    };
    
    template <class I> struct s_compile_time_conversion<I,I, true> : s_compile_time_conversion<I,I, false> {};
    
    
    //! Macro for specifying that a runtime convertor needs a temporary value for holding the conversion
    BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(need_temporary_holder_tag, need_holder_tag, false);
    
    //! Macro specifying that the returned value is an internal reference, so it can be stored by reference 
    //! instead of by value.
    BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(return_internal_reference, internal_reference, false);
    
    namespace distpatcher_utilities {
      template <class I, class T, class convertible_request, bool B_WRITE_ONLY>
      struct s_convert_func
      {typedef s_no_conversion<I, T, B_WRITE_ONLY> type;};
      
      template <class I, class T, bool B_WRITE_ONLY>
      struct s_convert_func<I, T, s_convertible_compile_time, B_WRITE_ONLY>
      {typedef s_compile_time_conversion<I, T, B_WRITE_ONLY>  type;};

      // This specialisation answers a drawback of the current implementation concerning the intermediate 
      // storage element in the conversion. 
      template <class I, bool B_WRITE_ONLY>
      struct s_convert_func<I&, I, s_convertible_compile_time, B_WRITE_ONLY>
      {typedef s_compile_time_conversion<I, I, B_WRITE_ONLY>  type;};
      
      template <class I, class T, bool B_WRITE_ONLY>
      struct s_convert_func<I, T, s_convertible_runtime_time, B_WRITE_ONLY>
      {typedef s_runtime_conversion<I, T, B_WRITE_ONLY>        type;};
      
      template <class I, class T, bool B_WRITE_ONLY>
      struct s_convert_func<I, T, s_convertible_dynamic_cast, B_WRITE_ONLY>
      {typedef s_dynamic_cast_conversion<I, T, B_WRITE_ONLY>   type;};
    }



    //! Simple policy for selecting convertors at compile time.
    //! It is possible to specialize this structure, or to provide it better logic.
    template <class I, class T, bool B_WRITE_ONLY = false>
      struct s_conversion_policy
    {
      typedef typename boost::mpl::if_<
        boost::is_convertible<I, T>, 
        s_convertible_compile_time,
        s_convertible_runtime_time >::type type;
    };


    template <class I, class T, bool B_WRITE_ONLY = false>
      struct s_dispatch_convertor
    {
      typedef typename s_conversion_policy<I, T, B_WRITE_ONLY>::type conversion_decision_type;
      typedef typename distpatcher_utilities::s_convert_func<I, T, conversion_decision_type, B_WRITE_ONLY>::type convertor_type;
    };


    namespace 
    {

      //! Utility function for selecting the storage type (according to the input type)
      //! The storage is by default the reference to S, unless the input type is mpl::void_
      template <class S>
        struct s_same_select_ref
      {
        typedef typename boost::mpl::if_<
          typename mpl::is_void_<S>::type,
          const mpl::void_ &,
          typename add_reference<S>::type>::type type;
      };


      /*!Helper meta-function for infering types that are suitable for dispatch meta-functions
       *
       * @example 
       * const IImage*& is transformed to IImage* (to keep interfaces semantics)
       * yaUINT8& to yaUINT8&
       * const yaUINT8& to yaUINT8&
       *
       * @author Raffi Enficiaud
       */
      struct s_dispatcher_type_helper_template_arg {
        template <class U> struct apply {
          typedef typename mpl::if_<
            typename is_reference<U>::type,
            
            typename mpl::if_<
              typename is_pointer<typename remove_reference<U>::type>::type,
              typename add_pointer<typename remove_const<typename remove_pointer<typename remove_reference<U>::type>::type>::type>::type,
              typename add_reference<typename remove_const<typename remove_reference<U>::type>::type>::type
              >::type,
            
            typename mpl::if_<
              typename is_pointer<U>::type,
              typename add_pointer<typename remove_const<typename remove_pointer<U>::type>::type>::type, 
              U
              >::type
              
            >::type type;
        };
      };
      
      
      
      #if 0
      /*! Helper meta-function for infering types suitable for dispatch meta-functions
       *
       * @example 
       * const IImage*& is transformed to IImage*
       * yaUINT8& to yaUINT8&
       * const yaUINT8& to yaUINT8&
       *
       * @author Raffi Enficiaud
       */
       struct s_dispatcher_type_helper_template_arg_keep_const {

        typedef typename mpl::if_<
            is_reference<U>,
            typename mpl::if_<
              is_pointer< typename remove_reference<U>::type >,
              typename remove_const<typename remove_reference<U>::type>::type,
              typename add_reference<typename remove_const<typename remove_reference<U>::type>::type>::type
              >::type, 
            typename mpl::if_<
              is_pointer<U>,
              typename add_pointer<typename remove_const<typename remove_pointer<U>::type>::type>::type, 
              U
              >::type
          >::type type;
      };
      #endif

      

      /*!Simple convertor for the input sequence type
       * Applies @ref s_dispatcher_type_helper_template_arg on all the elements of a sequence
       * @author Raffi Enficiaud
       */
      struct transform_arguments_for_convertors {
        template <class seq> struct apply {
          typedef typename boost::mpl::apply<s_dispatcher_type_helper_template_arg, seq>::type type;
        };
      };


#if 0
      template <class convertor_t, convertor_t* P>
      struct s_result_of_helper
      {
        template <class T> struct result;
        template <class U> struct result< s_result_of_helper(U) >
        {
          typedef typename boost::result_of< (convertor_t::*) (U)&P::convert>::type;
        };
      };

      template <class V, class U, V (*ptr_t)(U&)>
      V function_help_00(U& i)//V (&convertor_function)(U&))
      {
        return ptr_t(i);
      }


      template <class A>
      struct s_result_of_helper
      {
        template <class V>
        struct result;

        template <class V, class S_>
        struct result<S_(A&, V (*)(A) )>{
          //typedef typename boost::function_types::result_type<U>::type type;
          typedef V type;
        };


        template <class V>
        V operator()(A& a, V (*p_to_func)(A))
        {
          return p_to_func(a);
        }
      };


      template <class U, class convert_t>
      struct s_result_of_helper<U, V (convert_t::*)(U) >
      {
        typedef V type;
      };
#endif
      
      
      
      /*! Conversion utility
       *
       * Holds the real convertor from and to an interface type to the real input type of the function. Used internally by the dispather.
       * This is where the main logic for calling the convertors is implemented.
       * @author Raffi Enfciaud
       */
      template <class I, class T, bool B_WRITE_ONLY = false>
        struct s_convertor_wrapper
      {
      private:
        typedef s_convertor_wrapper<I, T, B_WRITE_ONLY>           this_type;
        
        typedef typename add_reference<I>::type     type_i;
        type_i i_;

        s_convertor_wrapper();
        this_type& operator=(const this_type&);
        

      public:

        //! Type of the policy
        typedef s_dispatch_convertor<
          typename mpl::apply<s_dispatcher_type_helper_template_arg, I>::type, 
          typename mpl::apply<s_dispatcher_type_helper_template_arg, T>::type,
          mpl::or_<
            mpl::bool_<B_WRITE_ONLY>, 
            typename mpl::and_<
              typename boost::is_reference<I>::type,
              typename boost::is_reference<T>::type,
              typename mpl::not_<typename boost::is_const< typename remove_reference<I>::type >::type>::type,
              typename mpl::not_<typename boost::is_const< typename remove_reference<T>::type >::type>::type
            >::type
          >::type::value
        > convertor_policy_type;

        //! Type of the convertor
        typedef typename convertor_policy_type::convertor_type         convertor_type;

        s_convertor_wrapper(const this_type& r_) : i_(r_.i_) 
        {
          YAYI_DBG_DISPATCH("s_convertor_wrapper " << std::endl
            << "\tElement : " << errors::demangle(typeid(T).name()) << std::endl
            << "\tconvertor " << errors::demangle(typeid(this_type).name()) << std::endl
            << "\tconvertor_policy_type " << errors::demangle(typeid(convertor_policy_type).name()) << std::endl
            << "\tconvertor_type " << errors::demangle(typeid(convertor_type).name()) << std::endl);
          //YAYI_DBG_DISPATCH("s_convertor_wrapper::copy_ctor with " << (void*)&i_ << " this = " << (void*)this << std::endl);
          YAYI_DBG_DISPATCH("ARG interface " << std::endl
            << "\tfrom " << errors::demangle(typeid(I).name()) 
            << " to " << errors::demangle(typeid(typename mpl::apply<s_dispatcher_type_helper_template_arg, I>::type).name()) << std::endl);
          YAYI_DBG_DISPATCH(std::endl << std::endl);
          
        }

        s_convertor_wrapper(type_i i) : i_(i)
        {
          //YAYI_DBG_DISPATCH("s_convertor_wrapper with " << (void*)&i_ << " this = " << (void*)this << std::endl);
          YAYI_DBG_DISPATCH("s_convertor_wrapper() " << errors::demangle(typeid(type_i).name()) << std::endl);
          YAYI_DBG_DISPATCH("\twith i= : " << print_only_ints(i_) << std::endl);
        }
        ~s_convertor_wrapper()
        {
          //YAYI_DBG_DISPATCH("~s_convertor_wrapper with " << (void*)&i_ << " this = " << (void*)this << std::endl);
        }
        
        //! Query the real convertor instance for conversion ability
        bool is_convertible() const YAYI_THROW_DEBUG_ONLY__ {
          YAYI_DBG_DISPATCH("s_convertor_wrapper::is_convertible " << errors::demangle(typeid(convertor_type).name()) << std::endl);
          return convertor_type::is_convertible(i_);
        }
        
        struct internal_holder {

          #if 0
          template <class T>
          struct s_make_an_error
          {typedef T type;};
          template <class T>
          struct s_make_an_error<T&>
          {};
          #endif
          
          // back convert helper class
          template <class II, class TT, class B = mpl::false_> 
          struct s_back_convert 
          {
            s_back_convert(II, TT){}
          };

          template <class II, class TT> 
          struct s_back_convert<II, TT, mpl::true_> 
          {
            II i_; TT t_;
            s_back_convert(II i, TT t) : i_(i), t_(t){}
            ~s_back_convert()
            {
              // Here we may need a particular back convertor. Now, we suppose that this transformation is implicit
              i_ = t_;
            }
          };

          // storage policy of intermediate object (or reference)
          // maybe should be moved into another template helper
          typedef typename mpl::if_<
            typename is_reference<I>::type
            ,
            
            // I&
            typename mpl::if_<
              typename is_const< 
                typename mpl::if_<
                  typename is_pointer< typename remove_reference<I>::type >::type,          // I*& ?
                  typename remove_pointer< typename remove_reference<I>::type >::type,      // I*& -> I
                  typename remove_reference<I>::type                                        // I& -> I
                >::type
              >::type                                                                       // I const& or I const* & ?
              ,
              
              // I const & --> T is_ref ? T const & : T const &
              typename mpl::if_<
              typename is_reference< T >::type, 
                typename mpl::if_<
                  typename need_temporary_holder_tag<convertor_type>::type,                 // "I const &" + "T&" + convertor needs a holder ?
                  typename add_const< typename remove_reference<T>::type >::type,           // "I const &" + "T&" + convertor needs a holder -> T const
                  typename add_reference< typename add_const< typename remove_reference<T>::type >::type >::type    // "I const &" + "T&" + convertor does not need a holder -> T const &
                  >::type,
                // "I const &" is const + "T" not a reference : the best thing to do is to store
                // the return type of the convertor. 
                //typename s_result_of_helper< typename add_reference<I>::type, &convertor_type::convert/*(type_i)*/ >::type
                //typename boost::result_of< convertor_type::convert(typename add_reference<I>::type) >::type
                //typename boost::result_of< function_help_00< typename add_reference<I>::type , &convertor_type::convert > >::type
                // Ok, my attempts all failed :)

                typename mpl::if_<
                  typename return_internal_reference<convertor_type>::type,
                  typename add_reference< typename add_const< T >::type >::type,
                  typename add_const< T >::type
                  >::type
#if 0

                // is constness
                typename mpl::if_<
                  typename need_temporary_holder_tag<convertor_type>::type,                 
                  typename add_const<T>::type,                                              // "I const &" + "T" + convertor needs a holder -> T const
                  //typename add_reference< typename add_const< T >::type >::type             // "I const &" + "T" + convertor does not need a holder -> T const &
                  typename add_const< T >::type
                  >::type
#endif
              >::type
              ,
              
              // I & --> T & : T
              typename mpl::if_<
                typename is_reference< T >::type, 
                typename mpl::if_<
                  typename need_temporary_holder_tag<convertor_type>::type,
                  typename remove_const< typename remove_reference<T>::type >::type,
                  typename add_reference< typename remove_const< typename remove_reference<T>::type >::type >::type
                >::type,
                typename mpl::if_<
                  typename need_temporary_holder_tag<convertor_type>::type,
                  typename remove_const< T >::type,
                  typename add_reference< typename remove_const< T >::type >::type
                >::type
              >::type
              
            >::type
            ,
              
            // I non &
            // T -> non const et non ref
            typename remove_const< typename remove_reference<T>::type >::type
          >::type type_t2;
            
          
          // if the storage needs a temporary holder ...
          typedef typename mpl::if_<
            typename need_temporary_holder_tag<convertor_type>::type,
            typename mpl::or_<
              typename mpl::and_<
                mpl::and_< typename is_reference<I>::type, typename is_reference<T>::type >,
                mpl::and_< 
                  mpl::not_< typename is_const<typename remove_reference<I>::type>::type >, 
                  mpl::not_< typename is_const<typename remove_reference<T>::type>::type > 
                > 
              >::type,
              typename mpl::bool_<B_WRITE_ONLY>::type
            >::type,
            mpl::false_
          >::type type_back_convert;
          
          
          typedef type_t2 type_t;
          
          type_i i_;                                //!< Reference to the original object
          type_t t_;                                //!< Converted object
          
          s_back_convert<type_i, typename add_reference<type_t>::type, type_back_convert> op_back;
          
          internal_holder(type_i i) : 
            i_(i), 
            t_(convertor_type::convert(i)), 
            op_back(i_, t_)
          {
            YAYI_DBG_DISPATCH("s_convertor_wrapper::internal_holder " << errors::demangle(typeid(i_).name()) << " -- to -- " << errors::demangle(typeid(t_).name()) << std::endl);
            YAYI_DBG_DISPATCH("s_convertor_wrapper::internal_holder " << errors::demangle(typeid(type_i).name()) << " -- to -- " << errors::demangle(typeid(type_t).name()) << std::endl);
            YAYI_DBG_DISPATCH("\tfrom : " << print_only_ints(i_) << " -- to -- " << print_only_ints(t_) << std::endl);
          }
          
          ~internal_holder() {
            // do the back conversion here
            // done in the destructor of op_back
            YAYI_DBG_DISPATCH("~s_convertor_wrapper::internal_holder " << errors::demangle(typeid(type_i).name()) << " -- to -- " << errors::demangle(typeid(type_t).name()) << std::endl);
            YAYI_DBG_DISPATCH("\tfrom : " << print_only_ints(i_) << " -- to -- " << print_only_ints(t_) << std::endl);
            YAYI_DBG_DISPATCH("\ttype t is reference ? : " << (boost::is_reference<type_t>::value ? "true":"false") << std::endl);
          }
          
          operator typename add_reference<type_t>::type () 
          {
            YAYI_DBG_DISPATCH("getting a reference to t of value " << print_only_ints(t_) << " with i of value " << print_only_ints(i_) << std::endl);
            YAYI_DBG_DISPATCH("\ttype t is reference ? : " << (boost::is_reference<type_t>::value ? "true":"false") << std::endl);
            YAYI_DBG_DISPATCH("\ttype t is const ? : " << (boost::is_const<typename boost::remove_reference<type_t>::type>::value ? "true":"false") << std::endl);
            return t_;
          }
          
          internal_holder& operator=(typename add_reference< typename add_const<type_t>::type >::type r_) {
            YAYI_DBG_DISPATCH("setting a reference to t of value " << print_only_ints(t_) << " to value " << r_ << std::endl);
            t_ = r_;
            return *this;
          }
          
        };
        

        //! Calls the real convertor convert static method
        internal_holder convert() const throw()
        {
          return internal_holder(i_);
        }

      };

      //! Query for conversion ability
      //! Called by the dispatcher (wrapper for boost::fusion::foreach call to the vector of wrappers of convertors is_convertible method)
      struct is_convertible {
        typedef bool result_type;
      #if ( (((BOOST_VERSION  / 100) % 1000) >= 42) && ((BOOST_VERSION /  100000) >= 1) )
        template<typename T> result_type operator()(const result_type& res, const T& t) const {
      #else
        template<typename T> result_type operator()(const T& t, const result_type& res) const {
      #endif
          // if res if false, no more convertibility test will be performed
          YAYI_DBG_DISPATCH("is convertible &" << (void*)&t << std::endl);
          YAYI_DBG_DISPATCH("::is_convertible " << errors::demangle(typeid(t).name()) << " res = " << res << " value " << t.is_convertible() << std::endl);
          return res && t.is_convertible();
        }
      };

      //! Conversion utility
      //! Called by the dispatcher (wrapper for boost::fusion::foreach call to the vector of convertors)
      struct convert_wrapper {
        //typedef void result_type;
        
        template <class T> struct result;
        template <class self, class T> struct result<self(T)> {
          typedef typename remove_reference<T>::type::internal_holder type;
        };
        
        template <class T> 
        typename result<convert_wrapper(T)>::type operator()(T t) const {
          return t.convert();
        }
      };

      
      
      
      
      // the holder helper class
      template <class fusion_seq, class mpl_seq, int index> 
      struct result_of_helper 
      {
      protected:
        typedef 
          typename fusion::result_of::value_of<
            typename fusion::result_of::advance_c<
              typename fusion::result_of::begin<fusion_seq>::type, 
                index >::type >::type seq_element_t;
       
        //! The type of the convertor
        typedef s_convertor_wrapper<
          seq_element_t, //typename mpl::apply<s_dispatcher_type_helper_template_arg, seq_element_t>::type,
          //typename remove_pointer<seq_element_t>::type,                 // remove pointer because we artificially added one
          //typename mpl::apply<s_dispatcher_type_helper_template_arg, typename mpl::at_c<mpl_seq, index>::type>::type> wrapper_type;
          typename mpl::at_c<mpl_seq, index>::type> wrapper_type; // Raffi: proper types already extrated in the convertor
          
        typedef typename wrapper_type::convertor_type::type is_convertor_defined;
        
        BOOST_MPL_ASSERT((typename wrapper_type::convertor_type::type));
        //reference_wrapper<fusion_seq const> seq;
      protected:
        typedef wrapper_type result;
        
        result_of_helper() {
          YAYI_DBG_DISPATCH("result_of_helper " << std::endl
            << "\tresult_of_helper " << errors::demangle(typeid(result_of_helper).name()) << std::endl
            << "\twrapper_type " << errors::demangle(typeid(wrapper_type).name()) << std::endl);
        }
        
        wrapper_type operator()(fusion_seq const& seq_) const throw() {
          // deref, see remark above
          YAYI_DBG_DISPATCH("result_of_helper #" << index << " with " << (void*)&fusion::deref(fusion::advance_c<index>(fusion::begin(seq_))) << std::endl);
          return wrapper_type(fusion::deref(fusion::advance_c<index>(fusion::begin(seq_))));
        }
                
      private:
        result_of_helper& operator=(const result_of_helper&);
        result_of_helper(const result_of_helper&);
      };
      
      
      
      // the holer intermediate class
      template <class fusion_seq, class mpl_seq, int index> 
        struct dispatch_result_of;
      template <class fusion_seq, class mpl_seq> 
        struct dispatch_result_of<fusion_seq, mpl_seq, 0>;

      
      template <class fusion_seq, class mpl_seq, int index> 
        struct dispatch_result_of : 
          dispatch_result_of<fusion_seq, mpl_seq, index-1>,
          protected result_of_helper<fusion_seq, mpl_seq, index>
      {
        typedef result_of_helper<fusion_seq, mpl_seq, index>        helper;
        typedef dispatch_result_of<fusion_seq, mpl_seq, index-1>    parent;
        
        BOOST_MPL_ASSERT((typename helper::is_convertor_defined));
        typedef typename mpl::and_<
          typename parent::is_convertor_defined,
          typename helper::is_convertor_defined>::type is_convertor_defined;
        
      private:
        dispatch_result_of(const dispatch_result_of&);
        
      public:
        
        dispatch_result_of() : parent(), helper()
        {
          YAYI_DBG_DISPATCH("dispatch_result_of " << std::endl
            << "\tdispatch_result_of " << errors::demangle(typeid(dispatch_result_of).name()) << std::endl
            << "\thelper " << errors::demangle(typeid(helper).name()) << std::endl);

        }
        
        #ifndef NDEBUG
        ~dispatch_result_of(){
          YAYI_DBG_DISPATCH("~result_of #" << index << " with this = " << (void*)this << std::endl);
        }
        #endif

        // vector holding
        typedef typename fusion::result_of::push_back<
          typename parent::result, 
          typename helper::result>::type const push_result;
          
        typedef typename fusion::traits::deduce_sequence<push_result>::type result;
        

        result operator()(fusion_seq const& seq_) const throw() {
          
          YAYI_DBG_DISPATCH("dispatch_result_of::operator()() #" << index << " with " << (void*)&fusion::deref(fusion::advance_c<index>(fusion::begin(seq_))) << std::endl);

          return fusion::push_back(this->parent::operator()(seq_), this->helper::operator()(seq_));
        }
      };
      
      template <class fusion_seq, class mpl_seq> 
        struct dispatch_result_of<fusion_seq, mpl_seq, 0> : 
          protected result_of_helper<fusion_seq, mpl_seq, 0>
      {
        typedef result_of_helper<fusion_seq, mpl_seq, 0>  helper;
        BOOST_MPL_ASSERT((typename helper::is_convertor_defined));
        typedef typename helper::is_convertor_defined is_convertor_defined;
        
        dispatch_result_of() : helper()
        {
          YAYI_DBG_DISPATCH("dispatch_result_of #" << 0 << " with this = " << (void*)this << std::endl);
        }
        
        #ifndef NDEBUG
        ~dispatch_result_of(){
          YAYI_DBG_DISPATCH("~result_of #" << 0 << " with this = " << (void*)this << std::endl);
        }
        #endif
                
        typedef fusion::vector< typename helper::result > const result;
        result operator()(fusion_seq const& seq_) const throw() {   
          YAYI_DBG_DISPATCH("dispatch_result_of::operator()() #" << 0 << " with " << (void*)&fusion::deref(fusion::advance_c<0>(fusion::begin(seq_))) << std::endl);
          return fusion::make_vector(helper::operator()(seq_));    
        }

      };

      
      
      template <class return_t, class return_storage_type, class T>  struct s_return_handler;
      template <class return_t, class return_storage_type>           struct s_return_handler<return_t, return_storage_type, void>;
      
      //! Utility class for handling function invocation and the conversion of its returned value
      //! @author Raffi Enficiaud
      template <class return_t, class return_storage_type, class T>  struct s_return_handler
      {
        typedef typename mpl::if_<
          is_same<return_t, typename add_reference<T>::type>,
          typename add_reference<T>::type,
          T>::type T_type;
      
        typedef s_convertor_wrapper<
          return_t,
          T_type,
          true> return_convertor_type;
        
        return_convertor_type return_convertor;
        
        //! Constructor
        //! @param[in] t reference to the storage of the return type.
        s_return_handler(typename add_reference<return_storage_type>::type i_) : return_convertor(i_)
        {
#ifndef NDEBUG
          BOOST_STATIC_ASSERT(return_convertor_type::convertor_type::type::value);
#endif
        }
        
        bool is_convertible() const throw()
        {
          return return_convertor.is_convertible();
        }
        
        //! Function invocation for non-member functions
        template <class F, class Seq>
        void invoke(F& f, Seq& seq) const
        {
          typename fusion::result_of::invoke<F, typename fusion::result_of::transform<Seq, convert_wrapper>::type>::type res = fusion::invoke(f, fusion::transform(seq, convert_wrapper()) );
          return_convertor.convert() = res;
        };
        
        //! Function invocation for member functions
        template <class F, class Seq, class U>
        void invoke(F& f, Seq& seq, U& u) const
        {
          typename fusion::result_of::invoke<F, typename fusion::result_of::push_front< typename fusion::result_of::transform<Seq, convert_wrapper>::type, U*>::type>::type res = fusion::invoke(f, fusion::push_front(fusion::transform(seq, convert_wrapper()), &u));
          return_convertor.convert() = res;
        };
      };
      
      
      //! Specializing of the invocation utility for function returning void.
      template <class return_t, class return_storage_type>
        struct s_return_handler<return_t, return_storage_type, void>
      {
        s_return_handler(typename add_reference<return_storage_type>::type)
        {
#ifndef NDEBUG
          BOOST_MPL_ASSERT((boost::is_same<return_t, mpl::void_>));
#endif
        }
        
        bool is_convertible() const throw()
        {
          return true;
        }
        
        template <class F, class Seq>
        void invoke(F& f, Seq& seq)
        {
          fusion::invoke(f, fusion::transform(seq, convert_wrapper()) );
        };
        template <class F, class Seq, class U>
        void invoke(F& f, Seq& seq, U& u)
        {
          fusion::invoke(f, fusion::push_front(fusion::transform(seq, convert_wrapper()), &u));
        };
      };
      
      
      
      
    
      
      /*!@brief Holds a sequence of convertor (from interface type to real type, deduced by the provided function)
       *
       * This class constructs a sequence of convertors, given the sequence of interface type element (concrete elements) and 
       * a vector of target types (for function input).
       * fusion_seq is the sequence of interface elements, while mpl_seq is the sequence of the target function input types.
       *
       * @author Raffi Enficiaud
       */
      template <class fusion_seq, class mpl_seq>
        struct s_convertor_holder
      {
        typedef dispatch_result_of< fusion_seq, mpl_seq,  mpl::size<mpl_seq>::value-1> transformer_t;
        typedef typename fusion::traits::deduce_sequence<typename transformer_t::result>::type result_type;
        
        typedef typename transformer_t::is_convertor_defined is_convertor_defined;
       
        result_type operator()(fusion_seq const & seq) {
          transformer_t op;
          return result_type(op(seq));
        }

      };






    }


    /*!@brief Dispatcher V2
     *
     * Now uses boost::fusion lib, especially for calling function objets. 
     * @author Raffi Enficiaud
     */
    template <
      class return_t = boost::mpl::void_, 
      class A1 = boost::mpl::void_, 
      class A2 = boost::mpl::void_, 
      class A3 = boost::mpl::void_, 
      class A4 = boost::mpl::void_, 
      class A5 = boost::mpl::void_, 
      class A6 = boost::mpl::void_>
      struct s_dispatcher
    {

      //! This dispatcher type
      typedef s_dispatcher<return_t, A1, A2, A3, A4, A5, A6>                   this_type;

      //! The fusion::vector type containing the reference to interface arguments
      typedef typename boost::fusion::vector<
        typename s_same_select_ref<A1>::type, 
        typename s_same_select_ref<A2>::type, 
        typename s_same_select_ref<A3>::type, 
        typename s_same_select_ref<A4>::type, 
        typename s_same_select_ref<A5>::type, 
        typename s_same_select_ref<A6>::type>                                         sequence_arguments_;

      //! The return interface type 
      typedef typename add_reference<return_t>::type                                  R0;

      //! Test type for mpl::void_ removal from the argument list
      typedef mpl::is_void_<
        remove_const< remove_reference<mpl::_> > 
      >  remove_void_arguments_;

      //! Interface arguments sequence without mpl::void_
      typedef typename fusion::result_of::remove_if<
        sequence_arguments_ const, 
        remove_void_arguments_ >::type                                          filtered_sequence_arguments_;

      private:
        this_type& operator=(const this_type&){}


      //! Compilation time test through MPL
      typedef mpl::vector<A1, A2, A3, A4, A5, A6>                               argument_seq_mpl_;
      typedef typename mpl::remove<argument_seq_mpl_, mpl::void_>::type         argument_seq_mpl_void_;
      typedef typename mpl::transform<
        argument_seq_mpl_void_, 
        transform_arguments_for_convertors>::type                               convertors_args_seq_type;

#ifndef NDEBUG
      typedef typename mpl::find<argument_seq_mpl_, mpl::void_>::type   iter_find_check;
      typedef typename mpl::upper_bound<argument_seq_mpl_, mpl::void_, boost::is_same<boost::mpl::_1, boost::mpl::_2> >::type iter_find_check2;
      BOOST_MPL_ASSERT_RELATION( (mpl::distance<iter_find_check2, iter_find_check>::value) , >=, 0);
#endif


      // Extractor for convertor
      template <class T> struct s_convertor_extractor_ {typedef typename T::convertor_type::type type;};

      //typedef typename fusion::traits::deduce_sequence<filtered_sequence_arguments_>::type vector_data_type;
      typedef typename fusion::result_of::as_vector<filtered_sequence_arguments_>::type vector_data_type;
      //typedef filtered_sequence_arguments_ vector_data_type;

      //typedef filtered_sequence_arguments_ vector_data_type;
      vector_data_type const value_data;

      typedef typename s_same_select_ref<return_t>::type return_storage_type;
      return_storage_type r0;

    
    




      
      
      template <class F, class vector_data_type_ = vector_data_type, class return_type_ = return_storage_type>
        struct s_internal_utility
      {
        typedef typename boost::function_types::parameter_types<F>::type  seq_parameters_;
        typedef typename boost::function_types::result_type<F>::type      ret_parameters;
        typedef boost::function_types::is_member_pointer<F>               ic_is_mem;


#if 0
        // simple stupid test (for development)
        typedef typename fusion::result_of::size<vector_data_type_>::type v;
        BOOST_MPL_ASSERT_RELATION(v::value, ==, 3);
#endif


        // static assertion of conversion feasibility (the convertor has been defined)
        
        // remove the first argument in case of member function
        typedef typename mpl::eval_if<
          ic_is_mem, 
          mpl::pop_front<seq_parameters_>,
          seq_parameters_>::type seq_parameters_without_this;

        /*typedef typename mpl::transform<
          seq_parameters_without_this, 
          transform_arguments_for_convertors
        >::type transformed_seq_parameters_without_this;*/
        
        typedef seq_parameters_without_this transformed_seq_parameters_without_this;


#if 0
        // Asserts all conversions are at least compile time convertible, with regards to the provided storage for data (the fusion vector)
        typedef typename mpl::transform_view<
          mpl::zip_view< mpl::vector<vector_data_type_, transformed_seq_parameters_without_this> >,
          mpl::unpack_args<s_convertor_wrapper<mpl::_1, mpl::_2> > 
        >::type zip_fusion_vector_and_target_function;

        typedef typename mpl::fold<
          zip_fusion_vector_and_target_function, 
          mpl::true_, 
          mpl::and_<s_convertor_extractor_<mpl::_2>, mpl::_1> 
        >::type are_all_compile_time_convertible;


        // Asserts all conversion are compile time possible, with regards to the values provided in the dispatch template parameters
        typedef typename mpl::transform_view<
          mpl::zip_view< mpl::vector<convertors_args_seq_type, transformed_seq_parameters_without_this> >,
          mpl::unpack_args<s_convertor_wrapper<mpl::_1, mpl::_2> > 
        >::type zip_dispatch_templates_and_target_function;

        typedef typename mpl::fold<
          zip_dispatch_templates_and_target_function, 
          mpl::true_, 
          mpl::and_<s_convertor_extractor_<mpl::_2>, mpl::_1> 
        >::type are_all_compile_time_convertible_for_dispatch;
#endif


        typedef s_convertor_wrapper<
          return_type_, 
          ret_parameters> return_convertor_type;


        // Object holding the convertors
        // Raffi : ERREUR sur le deuxième paramètre
        typedef s_convertor_holder<
          vector_data_type_,
          transformed_seq_parameters_without_this/*seq_parameters_without_this*/>      holder_type;
        //holder_type vector_dispatchers;//holder;
        
        typedef typename holder_type::is_convertor_defined are_all_compile_time_convertible_for_dispatch;
        typedef are_all_compile_time_convertible_for_dispatch are_all_compile_time_convertible;
        
        
        typename fusion::traits::deduce_sequence<typename holder_type::result_type>::type vector_dispatchers;
        //typename holder_type::result_type   vector_dispatchers;

        //return_convertor_type               return_convertor;

        // Function invocation wrapper (should contain a reference to the return type
        s_return_handler<return_type_, return_storage_type, ret_parameters>    op_invoke;

        s_internal_utility(
          typename add_reference<typename add_const<vector_data_type_>::type>::type value_data, 
          typename add_reference<return_type_>::type r0) : 
          vector_dispatchers(holder_type()(value_data)), 
          //return_convertor(r0), 
          op_invoke(r0)
        {
          // All argument convertors exist
          //BOOST_MPL_ASSERT((are_all_compile_time_convertible));
          //BOOST_MPL_ASSERT((are_all_compile_time_convertible_for_dispatch));
          BOOST_STATIC_ASSERT(are_all_compile_time_convertible_for_dispatch::value);
          YAYI_DBG_DISPATCH("s_internal_utility : are_all_compile_time_convertible_for_dispatch: " 
            << std::endl << "\t" << errors::demangle(typeid(are_all_compile_time_convertible_for_dispatch).name()) << std::endl);
          
          // Return type convertor exists
          BOOST_STATIC_ASSERT(return_convertor_type::convertor_type::type::value);
        }

        yayi::yaRC init()
        {
          // Runtime test of convertibility
          try 
          {
            if(!op_invoke.is_convertible() || !fusion::fold(vector_dispatchers, true, is_convertible()))
            {
              return yayi::yaRC_E_not_implemented;
            }
          }
          catch(yayi::errors::yaException & DEBUG_ONLY_VARIABLE(e)) 
          {
            DEBUG_INFO("Exception caught during the convertibility test. Details:\n" + e.message());
            return yayi::yaRC_E_not_implemented;
          }
          catch(...) 
          {
            DEBUG_INFO("Unknown exception caught during the convertibility test");
            return yayi::yaRC_E_not_implemented;
          }
          return yayi::yaRC_ok;
        }
        

        yayi::yaRC operator()(F& function) 
        {
          try
          {
            op_invoke.invoke(function, vector_dispatchers);
          }
          catch(yayi::errors::yaException & DEBUG_ONLY_VARIABLE(e))
          {
            DEBUG_INFO("Exception caught during the function call. Details:\n" + e.message());
            return yayi::yaRC_E_unknown;
          }
          catch(...)
          {
            DEBUG_INFO("Unknown exception caught during the function call (no details)");
            return yayi::yaRC_E_unknown;
          }

          return yayi::yaRC_ok;

        }

        template <class U>
        yayi::yaRC operator()(F& function, U& u) 
        {
          try
          {
            op_invoke.invoke(function, vector_dispatchers, u);
          }
          catch(yayi::errors::yaException & DEBUG_ONLY_VARIABLE(e))
          {
            DEBUG_INFO("Exception caught during the convertibility test. Details:\n" + e.message());
            return yayi::yaRC_E_unknown;
          }
          catch(...)
          {
            return yayi::yaRC_E_unknown;
          }

          return yayi::yaRC_ok;

        }
          

      };
    



    public:
      s_dispatcher(
        typename s_same_select_ref<R0>::type r  = R0(), 
        typename s_same_select_ref<A1>::type a1 = A1(), 
        typename s_same_select_ref<A2>::type a2 = A2(), 
        typename s_same_select_ref<A3>::type a3 = A3(), 
        typename s_same_select_ref<A4>::type a4 = A4(), 
        typename s_same_select_ref<A5>::type a5 = A5(), 
        typename s_same_select_ref<A6>::type a6 = A6()) : 
          value_data(fusion::remove_if<remove_void_arguments_>(fusion::make_vector(boost::ref(a1), boost::ref(a2), boost::ref(a3), boost::ref(a4), boost::ref(a5), boost::ref(a6)))), 
          r0(r)
      {
      }


      //! Generating a template function in which the convertors are automatically instanciated
      template <class F> 
        yayi::yaRC operator()(F function) const
      {
        s_internal_utility<F> op(this->value_data, this->r0);
        yayi::yaRC ret = op.init();
        if(ret != yayi::yaRC_ok) return ret;
        return op(function);
      }

      //! Generating a template function in which the convertors are automatically instanciated (member function version)
      template <class F, class U> 
        yayi::yaRC operator()(F function, U &u) const
      {
        s_internal_utility<F> op(this->value_data, this->r0);
        yayi::yaRC ret = op.init();
        if(ret != yayi::yaRC_ok) return ret;
        return op(function, u);
      }
      
      


      struct s_return_fold
      {
        yayi::yaRC ret;
        bool b_convert_ok;

        s_return_fold(const yayi::yaRC& r = yayi::yaRC_E_unknown, bool b_convert = false) : ret(r), b_convert_ok(b_convert){}
      };
      
      struct s_function_set_invocator
      {
        typedef s_return_fold result_type;
        this_type const& dispatcher_;

        s_function_set_invocator(this_type const& d) : dispatcher_(d) {}
        
        template <class F>
        #if ( (((BOOST_VERSION  / 100) % 1000) >= 42) && ((BOOST_VERSION /  100000) >= 1) )
          result_type operator()(result_type s, F function) const
        #else
          result_type operator()(F function, result_type s) const
        #endif
        {
          if(s.b_convert_ok)
            return s;

          yayi::yaRC& ret = s.ret;
          
          s_internal_utility<F> op(dispatcher_.value_data, dispatcher_.r0);
          YAYI_DBG_DISPATCH("dispatcher init " << errors::demangle(typeid(F).name()) << std::endl << std::endl);
          ret = op.init();
          YAYI_DBG_DISPATCH("dispatcher init end " << errors::demangle(typeid(F).name()) << std::endl << std::endl);
          if(ret != yayi::yaRC_ok) return ret;
          YAYI_DBG_DISPATCH("-> dispatcher init ok " << errors::demangle(typeid(F).name()) << std::endl << std::endl);
          
          s.b_convert_ok = true;
          
          ret = op(function);
          return s;
        }
      
      };
      
      friend struct s_function_set_invocator;
      
      
      
      template <class vector_functions>
      yayi::yaRC calls_first_suitable(vector_functions v) const
      {
        s_function_set_invocator proc(*this);
        s_return_fold ret = fusion::fold(v, s_return_fold(), proc);
        return ret.b_convert_ok ? ret.ret : yayi::yaRC_E_not_implemented;
      }

    };

  }
}

#endif


