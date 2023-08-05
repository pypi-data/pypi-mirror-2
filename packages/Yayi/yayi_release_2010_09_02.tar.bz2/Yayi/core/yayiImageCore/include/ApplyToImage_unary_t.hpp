/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_APPLY_TO_IMAGE_UNARY_HPP__
#define YAYI_APPLY_TO_IMAGE_UNARY_HPP__

/*!@file
 * This file defines the unary operators on images.
 * @todo: add multithreading
 */


#include <Yayi/core/yayiImageCore/include/ApplyToImage_T.hpp>


namespace yayi
{




  
  



  //! Specializing of s_apply_op_range for independant iterators and unary operators
  template <class it_strategy /*= iterators_independant_tag*/>
  struct s_apply_op_range<it_strategy, operator_type_unary_no_return>
  {
    template <class op_, class iter1, class image1>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, image1&)
    {
      for(; it1 != it1e; ++it1){
        op(*it1);
      }
      return yaRC_ok;
    }
  };
    
  //! Specializing of s_apply_op_range for independant iterators and unary operators with return value
  template <class it_strategy /*= iterators_independant_tag*/>
  struct s_apply_op_range<it_strategy, operator_type_unary>
  {
    //! Unary operation with return value
    template <class op_, class iter1, class iter2, class image1, class image2>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, iter2 it2, const iter2 it2e, image1&, image2&)
    {    
      // todo : some cases where im1 == im2 && it1 == it2 && it1e == it2e should be optimized
      for(; it1 != it1e && it2 != it2e; ++it1, ++it2){
        *it2 = op(*it1);
      }
      return yaRC_ok;
    }
  };

  //! Specializing of s_apply_op_range for iterators sharing the same offset configuration
  template <>
  struct s_apply_op_range<iterators_same_offset_tag, operator_type_unary>
  {
    //! Unary operation with return value
    template <class op_, class iter1, class iter2, class image1, class image2>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, iter2, const iter2, image1& im1, image2& im2)
    {
      for(; it1 != it1e; ++it1){
        const offset o = it1.Offset();
        im2.pixel(o) = op(im1.pixel(o));
      }
      return yaRC_ok;
    }
  };

  //! Specializing of s_apply_op_range for iterators sharing the same offset configuration
  template <>
  struct s_apply_op_range<iterators_same_offset_shifted_tag, operator_type_unary>
  {
    //! Unary operation with return value
    template <class op_, class iter1, class iter2, class image1, class image2>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, iter2 it2, const iter2 it2e, image1& im1, image2& im2)
    {
      if(it1 != it1e && it2 != it2e)
      {
        const offset shift = it2.Offset() - it1.Offset();
        for(; it1 != it1e; ++it1){
          const offset o = it1.Offset();
          im2.pixel(o + shift) = op(im1.pixel(o));
        }
      }
      return yaRC_ok;
    }
  };

  //! Specializing of s_apply_op_range for iterators sharing the same offset configuration
  template <>
  struct s_apply_op_range<iterators_same_offset_and_same_images_tag, operator_type_unary>
  {
    //! Unary operation with return value
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename enable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type    
    operator()(op_& op, iter1, iter1, iter2 it2, const iter2 it2e, image1& im1, image2&)
    {
      typedef typename image2::reference ref_t;
      for(; it2 != it2e; ++it2){
        ref_t p = *it2;
        p = op(p);
      }
      return yaRC_ok;
    }

    template <class op_, class iter1, class iter2, class image1, class image2>
    typename disable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type 
    operator()(op_&, iter1, const iter1, iter2, const iter2, image1&, image2&)
    {
      YAYI_THROW("This function should never be called : the program is ill-formed !");
    }
  };

  //! Specializing of s_apply_op_range for iterators sharing the same pointer representation
  template <>
  struct s_apply_op_range<iterators_same_pointer_and_same_images_tag, operator_type_unary>
  {
    //! Unary operation with return value
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename enable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type
    operator()(
      op_& op, 
      iter1 DEBUG_ONLY_VARIABLE(it1), iter1 DEBUG_ONLY_VARIABLE(it1e), 
      iter2 it2, iter2 it2e, 
      image1& DEBUG_ONLY_VARIABLE(im1), 
      image2& im2)
    {
      DEBUG_ASSERT(im1 == im2, "Image are not the same! program is ill formed");
      typedef typename image2::reference ref_t;
      typedef typename boost::add_pointer<typename boost::remove_reference<ref_t>::type>::type p_type;
      
      p_type p1 = &(*it2), p2 = &(*(--it2e)); // add const to p2
    
      #ifndef NDEBUG
      // some checks for the debug version
      for(; p1 <= p2; ++p1, ++it2){
        *p1 = op(*p1);
      } 
      YAYI_ASSERT(it2 == ++it2e, "Iterators are differents");

      #else
      for(; p1 <= p2; ++p1){
        *p1 = op(*p1);
      }
      #endif
      return yaRC_ok;
    }

    #if 1
    // Raffi: this is needed because of the main switch, but should disapear soon
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename disable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type    
    operator()(op_&, iter1, const iter1, iter2, const iter2, image1&, image2&)
    {
      YAYI_THROW("This function should never be called : the program is ill-formed !");
    }
    #endif
  };




  //! Specializing of s_apply_op_range for iterators with a pointer representation
  template <>
  struct s_apply_op_range<iterators_same_pointer_and_same_images_tag, operator_type_unary_no_return>
  {
    template <class op_, class iter1, class image1>
    yaRC operator()(op_& op, iter1 it1, iter1 it1e, image1&)
    {
      typedef typename iter1::reference ref_t;
      typedef typename boost::add_pointer<typename boost::remove_reference<ref_t>::type>::type p_type;
      
      p_type p1 = &(*it1), p2 = &(*(--it1e)); // add const to p2
    
      #ifndef NDEBUG
      // some checks for the debug version
      for(; p1 <= p2; ++p1, ++it1){
        op(*p1);
      } 
      YAYI_ASSERT(it1 == ++it1e, "Iterators are differents");
      
      #else
      for(; p1 <= p2; ++p1){
        op(*p1);
      }
      #endif
      return yaRC_ok;
    }

  };



  
  /*!@brief Unary operator functor over an image
   *
   * @author Raffi Enficiaud
   */
  struct s_apply_unary_operator
  {

  private:
    template <class iterator_extractor_t, class image_in_out, class op_>
    yaRC apply(image_in_out& im, op_& op) const
    {
      //BOOST_STATIC_ASSERT(is_void<typename op_::result_type>::value);
      typedef s_iterator_extractor<iterator_extractor_t> extractor_type;
      
      extractor_type extractor;
      
      typedef typename extractor_type::template results<extractor_type(image_in_out&)>::type result_type;
      
      const result_type iterators(extractor(im));
      typename result_type::first_type        it  = iterators.first;
      typename result_type::second_type const ite = iterators.second;
      
      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< op_(typename result_type::first_type::reference) >::type range_type_with_potential_return;
      typedef typename s_remove_return<range_type_with_potential_return>::type range_type;
      
      
      // Here we can add more precision on the type of 
      s_apply_op_range<iterators_same_pointer_and_same_images_tag, range_type> op_apply;
      
      return op_apply(op, it, ite, im);
    }

    // TODO : separate the extractors for each image
    template <class iterator_extractor_t, class image_in, class image_out, class op_>
    yaRC apply(image_in& im, image_out& out, op_& op) const
    {
      //BOOST_STATIC_ASSERT(is_void<typename op_::result_type>::value);
      typedef s_iterator_extractor<iterator_extractor_t> extractor_type;
      
      extractor_type extractor;
      
      typedef typename extractor_type::template results<extractor_type(image_in&)>::type itrange_in_t;
      typedef typename extractor_type::template results<extractor_type(image_out&)>::type itrange_out_t;
      
      itrange_in_t const iterators_in(extractor(im));
      typename itrange_in_t::first_type        it   = iterators_in.first;
      typename itrange_in_t::second_type const ite  = iterators_in.second;
      
      itrange_out_t const iterators_out(extractor(out));
      typename itrange_out_t::first_type        ito = iterators_out.first;
      typename itrange_out_t::second_type const itoe= iterators_out.second;
      
      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< op_(typename itrange_in_t::first_type::reference) >::type range_type;
      
      
      switch(iterator_strategy(im, out))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_pointer_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);      
        }
        
        case eis_same_offset_same_pointer_type:
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);
        }
        
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);
        }
    
      }  
      
    }
    


    //! Applyer on images with support rectangle definition
    template <class iterator_extractor1_t, class iterator_extractor2_t, class image_in, class image_out, class op_>
    yaRC apply(
      image_in& im, 
      const s_hyper_rectangle<image_in::coordinate_type::static_dimensions> &rect_in,
      image_out& out, 
      const s_hyper_rectangle<image_out::coordinate_type::static_dimensions> &rect_out,
      op_& op) const
    {
      typedef s_iterator_extractor<iterator_extractor1_t> extractor1_type;
      typedef s_iterator_extractor<iterator_extractor2_t> extractor2_type;
      typedef const s_hyper_rectangle<image_in::coordinate_type::static_dimensions>  rect_in_t;
      typedef const s_hyper_rectangle<image_out::coordinate_type::static_dimensions> rect_out_t;
      
      extractor1_type extractor1;
      extractor2_type extractor2;
      
      typedef typename extractor1_type::template results<extractor1_type(image_in&, rect_in_t&)>::type    itrange_in_t;
      typedef typename extractor2_type::template results<extractor2_type(image_out&, rect_out_t&)>::type  itrange_out_t;
      
      itrange_in_t const iterators_in(extractor1(im, rect_in));
      typename itrange_in_t::first_type        it   = iterators_in.first;
      typename itrange_in_t::second_type const ite  = iterators_in.second;
      
      itrange_out_t const iterators_out(extractor2(out, rect_out));
      typename itrange_out_t::first_type        ito   = iterators_out.first;
      typename itrange_out_t::second_type const itoe  = iterators_out.second;
      
      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< op_(typename itrange_in_t::first_type::reference) >::type range_type;
      
      
      switch(iterator_strategy<typename itrange_in_t::first_type, typename itrange_out_t::first_type>(im, rect_in, out, rect_out))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_offset_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);      
        }
        
        case eis_same_offset_same_pointer_type:
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);
        }
        case eis_same_offset_shifted:
        {
          s_apply_op_range<iterators_same_offset_shifted_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);
        }
        
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it, ite, ito, itoe, im, out);
        }
    
      }  
      
    }      



  public:
    template <class image_in_out, class op_>
    yaRC operator()(image_in_out& im, op_& op) const
    {
      return apply<iterator_choice_strategy_non_windowed_tag>(im, op);
    }

    template <class image_in, class image_out, class op_>
    yaRC operator()(const image_in& im, image_out& out, op_& op) const
    {
      return apply<iterator_choice_strategy_non_windowed_tag>(im, out, op);
    }

    //! Windowed operator on unary functors
    template <class image_in, class image_out, class op_>
    yaRC operator()(
      const image_in& im, 
      const s_hyper_rectangle<image_in::coordinate_type::static_dimensions> &rect_in,
      image_out& out, 
      const s_hyper_rectangle<image_out::coordinate_type::static_dimensions> &rect_out,
      op_& op) const
    {
      switch(iterator_extractor(im, rect_in))
      {
      
      case eic_non_windowed:
        {
          switch(iterator_extractor(out, rect_out))
          {
          case eic_non_windowed:
            return apply<iterator_choice_strategy_non_windowed_tag, iterator_choice_strategy_non_windowed_tag>(im, rect_in, out, rect_out, op);
          case eic_windowed:
            return apply<iterator_choice_strategy_non_windowed_tag, iterator_choice_strategy_windowed_tag>(im, rect_in, out, rect_out, op);
          default:
            YAYI_THROW("Unsupported case " + any_to_string(iterator_extractor(out, rect_out)));
          }
        }
      
      case eic_windowed:
        {
          switch(iterator_extractor(out, rect_out))
          {
          case eic_non_windowed:
            return apply<iterator_choice_strategy_windowed_tag, iterator_choice_strategy_non_windowed_tag>(im, rect_in, out, rect_out, op);
          case eic_windowed:
            return apply<iterator_choice_strategy_windowed_tag, iterator_choice_strategy_windowed_tag>(im, rect_in, out, rect_out, op);
          default:
            YAYI_THROW("Unsupported case " + any_to_string(iterator_extractor(out, rect_out)));
          }
        }

      default:
        YAYI_THROW("Unsupported case " + any_to_string(iterator_extractor(im, rect_in)));
      }
    }

  };





}



#endif /* YAYI_APPLY_TO_IMAGE_UNARY_HPP__ */

