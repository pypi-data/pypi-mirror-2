/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */





#include "main.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiStructuringElement_t.hpp"

#include <iostream>

using namespace yayi;





using namespace boost;




template< typename T1, typename T2 > struct f1
{
  typedef typename mpl::insert<T1, 
      mpl::pair<
      typename mpl::vector_c<int, 1, T2::value >::type, 
        typename T2::type > >::type type;
};



template <class U, class V>
  struct s_vector_equal
{
  typedef typename mpl::equal<typename U::second, V>::type type;
};

template <class VectorIndex, class Shift, class SE>
  struct s_shifter_helper
{
  typedef typename SE::template shift_point< typename SE::template extract_nth_point<VectorIndex>::type, Shift >::type type;
};



template <class VectorIndex, class VectorShifted, class VectorReference>
  struct s_correspondance_helper
{
  typedef typename mpl::at<VectorReference, VectorIndex>::type pair_to_find;
  typedef typename mpl::find_if<
    VectorShifted,
    s_vector_equal<mpl::_1, typename pair_to_find::second>
  >::type iter_type;

  typedef typename mpl::not_<
     boost::is_same<
      iter_type, 
      typename mpl::end<VectorShifted>::type
      >
  >::type is_found;
  
  template <class found, class iter_type, class pair_to_find> struct s_internal {typedef mpl::void_ type;};
  template <class iter_type, class pair_to_find> struct s_internal<mpl::true_, iter_type, pair_to_find> {
    typedef mpl::pair<
      typename mpl::deref<iter_type>::type::first,
      typename pair_to_find::first> type;};
  
  
  typedef typename /*dummy_rule::*/s_internal<is_found, iter_type, pair_to_find>::type type;
};




struct cover_printer
{
  template< typename U > void operator()(U x){
    std::cout << "\tinitial = " << U::first::value << "\tfinal = " << U::second::value /*<< "\t" << x */<< std::endl;
  }
};


class se_covering_forward_test 
{
public:

