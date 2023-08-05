/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_APPLY_TO_IMAGE_HPP__
#define YAYI_APPLY_TO_IMAGE_HPP__


/*!@file
 * Contains necessary function to iterator operators over images
 *
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <Yayi/core/yayiCommon/include/common_string_utilities.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>

#include <boost/function_types/function_type.hpp>
#include <boost/function_types/result_type.hpp>
#include <boost/function_types/parameter_types.hpp>
#include <boost/function_types/function_arity.hpp>
#include <boost/function_types/is_member_pointer.hpp>


#include <boost/static_assert.hpp>
#include <boost/mpl/has_xxx.hpp>
#include <boost/utility/result_of.hpp>
#include <boost/function_types/result_type.hpp>



namespace yayi
{

  /*! Strategy to be used for requesting the iterators for more than one image algorithms
   *
   */
  typedef enum e_point_processing_iterator_strategy
  {
    eis_all_different,                      //!< every iterator has to be iterated
    eis_same_offset,                        //!< only one of the iterators can be used if the algorithm shares the offset
    eis_same_offset_shifted,                //!< only one of the iterators can be used if the algorithm shares a shifted offset
    eis_window_maximal_same_pointer,        //!< the iterator over the whole image can be used, one iterator can be used if the algorithm shares the pointer difference
    eis_same_offset_same_pointer_type       //!< the images are offset compatible and have the same pointer arithmetic. 
  } point_processing_iterator_strategy;



  typedef enum e_iterator_choice_strategy
  {
    eic_non_windowed,                       //!< used to indicate that the non windowed iterator should or can be extracted from the image
    eic_windowed                            //!< used to indicate that the windowed iterator should be used
  } iterator_choice_strategy;


  //! This tag is for extracting the block version of the iterator
  struct iterator_choice_strategy_non_windowed_tag  {};
  //! This tag is for extracting the windowed version of the iterator
  struct iterator_choice_strategy_windowed_tag      {};



  template <class image>
  iterator_choice_strategy iterator_extractor(const image& im, const s_hyper_rectangle<image::coordinate_type::static_dimensions> &rect_in)
  {
    return (rect_in.Size() == im.Size() ? eic_non_windowed : eic_windowed);
  }
  
  template <class image1, class image2>
  iterator_choice_strategy iterator_extractor(
    const image1& im1, 
    const s_hyper_rectangle<image1::coordinate_type::static_dimensions> &rect_im1,
    const image2& im2,
    const s_hyper_rectangle<image2::coordinate_type::static_dimensions> &rect_im2)
  {
    // here we can have a better criterion based on the subspace spanned by the hyperrectangles and the geometry of the images...
    if(im1.Size() == rect_im1.Size() && im2.Size() == rect_im2.Size())
      return eic_non_windowed;
    return eic_windowed;
  }
  
  template <class image1, class image2, class image3>
  iterator_choice_strategy iterator_extractor(const image1& im1, const image2& im2, const image3& im3)
  {
    return eic_non_windowed;
  }
  
  
  
  namespace ns_operator_tag {
  
    /*! The operator tags define some properties of the operators
     *  These properties would allow optimization at run time by splitting (or not) the pixel set into smaller ones,
     *  distributed on different computational units (threads, cpu or machines).
     */
     
    struct operator_no_tag;
    
    
    /*! This tag means that the underlying operator is insensitive to the order of the points on which it is applied to
     *  Example:
     *  \[T(a_1, a_2, ..., a_n) = T({a_i}_{i \in \N^*_n}) = T(a_2, a_1, ..., a_n) = ...\]
     */
    struct operator_commutative {};

    /*! The used operator is a "partition set morphism". This means
     *  that the processing can be split into smaller processings, for instance (T stands for the operator, + is the operator 
     *  in the destination monoid):
     *  
     *  \[\forall j \in \N^*_n, T(a_1, a_2, ..., a_n) = T(a_1, ..., a_j) + T(a_{j+1}, ..., a_n)\]
     */
    struct operator_partition_set_morphism;
  
  
    BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(has_operator_tag, operator_tag, false);

  
  }






  /*!@brief Return the best strategy from the runtime informations over the images for using the iterators and the pixel accesses.
   *
   * @author Raffi Enficiaud
   */
  template <class image1, class image2>
  point_processing_iterator_strategy iterator_strategy(const image1& im1, const image2& im2)
  {
    if(are_images_same(im1, im2))
    {
      return eis_window_maximal_same_pointer;
    }

    if(are_same_geometry(im1, im2))
    {
      // same geometry : if the windows are mxiaml, only one iterator can be used
      if(are_images_same_type(im1, im2))
        return eis_same_offset_same_pointer_type;
      else
        return eis_same_offset;
    }
    
    // TODO : add other type of optimizations
    return eis_all_different;
  }
   
  template <class image1, class image2, class image3>
  point_processing_iterator_strategy iterator_strategy(const image1& im1, const image2& im2, const image3& im3)
  {
    if(are_images_same(im1, im2) && are_images_same(im1, im3))
    {
      return eis_window_maximal_same_pointer;
    }

    if(are_same_geometry(im1, im2) && are_same_geometry(im1, im3))
    {
      // same geometry : if the windows are mxiaml, only one iterator can be used
      if(are_images_same_type(im1, im2) && are_images_same_type(im1, im3))
        return eis_same_offset_same_pointer_type;
      else
        return eis_same_offset;
    }

    // TODO : add other type of optimizations
    return eis_all_different;
  }

  template <class image1, class image2, class image3, class image4>
  point_processing_iterator_strategy iterator_strategy(const image1& im1, const image2& im2, const image3& im3, const image4& im4)
  {
    if(are_same_geometry(im1, im2) && are_same_geometry(im1, im3) && are_same_geometry(im1, im4))
    {
      // same geometry : if the windows are mxiaml, only one iterator can be used
      if(are_images_same_type(im1, im2) && are_images_same_type(im1, im3) && are_images_same_type(im1, im4))
        return eis_same_offset_same_pointer_type;
      else
        return eis_same_offset;
    }

    // TODO : add other type of optimizations
    return eis_all_different;
  }

  template <class image1, class image2, class image3, class image4, class image5>
  point_processing_iterator_strategy iterator_strategy(const image1& im1, const image2& im2, const image3& im3, const image4& im4, const image5& im5)
  {
    if(are_same_geometry(im1, im2) && are_same_geometry(im1, im3) && are_same_geometry(im1, im4) && are_same_geometry(im1, im5))
    {
      // same geometry : if the windows are mxiaml, only one iterator can be used
      if(are_images_same_type(im1, im2) && are_images_same_type(im1, im3) && are_images_same_type(im1, im4) && are_images_same_type(im1, im5))
        return eis_same_offset_same_pointer_type;
      else
        return eis_same_offset;
    }

    // TODO : add other type of optimizations
    return eis_all_different;
  }


  template <class image1, class image2, class it1, class it2>
  struct s_iterator_strategy_helper
  {
    point_processing_iterator_strategy operator()(
      const image1& im1, 
      const s_hyper_rectangle<image1::coordinate_type::static_dimensions> &rect_im1,
      const image2& im2,
      const s_hyper_rectangle<image2::coordinate_type::static_dimensions> &rect_im2) const
    {
      return eis_all_different;
    }
  };

  template <class image1, class image2, class it1>
  struct s_iterator_strategy_helper<image1, image2, it1, it1>
  {
    point_processing_iterator_strategy operator()(
      const image1& im1, 
      const s_hyper_rectangle<image1::coordinate_type::static_dimensions> &rect_im1,
      const image2& im2,
      const s_hyper_rectangle<image2::coordinate_type::static_dimensions> &rect_im2) const
    {
      // The two images are the same, in case the window is maximal, the pointer only can be used
      if(are_images_same(im1, im2) && (rect_im1 == rect_im2 && rect_im1.Size() == im1.Size()))
      {
        return eis_window_maximal_same_pointer;
      }
    
      // The two images have the same geometry
      if(are_same_geometry(im1, im2))
      {
        // if the images are of the same type, the pointer differences can be used (instead of an offset involving a multiplication)
        if(rect_im1 == rect_im2)
        {
          if(are_images_same_type(im1, im2))
            return eis_same_offset_same_pointer_type;
          return eis_same_offset;
        }
        
        if(rect_im1.Size() == rect_im2.Size())
          return eis_same_offset_shifted;
      }
    
    
      // TODO : add other type of optimizations
      return eis_all_different;
    }
  };

  template <class it1, class it2, class image1, class image2>
  point_processing_iterator_strategy iterator_strategy(
    const image1& im1, 
    const s_hyper_rectangle<image1::coordinate_type::static_dimensions> &rect_im1,
    const image2& im2,
    const s_hyper_rectangle<image2::coordinate_type::static_dimensions> &rect_im2)
  {
    s_iterator_strategy_helper<image1, image2, it1, it2> op;
    return op(im1, rect_im1, im2, rect_im2);
  }



  
  
  namespace {


    //! Utility for extracting the correct range of iterators from images
    template <class> 
    struct s_iterator_extractor;

    //! Extracts the correct range of non-windowed iterators from the provided image
    template <> 
    struct s_iterator_extractor<iterator_choice_strategy_non_windowed_tag>
    {
      typedef s_iterator_extractor<iterator_choice_strategy_non_windowed_tag> this_type;
      template <class T> struct results;

      template <class self_, class image> struct results<self_(image&)> {
        typedef typename boost::mpl::if_<
          boost::is_const<image>, 
          typename image::const_iterator, 
          typename image::iterator>::type iterator_type;
        typedef std::pair<iterator_type, iterator_type>   type;
      };
      
      template <class self_, class image, int dim> 
      struct results<self_(image&, const s_hyper_rectangle<dim>&)> 
      {
        typedef typename boost::mpl::if_<
          boost::is_const<image>, 
          typename image::const_iterator, 
          typename image::iterator>::type iterator_type;
        typedef std::pair<iterator_type, iterator_type>   type;
      };      
      
      
      // the image is either const or not const, the compiler knows. The only 
      // important fact is the return type, the called methods are the same.
      template <class image>
      typename results<this_type(image&)>::type operator()(image& im) const
      {
        return std::make_pair(im.begin_block(), im.end_block());
      }
      
      // the image is either const or not const, the compiler knows. The only 
      // important fact is the return type, the called methods are the same.
      // The second parameter is simply ignored here
      template <class image>
      typename results<this_type(image&, const s_hyper_rectangle<image::coordinate_type::static_dimensions>&)>::type 
      operator()(
        image& im, 
        const s_hyper_rectangle<image::coordinate_type::static_dimensions> &) const
      {
        return std::make_pair(im.begin_block(), im.end_block());
      }
    
    };

    //! Extracts the correct range of windowed iterators from the provided image
    template <> 
    struct s_iterator_extractor<iterator_choice_strategy_windowed_tag>
    {
      typedef s_iterator_extractor<iterator_choice_strategy_windowed_tag> this_type;
      template <class T> struct results;

      template <class self_, class image> 
      struct results< self_(image&, const s_hyper_rectangle<image::coordinate_type::static_dimensions> )> {
        typedef typename boost::mpl::if_<
          boost::is_const<image>, 
          typename image::const_window_iterator, 
          typename image::window_iterator>::type iterator_type;

        typedef std::pair<iterator_type, iterator_type>   type;
      };

      template <class self_, class image, int dim> 
      struct results<self_(image&, const s_hyper_rectangle<dim>&)> 
      {
        typedef typename boost::mpl::if_<
          boost::is_const<image>, 
          typename image::const_window_iterator, 
          typename image::window_iterator>::type iterator_type;
        typedef std::pair<iterator_type, iterator_type>   type;
      };    

      // the image is either const or not const, the compiler knows. The only 
      // important fact is the return type, the called methods are the same.
      template <class image> 
      typename results<this_type(image&, const s_hyper_rectangle<image::coordinate_type::static_dimensions>&)>::type 
      operator()(
        image& im, 
        const s_hyper_rectangle<image::coordinate_type::static_dimensions> &rect) const
      {
        return std::make_pair(
           im.begin_window(rect.lowerleft_corner, rect.Size()), 
           im.end_window(rect.lowerleft_corner, rect.Size()));
      }
    };

  }








  struct iterators_independant_tag            {};     //!< The input iterators are independant
  struct iterators_same_number_of_points_tag  {};     //!< The input iterators are iterating over the same number of points (useful ?)
  struct iterators_same_offset_tag            {};     //!< The iterators have the same offset structure
  struct iterators_same_offset_shifted_tag    {};     //!< The iterators have the same offset structure, with a constant shift
  struct iterators_same_offset_and_same_images_tag {};     //!< Same as iterators_same_offset_tag but the images are also the same
  struct iterators_same_pointer_and_same_images_tag{};     //!< The iterator can be bypassed in order to used pointer increments in the iterator range

  struct operator_type_zero_ary               {};     //!< No input, but an output (eg. a generator)
  struct operator_type_zero_ary_no_return     {};     //!< No input, no output (eg. a counter)
  
  struct operator_type_unary                  {};     //!< An input and an output (eg. a transformer)
  struct operator_type_unary_no_return        {};     //!< An input but not output (eg. an applyier)
  
  struct operator_type_binary                 {};
  struct operator_type_binary_no_return       {};

  struct operator_type_ternary                {};
  struct operator_type_ternary_no_return      {};

  struct operator_type_fourary                {};
  struct operator_type_fourary_no_return      {};

  BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(operator_has_result_member_tag, result, false);


  namespace {
  
    template <class T> struct s_remove_return                   {typedef T type;};
    
    template <> struct s_remove_return<operator_type_zero_ary>  {typedef operator_type_zero_ary_no_return type; };
    template <> struct s_remove_return<operator_type_unary>     {typedef operator_type_unary_no_return type;    };
    template <> struct s_remove_return<operator_type_binary>    {typedef operator_type_binary_no_return type;   };
    template <> struct s_remove_return<operator_type_ternary>   {typedef operator_type_ternary_no_return type;  };
    template <> struct s_remove_return<operator_type_fourary>   {typedef operator_type_fourary_no_return type;  };
  
  }




  /*!@brief Utility structure for extracting the type of the supplied operator
   *
   * @author Raffi Enficiaud
   */
  struct s_extract_operator_type
  {
    template <class op_> struct result;
    
    // Revoir l'utilité de cette fonction ici. Grosso modo: on ne cherche pas à savoir le nombre de paramètres avec lequel
    // on appelle cette fonction, mais plutôt de connaitre le type de la fonction.
    template <class op_> 
    struct result< op_() > {
      typedef typename boost::result_of< op_() >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_zero_ary_no_return, 
        operator_type_zero_ary>::type type;
    };

    template <class op_, class T> 
    struct result< op_(T) > {
      typedef typename boost::result_of< op_(T) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_unary_no_return, 
        operator_type_unary>::type type;
    };

    template <class op_, class T, class U> 
    struct result< op_(T, U)> {
      typedef typename boost::result_of< op_(T, U) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_binary_no_return, 
        operator_type_binary>::type type;
    };

    template <class op_, class T, class U, class V> 
    struct result< op_(T, U, V)> {
      typedef typename boost::result_of< op_(T, U, V) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_ternary_no_return, 
        operator_type_ternary>::type type;
    };

    template <class op_, class T, class U, class V, class W> 
    struct result< op_(T, U, V, W)> {
      typedef typename boost::result_of< op_(T, U, V, W) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_fourary_no_return, 
        operator_type_fourary>::type type;
    };

  };
  
  typedef s_extract_operator_type operator_traits;

  //! Declaration of the iterator application utllity structure
  template <class iterators_interaction_t, class operator_type_t>
  struct s_apply_op_range;

  
}


#endif /* YAYI_APPLY_TO_IMAGE_HPP__ */

