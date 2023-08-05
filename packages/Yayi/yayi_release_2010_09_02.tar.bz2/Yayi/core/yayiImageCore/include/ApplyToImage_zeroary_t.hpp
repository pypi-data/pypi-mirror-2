/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_APPLY_TO_IMAGE_ZERO_HPP__
#define YAYI_APPLY_TO_IMAGE_ZERO_HPP__

/*!@file
 * This file defines operators on images with zero arity.
 * @todo: add multithreading
 */


#include <Yayi/core/yayiImageCore/include/ApplyToImage_T.hpp>



namespace yayi
{


  
  //! Specializing of s_apply_op_range for zero ary operators (no return)
  template <class iterator_type>
  struct s_apply_op_range<iterator_type, operator_type_zero_ary_no_return>
  {
    template <class op_, class iter1, class image1>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, image1&)
    {
      // to do: just count the number of element inside the iterator range would be enough there
      for(; it1 != it1e; ++it1){
        op();
      }
      return yaRC_ok;
    }
  };
  
  //! Specializing of s_apply_op_range for zero ary operators (with return)
  template <class iterator_type>
  struct s_apply_op_range<iterator_type, operator_type_zero_ary>
  {
    template <class op_, class iter1, class image1>
    yaRC operator()(op_& op, iter1 it1, const iter1 it1e, image1&)
    {
      for(; it1 != it1e; ++it1){
        *it1 = op();
      }
      return yaRC_ok;
    }
  };


  /*!@brief Unary operator functor over an image
   *
   * @author Raffi Enficiaud
   */
  struct s_apply_zeroary_operator
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
      typedef typename s_extract_operator_type::template result< op_() >::type range_type_with_potential_return;
      typedef typename s_remove_return<range_type_with_potential_return>::type range_type;
      
      // Here we can add more precision on the type of 
      s_apply_op_range<iterators_same_pointer_and_same_images_tag, range_type> op_apply;
      
      return op_apply(op, it, ite, im);
    }


    //! Applyer on images with support rectangle definition
    template <class iterator_extractor1_t, class image_inout, class op_>
    yaRC apply(
      const s_hyper_rectangle<image_inout::coordinate_type::static_dimensions> &rect_inout,
      image_inout& im,
      op_& op) const
    {
      typedef s_iterator_extractor<iterator_extractor1_t> extractor1_type;
      typedef const s_hyper_rectangle<image_inout::coordinate_type::static_dimensions>  rect_inout_t;
      
      extractor1_type extractor1;
      
      typedef typename extractor1_type::template results<extractor1_type(image_inout&, rect_inout_t&)>::type    itrange_inout_t;
      
      itrange_inout_t const iterators_inout(extractor1(im, rect_inout));
      typename itrange_inout_t::first_type        it   = iterators_inout.first;
      typename itrange_inout_t::second_type const ite  = iterators_inout.second;
      
      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< op_() >::type range_type_with_potential_return;
      typedef typename s_remove_return<range_type_with_potential_return>::type range_type;      
      
      switch(iterator_strategy<typename itrange_inout_t::first_type>(im, rect_inout))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_offset_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it, ite, im);      
        }
        
        case eis_same_offset_same_pointer_type:
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it, ite, im);
        }
        case eis_same_offset_shifted:
        {
          s_apply_op_range<iterators_same_offset_shifted_tag, range_type> op_apply;
          return op_apply(op, it, ite, im);
        }
        
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it, ite, im);
        }
    
      }  
      
    }      



  public:
    template <class image_in_out, class op_>
    yaRC operator()(image_in_out& im, op_& op) const
    {
      return apply<iterator_choice_strategy_non_windowed_tag>(im, op);
    }

    //! Windowed operator on unary functors
    template <class image_inout, class op_>
    yaRC operator()(
      const s_hyper_rectangle<image_inout::coordinate_type::static_dimensions> &rect_inout,
      image_inout& im, 
      op_& op) const
    {
      switch(iterator_extractor(im, rect_inout))
      {
      case eic_non_windowed:
        return apply<iterator_choice_strategy_non_windowed_tag>(im, rect_inout, op);
      case eic_windowed:
        return apply<iterator_choice_strategy_windowed_tag>(im, rect_inout, op);
      default:
        YAYI_THROW("Unsupported case " + any_to_string(iterator_extractor(im, rect_inout)));
      }
    }

  };




}

#endif 