  void test_1()
  {

    // Most of these tests will be performed done at compilation time
    typedef boost::mpl::pair<
      boost::mpl::int_<2>, 
      boost::mpl::vector_c<int, -1,-1, 0,-1, 1,-1,  -1,0, 0,0, 1,0, -1,1, 0,1, 1,1 > 
    > se_coordinate_type__;

    typedef se_t<se_coordinate_type__::first, se_coordinate_type__::second::type> se_type;

    BOOST_CHECKPOINT("test_1");	


    // Should not have additionnal coordinates. 
    BOOST_MPL_ASSERT_RELATION( (mpl::modulus<se_type::size_coordinate, se_type::se_coordinate_type::first >::type::value), == , 0);
    BOOST_MPL_ASSERT_RELATION( se_type::nb_coordinate::value, ==, 9) ;
    BOOST_MPL_ASSERT_RELATION( (mpl::times<se_type::nb_coordinate, se_coordinate_type__::first >::type::value), ==, (se_type::size_coordinate::value) ) ;



    typedef se_type::get_nth_coordinate< mpl::int_<0> >::type coordinate_0;



    BOOST_MPL_ASSERT((mpl::equal<coordinate_0, boost::mpl::vector_c<int,-1,-1> > ));
    BOOST_MPL_ASSERT_NOT( (mpl::equal<coordinate_0, boost::mpl::vector_c<int,-1,1> > ));
    
    BOOST_MPL_ASSERT((mpl::equal<se_type::get_nth_coordinate< mpl::int_<2> >::type, boost::mpl::vector_c<int,1,-1> > ));
    BOOST_MPL_ASSERT((mpl::equal<se_type::get_nth_coordinate< mpl::int_<3> >::type, boost::mpl::vector_c<int,-1,0> > ));
    BOOST_MPL_ASSERT((mpl::equal<se_type::get_nth_coordinate< mpl::int_<4> >::type, boost::mpl::vector_c<int,0,0> > ));
    BOOST_MPL_ASSERT_NOT((mpl::equal<se_type::get_nth_coordinate< mpl::int_<5> >::type, boost::mpl::vector_c<int,0,0> > ));
    BOOST_MPL_ASSERT((mpl::equal<se_type::get_nth_coordinate< mpl::int_<7> >::type, boost::mpl::vector_c<int,0,1> > ));

    BOOST_MPL_ASSERT_RELATION( mpl::size< se_type::get_nth_coordinate< mpl::int_<7> >::type >::type::value, ==, 2 );
    BOOST_MPL_ASSERT_RELATION( mpl::size< se_type::get_nth_coordinate< mpl::int_<7> >::type >::type::value, >, 0 );
    //BOOST_MPL_ASSERT_RELATION( mpl::size< se_type::get_nth_coordinate< mpl::int_<7> >::type >::type::value, ==, 7 );



    //BOOST_MPL_ASSERT((mpl::equal<se_type::extract_all_nth_dimension_vector< mpl::int_<0> >::type, boost::mpl::vector_c<int,1,0,1,-1,0,1,-1,0,1>));


#if 0
    BOOST_MPL_ASSERT( (mpl::equal<mpl::range_c<int, 0, se_type::size_coordinate::value >, mpl::vector_c<int, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 > > ));


    typedef mpl::zip_view< mpl::vector<se_type::se_coordinate_type::second, mpl::range_c<int, 0, se_type::size_coordinate::value > > > m_zip_view;

    typedef mpl::transform_view<
      m_zip_view,
      mpl::unpack_args< mpl::_1 >
    >::type m_simple_test;

    BOOST_MPL_ASSERT( (mpl::equal<m_simple_test, se_type::se_coordinate_type::second > ));




    typedef mpl::filter_view<
      m_zip_view,
      mpl::unpack_args< mpl::equal_to< mpl::modulus< mpl::plus<mpl::_2, mpl::int_<1> >, se_type::se_coordinate_type::first > , mpl::int_<0> > >
    >::type m_filter_view;

    BOOST_MPL_ASSERT_RELATION(mpl::size<m_filter_view>::value, ==, 9);


    typedef mpl::transform_view<
      m_filter_view,
      mpl::unpack_args< mpl::_2 >
    > m_simple_test2;

    BOOST_MPL_ASSERT( (mpl::equal<m_simple_test2, mpl::vector_c<int, 1,3,5,7,9,11,13,15,17 > > ));


    typedef 
      mpl::transform_view< 
        m_filter_view, 
        mpl::unpack_args<mpl::_1> 
      >::type vector_dim_1;

    BOOST_MPL_ASSERT((mpl::equal<vector_dim_1::type, boost::mpl::vector_c<int,-1,-1,-1,0,0,0,1,1,1> > ));


    typedef mpl::advance<mpl::begin<se_coordinate_type__::second>::type, mpl::times<se_coordinate_type__::first, mpl::int_<0> >::type >::type begin_iterator;
    typedef mpl::advance<mpl::begin<se_coordinate_type__::second>::type, mpl::times<se_coordinate_type__::first, mpl::plus<mpl::int_<0>, mpl::int_<1> >::type >::type >::type end_iterator;
#endif




    BOOST_MPL_ASSERT((mpl::equal<se_type::extract_all_nth_dimension_vector<mpl::int_<1> >::type, boost::mpl::vector_c<int,-1,-1,-1,0,0,0,1,1,1> > ));
    BOOST_MPL_ASSERT_NOT((mpl::equal<se_type::extract_all_nth_dimension_vector<mpl::int_<1> >::type, boost::mpl::vector_c<int,-1,-1,-1,0,0,0,1,1,2> > ));


    BOOST_MPL_ASSERT( (mpl::equal_to<se_type::extract_min_max_extension_on_dimension<mpl::int_<1> >::min_value_t, mpl::int_<-1> > ));
    BOOST_MPL_ASSERT( (mpl::equal_to<se_type::extract_min_max_extension_on_dimension<mpl::int_<1> >::max_value_t, mpl::int_<1> > ));



    //BOOST_MPL_ASSERT((mpl::equal<se_type::template shift_vector<boost::mpl::vector_c<int,-1,2> >::type, vector_to_have));

    //boost::mpl::vector_c<int, -1,-1, 0,-1, 1,-1,  -1,0, 0,0, 1,0, -1,1, 0,1, 1,1 > 

    // point extraction
    BOOST_MPL_ASSERT((mpl::equal<se_type::extract_nth_point<mpl::int_<0> >::type, boost::mpl::vector_c<int, -1,-1> >));
    BOOST_MPL_ASSERT((mpl::equal<se_type::extract_nth_point<mpl::int_<2> >::type, boost::mpl::vector_c<int, 1,-1> >));
    BOOST_MPL_ASSERT((mpl::equal<se_type::extract_nth_point<mpl::int_<5> >::type, boost::mpl::vector_c<int, 1,0> >));
    BOOST_MPL_ASSERT((mpl::equal<se_type::extract_nth_point<mpl::int_<8> >::type, boost::mpl::vector_c<int, 1,1> >));


    // Shifting
    typedef se_type::extract_nth_point<mpl::int_<8> >::type point_from_vector; /*boost::mpl::vector_c<int, 1,1>*/
    typedef boost::mpl::vector_c<int, 1,-10> shift_vector;
    typedef boost::mpl::vector_c<int, 1,0> small_shift_vector;
    BOOST_MPL_ASSERT((mpl::equal<se_type::shift_point<point_from_vector, shift_vector >::type, boost::mpl::vector_c<int, 2,-9> >));
    BOOST_MPL_ASSERT_NOT((mpl::equal<se_type::shift_point<point_from_vector, shift_vector >::type, boost::mpl::vector_c<int, 2,-10> >));


    // Shifting for all the vector
    typedef boost::mpl::vector_c<int, 
        0,-11, 
        1,-11, 
        2,-11,
        0,-10, 
        1,-10, 
        2,-10, 
        0,-9, 
        1,-9, 
        2,-9 > vector_to_have;

#if 1
    typedef
      mpl::accumulate<
        mpl::transform_view<
          mpl::range_c<int, 0, se_type::nb_coordinate::value>,
          se_type::shift_point< se_type::extract_nth_point<mpl::_1>, shift_vector >
        >,
        mpl::vector_c<int>,
        mpl::insert_range<mpl::_1, mpl::end<mpl::_1>, mpl::_2> 
      >::type shifted_vector_type2; 

    BOOST_MPL_ASSERT((mpl::equal<shifted_vector_type2, vector_to_have >));
#endif

    typedef 
      mpl::transform_view<
        mpl::range_c<int, 0, se_type::nb_coordinate::value >,
        se_type::shift_point< se_type::extract_nth_point<mpl::_1>, shift_vector >
    >::type transformed_vector;

    
    typedef mpl::at_c<transformed_vector, 0>::type range_0;
    typedef mpl::back_inserter<range_0> insert_back;
    BOOST_MPL_ASSERT((mpl::equal<
      mpl::copy< mpl::vector_c<int>, insert_back >::type,
      range_0>));

#if 1
    typedef mpl::accumulate<
      transformed_vector,
      mpl::vector_c<int>,
      mpl::copy<mpl::_2, mpl::back_inserter<mpl::_1> > >::type shifted_vector_type;

    BOOST_MPL_ASSERT((mpl::equal_to<mpl::size<shifted_vector_type>::type, mpl::size<se_type::se_coordinate_type::second>::type> ));

    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<0> >::type, mpl::int_<0> > ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<1> >::type, mpl::int_<-11> > ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<2> >::type, mpl::int_<1> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<3> >::type, mpl::int_<-11> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<4> >::type, mpl::int_<2> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_type, mpl::int_<5> >::type, mpl::int_<-11> >));
