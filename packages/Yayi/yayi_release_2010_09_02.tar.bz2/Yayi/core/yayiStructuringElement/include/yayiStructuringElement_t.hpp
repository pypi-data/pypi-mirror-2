/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_STRUCTURING_ELEMENT_T_HPP__
#define YAYI_STRUCTURING_ELEMENT_T_HPP__



/*!@file 
 * This file contains a template structuring element definition
 * This work is not finished yet.
 * @author Raffi Enficiaud
 */

#include "Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp"



#include <boost/mpl/assert.hpp>
#include <boost/mpl/equal.hpp>
#include <boost/mpl/vector_c.hpp>
#include <boost/mpl/pair.hpp>
#include <boost/mpl/arithmetic.hpp>
#include <boost/mpl/begin_end.hpp>
#include <boost/mpl/iterator_range.hpp>
#include <boost/mpl/advance.hpp>
#include <boost/mpl/zip_view.hpp>
#include <boost/mpl/transform_view.hpp>
#include <boost/mpl/filter_view.hpp>
#include <boost/mpl/unpack_args.hpp>
#include <boost/mpl/vector.hpp>
#include <boost/mpl/range_c.hpp>

#include <boost/mpl/min_element.hpp>
#include <boost/mpl/max_element.hpp>

#include <boost/mpl/deref.hpp>
#include <boost/static_assert.hpp>
#include <boost/mpl/size.hpp>

#include <boost/mpl/insert_range.hpp>
#include <boost/mpl/accumulate.hpp>
#include <boost/mpl/back_inserter.hpp>
#include <boost/mpl/copy.hpp>

#include <boost/mpl/set.hpp>
#include <boost/mpl/map.hpp>
#include <boost/mpl/inserter.hpp>
#include <boost/mpl/insert.hpp>
#include <boost/mpl/empty.hpp>
#include <boost/mpl/front.hpp>
#include <boost/mpl/distance.hpp>
#include <boost/mpl/has_key.hpp>
#include <boost/mpl/lambda.hpp>
#include <boost/mpl/protect.hpp>
#include <boost/mpl/quote.hpp>


#include <boost/mpl/transform.hpp>
#include <boost/mpl/find_if.hpp>

#include <boost/mpl/copy_if.hpp>
#include <boost/mpl/void.hpp>

#include <boost/mpl/for_each.hpp>




namespace yayi {

  using namespace boost;

  /*! The template structuring element
   * This class defines several constants and methods available at compilation time, and making it easier to
   * design powerful meta-algorithms that use the geometry of the SE for optimizations
   *
   * @author Raffi Enficiaud
   */
  template <
    class dimension_ = mpl::int_<2>, 
    class coordinates_elements_ = mpl::vector_c<int> 
  >
  class se_t
  {
  public:
    typedef dimension_                                                dimension;              //!< The dimension of the SE
    typedef coordinates_elements_                                     coordinates_elements;   //!< The sequence of positions (non separated tuples) 
    typedef mpl::pair<dimension, coordinates_elements>                se_coordinate_type;
    typedef typename mpl::size<coordinates_elements>::type            size_coordinate;        //!< The number of coordinates
    typedef typename mpl::divides<size_coordinate, dimension>::type   nb_coordinate;          //!< The number of points in the SE

    // Should not have additionnal coordinates. 
    BOOST_MPL_ASSERT_RELATION( (mpl::modulus<size_coordinate, typename se_coordinate_type::first >::type::value), == , 0);

    //! Returns the uth element of the provided sequence
    template <class U>
    struct get_nth_coordinate
    {
      typedef typename mpl::iterator_range<
        typename mpl::advance<typename mpl::begin<coordinates_elements>::type, typename mpl::times<dimension, U>::type >::type,
        typename mpl::advance<typename mpl::begin<coordinates_elements>::type, typename mpl::times<dimension, typename mpl::plus<U, mpl::int_<1> >::type >::type >::type>::type type;
    };


    // A faire, les extensions maximales sur chaque dimension (le pavé de support)
    // L'extension maximale résumée sur toutes les dimensions 


    template <class U>
    struct extract_all_nth_dimension_vector
    {
      // Ensures the requested dimension is correct
      //BOOST_MPL_ASSERT_RELATION( U, <= , (typename se_coordinate_type::first) );
      BOOST_MPL_ASSERT( (boost::is_same<typename U::tag, mpl::integral_c_tag>) );
      
      typedef typename
        mpl::transform_view<
        mpl::filter_view<
        mpl::zip_view< mpl::vector<coordinates_elements, mpl::range_c<int, 0, size_coordinate::value > > >,
        mpl::unpack_args< mpl::equal_to< mpl::modulus< mpl::plus<mpl::_2, U >, typename se_coordinate_type::first > , mpl::int_<0> > >
        >, 
        mpl::unpack_args<mpl::_1> 
        >::type type;
    };


    //! Extract the nth vector point
    template <class U>
    struct extract_nth_point
    {
      // Ensures the requested dimension is correct
      //BOOST_MPL_ASSERT_RELATION( U, <= , (typename se_coordinate_type::first) );
      BOOST_MPL_ASSERT( (boost::is_same<typename U::tag, mpl::integral_c_tag>) );
      
      typedef typename mpl::advance<typename mpl::begin<coordinates_elements>::type, typename mpl::times<dimension, U >::type >::type begin_iterator;
      //typedef typename mpl::advance<typename mpl::begin<coordinates_elements>::type, typename mpl::times<dimension, typename mpl::plus<mpl::int_<1>, U>::type >::type >::type end_iterator;
      typedef typename mpl::advance<begin_iterator, dimension>::type end_iterator;
      