#endif
    BOOST_MPL_ASSERT((mpl::equal<shifted_vector_type, vector_to_have >));


    typedef se_type::shift_vector<shift_vector>::type shifted_vector_se;
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::size<shifted_vector_se>::type, mpl::size<se_type::se_coordinate_type::second>::type> ));

    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<0> >::type, mpl::int_<0> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<1> >::type, mpl::int_<-11> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<2> >::type, mpl::int_<1> > ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<3> >::type, mpl::int_<-11> >));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<4> >::type, mpl::int_<2> > ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::at<shifted_vector_se, mpl::int_<5> >::type, mpl::int_<-11> >));

    BOOST_MPL_ASSERT((mpl::equal<shifted_vector_se, vector_to_have >));
    

    
    typedef mpl::lambda<se_type::extract_nth_point<mpl::_1> >::type l_exp;
    typedef mpl::transform_view<
        mpl::range_c<int, 0, 2>,
        l_exp
      >::type shifted_coordinates_vector_type;
    
    BOOST_MPL_ASSERT(( mpl::equal<mpl::at_c<shifted_coordinates_vector_type, 0>::type,  boost::mpl::vector_c<int, -1,-1> > ));
   
   
   

    typedef mpl::transform_view<
        shifted_coordinates_vector_type,
        se_type::shift_point< mpl::_1 , shift_vector>
      >::type shifted_coordinates_vector_type2;

    BOOST_MPL_ASSERT(( mpl::equal<mpl::at_c<shifted_coordinates_vector_type2, 0>::type,  boost::mpl::vector_c<int, 0,-11> > ));
    BOOST_MPL_ASSERT_NOT(( mpl::equal<mpl::at_c<shifted_coordinates_vector_type2, 0>::type,  boost::mpl::vector_c<int, 0,-12> > ));




    // Quelques tests sur mpl::map
    typedef mpl::map<> map_1_t;
    
    typedef mpl::insert<
              map_1_t,  
              mpl::pair<
                //mpl::at<shifted_coordinates_vector_type2, mpl::int_<0> >::type, 
                 mpl::vector_c<int, 0,-11>, mpl::int_<0>
              > 
            >::type map_2_t;
    BOOST_MPL_ASSERT((boost::is_same< mpl::vector_c<int, 0,-11>::type, mpl::vector_c<int, 0,-11>::type >));
    BOOST_MPL_ASSERT_NOT((boost::is_same< mpl::vector_c<int, 0,-11>::type, mpl::vector_c<int, 0,-12>::type >));
    BOOST_MPL_ASSERT_NOT(( mpl::empty<map_2_t> ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::size<map_2_t>::type, mpl::int_<1> >));
    BOOST_MPL_ASSERT_NOT((mpl::equal_to<mpl::size<map_2_t>::type, mpl::int_<2> >));
    
    
    BOOST_MPL_ASSERT((mpl::equal<mpl::front<map_2_t>::type::first, mpl::vector_c<int, 0,-11> > ));
    BOOST_MPL_ASSERT_NOT((mpl::equal<mpl::front<map_2_t>::type::first, mpl::vector_c<int, 0,-12> > ));
    BOOST_MPL_ASSERT_NOT((boost::is_same<mpl::front<map_2_t>::type::first, mpl::vector_c<int, 0,-12> > ));
    BOOST_MPL_ASSERT((mpl::equal_to<mpl::front<map_2_t>::type::second, mpl::int_<0> > ));
    BOOST_MPL_ASSERT_NOT((mpl::equal_to<mpl::front<map_2_t>::type::second, mpl::int_<2> > ));
    
    
    typedef mpl::map<
      mpl::pair<
        mpl::vector_c<int, 0,-11>, mpl::int_<0>
      >
    > my_fucking_map_type;
    
    BOOST_MPL_ASSERT((boost::is_same<mpl::front<my_fucking_map_type>::type::first, mpl::vector_c<int, 0,-11> > ));
    BOOST_MPL_ASSERT_NOT((boost::is_same<mpl::front<my_fucking_map_type>::type::first, mpl::vector_c<int, 0,-2> > ));

    
    
    //BOOST_MPL_ASSERT(( mpl::has_key<map_2_t, boost::mpl::vector_c<int, 0,-11> > ));
 
#if 0 
#if 0
    typedef 
      mpl::copy<
        mpl::range_c<int, 0, 1 >,
        mpl::inserter<
          mpl::map<>, 
          mpl::insert<
            mpl::quote2<
              mpl::_1, 
              mpl::pair<
                mpl::at<shifted_coordinates_vector_type2, mpl::_2>, 
                mpl::_2 
              >
            >
          > 
        >
      >::type map_shifted_vector_type;
#endif



#endif




    // LE contenu de ce qui suit est repris dans se_type::s_cover_uncover
      
    
    typedef mpl::copy<
      //mpl::range_c<int, 0, /*mpl::size<se_type::se_coordinate_type::second>::type::value*/se_type::nb_coordinate::value>,
      mpl::range_c<int, 0, 9>,
        mpl::inserter<
          mpl::vector<>,
          mpl::push_back<
            mpl::_1,
            mpl::pair<
              mpl::_2, 
              se_type::extract_nth_point<mpl::_2>
            >
          >
        >
      >::type paired_vector; 
      
    BOOST_MPL_ASSERT(( mpl::equal_to<mpl::front<paired_vector>::type::first, mpl::int_<0> > ));
    BOOST_MPL_ASSERT(( mpl::equal<mpl::front<paired_vector>::type::second, mpl::vector_c<int, -1,-1> > ));



    typedef mpl::copy<
        mpl::range_c<int, 0, 9>,
        mpl::inserter<
          mpl::vector<>,
          mpl::push_back<
            mpl::_1,
            mpl::pair<
              mpl::_2, 
              se_type::shift_point<se_type::extract_nth_point<mpl::_2>, small_shift_vector>
            >
          >
        >
      >::type paired_vector_shifted;
    
    typedef mpl::vector_c<int, 0,-1> vector_to_find;


    // test
    typedef mpl::front<paired_vector_shifted>::type result_shifting;
    typedef result_shifting::first                  result_shifting_position;
    typedef result_shifting::second                 result_shifting_translated;
    BOOST_MPL_ASSERT(( mpl::equal_to<result_shifting_position, mpl::int_<0> > ));
    BOOST_MPL_ASSERT(( mpl::equal<result_shifting_translated,  vector_to_find> ));
    BOOST_MPL_ASSERT(( mpl::equal_to<mpl::size<result_shifting_translated>::type, mpl::int_<2> > ));
      

    typedef mpl::lambda<s_vector_equal<mpl::_1, vector_to_find > >::type m_lambda;


    typedef mpl::find_if<paired_vector_shifted, m_lambda >::type iter_find_shifted;
    BOOST_MPL_ASSERT_RELATION( iter_find_shifted::pos::value, ==, 0 );
    BOOST_MPL_ASSERT(( mpl::equal_to< mpl::deref<iter_find_shifted>::type::first, mpl::int_<0> > ));


    typedef paired_vector_shifted VectorShifted;
    typedef paired_vector         VectorReference;
    typedef mpl::int_<0>          VectorIndex;

    typedef mpl::find_if<
      VectorShifted,
      s_vector_equal<mpl::_1, mpl::at<VectorReference, VectorIndex>::type::second>
    >::type iter_type_void;
    
    BOOST_MPL_ASSERT(( boost::is_same< iter_type_void, mpl::end<VectorShifted>::type > ));

    typedef mpl::find_if<
      VectorReference,
      s_vector_equal<mpl::_1, mpl::at<VectorShifted, VectorIndex>::type::second>
    >::type iter_type;

    typedef  
      mpl::eval_if<
        mpl::not_<boost::is_same< iter_type, mpl::end<VectorReference>::type > >::type,
        mpl::pair<
          mpl::deref<iter_type>::type::first,                   // ici l'évaluation ne fonctionne pas correctement si iter_type == end
          mpl::at<VectorReference, VectorIndex>::type::first>, // normalement VectorIndex
        mpl::void_
      >::type type_to_find;

    typedef s_correspondance_helper<mpl::int_<0>, paired_vector_shifted, paired_vector> correspondance_h1;
    BOOST_MPL_ASSERT_NOT((correspondance_h1::is_found));
    BOOST_MPL_ASSERT( (boost::is_same<correspondance_h1::type, mpl::void_ >) );