      typedef mpl::iterator_range<begin_iterator, end_iterator> type;
    };


    //! Returns U + V
    template <class V, class U>
    struct shift_point
    {
      typedef typename mpl::transform_view<
        mpl::zip_view< mpl::vector<V, U> >,
        mpl::unpack_args< mpl::plus<mpl::_1, mpl::_2> >
        >::type type;
    };


    //! Applies the shift given by vector U to all the points of the vector
    template <class U>
    struct shift_vector
    {
      typedef typename 
        mpl::transform_view<
          mpl::range_c<int, 0, nb_coordinate::value >,
          shift_point< extract_nth_point<mpl::_1>, typename U::type>
        >::type transformed_vector;
      
      typedef typename 
        mpl::accumulate<
          transformed_vector,
          mpl::vector_c<int>,
          mpl::copy<mpl::_2, mpl::back_inserter<mpl::_1> > 
        >::type type;
    };


    //! Returns the transpose of U, with V as the origin
    template <class U, class V>
    struct transpose_point
    {
      typedef typename mpl::transform_view<
        mpl::zip_view< mpl::vector<U, V> >,
        mpl::unpack_args< mpl::minus<mpl::_2, mpl::_1> >
        >::type type;
    };

    template <class U>
    struct transpose_point_origin 
    {
      typedef typename mpl::transform_view<
        U,
        mpl::negate<mpl::_1> 
        >::type type;
    };



    // Returns the minimum and maximum values around 0 along the specified (U) dimension
    template <class U>
    struct extract_min_max_extension_on_dimension
    {
      typedef typename extract_all_nth_dimension_vector<U>::type v_dimension;
      
      typedef typename mpl::min_element<v_dimension>::type iter_min;
      //BOOST_MPL_ASSERT_NOT((mpl::equal_to<iter_min, mpl::end<v_dimension> > ));
      
      typedef typename mpl::deref<iter_min>::type min_value_t;
      
      typedef typename mpl::max_element<v_dimension>::type iter_max;
      //BOOST_MPL_ASSERT_NOT((mpl::equal_to<iter_max, mpl::end<v_dimension> > ));
      
      typedef typename mpl::deref<iter_max>::type max_value_t;
      
    };

    //typename mpl::min_element<mpl::transform_view<mpl::range_c<int, 0, dimension::value>, extract_all_nth_dimension_vector<mpl::_> > >::type::value extension_min;



    template <class vector_delta>
    struct s_vectors_to_center
    {
      
      
      
    };



    // Une fonction donnant les points lorsqu'une operation est appliquée à chaque pixel
    // pour avoir une idée des positions entrantes et sortantes du vecteur de coordonnée.


    /*!@brief This structure informs the newly covered points and uncovered points when a shift of delta is applied on dimension U
     *
     */
    template <class delta>
    struct s_cover_uncover
    {
      //typedef typename extract_all_nth_dimension_vector<U>::type v_dimension;
      
      // Original paired vectors
      typedef typename mpl::copy<
        mpl::range_c<int, 0, nb_coordinate::value>,
        mpl::inserter<
          mpl::vector<>,
          mpl::push_back<mpl::_1, mpl::pair<
            mpl::_2, 
            extract_nth_point<mpl::_2> >
          >
        >
        >::type paired_se;    
      
      // Shifted paired vectors
      typedef typename mpl::copy<
        mpl::range_c<int, 0, nb_coordinate::value>,
        mpl::inserter<
          mpl::vector<>,
          mpl::push_back<mpl::_1, mpl::pair<
            mpl::_2, 
            shift_point<extract_nth_point<mpl::_2>, delta> > 
          >
        >
      >::type paired_shifted_se;
      
      
      template <class U, class V> struct s_vector_equal
      {
        typedef typename mpl::equal<typename U::second, V>::type type;
      };
      
      
      // Helper
      template <class VectorIndex, class VectorShifted, class VectorReference>
      struct s_cover_helper
      {
        typedef typename mpl::find_if<
          VectorShifted,
          s_vector_equal<mpl::_1, typename mpl::at<VectorReference, VectorIndex>::type::second>
          >::type iter_type;
        
        template <class It, class V, class I>
        struct s_correspondance_helper_inner
        {
          typedef typename mpl::pair<
            typename mpl::deref<It>::type::first,
            typename mpl::at<V, I>::type::first
            >::type type;
        };
        
        typedef typename 
          mpl::eval_if<
            boost::is_same<iter_type, typename mpl::end<VectorShifted>::type>,
            mpl::void_,
            s_correspondance_helper_inner<iter_type, VectorReference, VectorIndex> // normalement VectorIndex
          >::type type;
      };
      
      
      typedef typename mpl::transform_view<
        mpl::range_c<int, 0, nb_coordinate::value>, 
        s_cover_helper<mpl::_1, paired_shifted_se, paired_se> 
        >::type transformed_correspondance;
      
      typedef typename mpl::copy_if<
        transformed_correspondance,
        mpl::not_< boost::is_same<mpl::_1, mpl::void_> >,
        mpl::back_inserter< mpl::vector<> >
        >::type covered_points;
      
    };



    /*@param[in] v codes the dimensions of the image
     */
    template <class coordinate_vector>
    std::vector<int> operator()(const coordinate_vector& v) const
    {
      
      
      return std::vector<int>();
    }




  };

}
#endif