#if 0
    typedef mpl::transform<
      mpl::range_c<int, 0, 9>, 
      s_correspondance_helper<mpl::_1, paired_vector_shifted, paired_vector> 
    >::type transformed_correspondance;

    typedef 
      mpl::copy_if<
        transformed_correspondance,
        mpl::not_< boost::is_same<mpl::_1, mpl::void_> >,
        mpl::back_inserter< mpl::vector<> >
      >::type correspondance_type;

    BOOST_MPL_ASSERT(( mpl::equal_to<mpl::size< correspondance_type>::type, mpl::int_<0> > ));
#endif


    BOOST_MPL_ASSERT(( mpl::equal_to<mpl::size< se_type::s_cover_uncover<shift_vector>::covered_points>::type, mpl::int_<0> > ));

    typedef se_type::s_cover_uncover<boost::mpl::vector_c<int, 1,0> >::covered_points cover_points;
    BOOST_MPL_ASSERT_NOT(( mpl::equal_to<mpl::size< cover_points>::type, mpl::int_<0> > ));
    
    BOOST_MPL_ASSERT(( mpl::equal_to<mpl::size< cover_points>::type, mpl::int_<6> > ));


    std::cout << "cover_points : size = " << mpl::size< cover_points>::type::value << std::endl;

    std::cout << "cover_points :" << std::endl;
    mpl::for_each<cover_points>(cover_printer());
    
    
    // test transposition par rapport à l'origine
    typedef se_type::transpose_point_origin<boost::mpl::vector_c<int, 1,0> >::type transposed_vector;
    BOOST_MPL_ASSERT(( mpl::equal<transposed_vector, mpl::vector_c<int, -1,0> > ));
    
    
    
  }
};






void register_se_iterators_recovery_test(test_suite*& test)
{
  boost::shared_ptr<se_covering_forward_test> instance( new se_covering_forward_test );
  test->add( BOOST_CLASS_TEST_CASE( &se_covering_forward_test::test_1,  instance ) );
}


