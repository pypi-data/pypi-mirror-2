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
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <Yayi/core/yayiCommon/common_coordinates_operations_t.hpp>

#include <Yayi/core/yayiCommon/include/common_coordinates_mpl_utils_t.hpp>




void test_construction()
{
  BOOST_CHECKPOINT("test_construction");	
  typedef yayi::s_coordinate<2> coordinate_type;

  coordinate_type::scalar_coordinate_type s1[] = {3,4}, s2[] = {3,4}, s3[] = {5,6};

  coordinate_type 
    coord1(coordinate_type::from_table(s1)), 
    coord2(coordinate_type::from_table(s2)), 
    coord3(coordinate_type::from_table(s3)), 
    coord4(3);

  BOOST_CHECK(coord1 == coord2);
  BOOST_CHECK(coord2 == coord1);
  BOOST_CHECK(coord3 != coord1);
  BOOST_CHECK(coord1 != coord3);
  BOOST_CHECK(coord2 != coord3);
  BOOST_CHECK(coord3 != coord2);

  coord1[1] = 3;
  BOOST_CHECK(coord1 == coord4);
  BOOST_CHECK_MESSAGE(coord2 != coord4, 
    "Error comparison for different coordinates, the contents are \n\tleft" << coord2 << " initiliazed from {3,4}\n\t"
    "right " << coord4 << "  initiliazed from (3)");

  BOOST_CHECK(total_number_of_points(coord1) == 9);
  BOOST_CHECK(total_number_of_points(coord3) == 30);

}



void test_construction_mpl()
{
  typedef yayi::from_mpl_to_coordinate<boost::mpl::vector_c<int, 10, 3, 4> > s_type;
  
  BOOST_CHECK( (boost::is_same<s_type::result_type, yayi::s_coordinate<3> >::value) );
  
  s_type::result_type res = s_type::get();
  BOOST_REQUIRE(res.dimension() == 3);
  BOOST_CHECK(res[0] == 10);
  BOOST_CHECK(res[1] == 3);
  BOOST_CHECK(res[2] == 4);
  BOOST_CHECK(res == s_type::get());

}

void test_from_table_multiple()
{
  BOOST_CHECKPOINT("test_from_table_multiple");	
  typedef yayi::s_coordinate<2> coordinate_type;
  static const coordinate_type::scalar_coordinate_type coords [] = {0,0, 1,0, -1,0, 0,1};

  std::vector<coordinate_type> v(coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
  
  BOOST_REQUIRE_MESSAGE(v.size() == 4, "Vector size = " << v.size() << " != 4");
  
  using yayi::c2D;

  BOOST_CHECK(v[0] == c2D(0,0));
  BOOST_CHECK(v[1] == c2D(1,0));
  BOOST_CHECK(v[2] == c2D(-1,0));
  BOOST_CHECK(v[3] == c2D(0,1));
}

void test_sets_equal()
{
  BOOST_CHECKPOINT("test_sets_equal");	
  typedef yayi::s_coordinate<2> coordinate_type;
  static const coordinate_type::scalar_coordinate_type coords1 [] = {0,0, 1,0, -1,0, 0,1};
  static const coordinate_type::scalar_coordinate_type coords2 [] = {0,1, -1,0, 0,0, 1,0, 0,0};
  static const coordinate_type::scalar_coordinate_type coords3 [] = {0,1, -1,0, 0,0, 1,0, 2,0};

  std::vector<coordinate_type> v1(coordinate_type::from_table_multiple(coords1, coords1 + sizeof(coords1)/sizeof(coords1[0])));
  std::vector<coordinate_type> v2(coordinate_type::from_table_multiple(coords2, coords2 + sizeof(coords2)/sizeof(coords2[0])));
  std::vector<coordinate_type> v3(coordinate_type::from_table_multiple(coords3, coords3 + sizeof(coords3)/sizeof(coords3[0])));
  
  BOOST_CHECK(are_sets_of_points_equal(v1, v1));
  BOOST_CHECK(are_sets_of_points_equal(v2, v2));
  BOOST_CHECK(are_sets_of_points_equal(std::list<coordinate_type>(v1.begin(), v1.end()), std::list<coordinate_type>(v1.begin(), v1.end())));
  BOOST_CHECK(are_sets_of_points_equal(std::list<coordinate_type>(v2.begin(), v2.end()), std::list<coordinate_type>(v2.begin(), v2.end())));

  BOOST_CHECK(are_sets_of_points_equal(v1, v2));
  BOOST_CHECK(are_sets_of_points_equal(v2, v1));
  BOOST_CHECK(are_sets_of_points_equal(std::list<coordinate_type>(v1.begin(), v1.end()), std::list<coordinate_type>(v2.begin(), v2.end())));
  BOOST_CHECK(are_sets_of_points_equal(std::list<coordinate_type>(v2.begin(), v2.end()), std::list<coordinate_type>(v1.begin(), v1.end())));

  BOOST_CHECK(!are_sets_of_points_equal(v1, v3));
  BOOST_CHECK(!are_sets_of_points_equal(v3, v1));
  BOOST_CHECK(!are_sets_of_points_equal(std::list<coordinate_type>(v1.begin(), v1.end()), std::list<coordinate_type>(v3.begin(), v3.end())));
  BOOST_CHECK(!are_sets_of_points_equal(std::list<coordinate_type>(v3.begin(), v3.end()), std::list<coordinate_type>(v1.begin(), v1.end())));
  BOOST_CHECK(!are_sets_of_points_equal(v2, v3));
  BOOST_CHECK(!are_sets_of_points_equal(std::list<coordinate_type>(v2.begin(), v2.end()), std::list<coordinate_type>(v3.begin(), v3.end())));

}

void test_sets_equal_bug()
{
  BOOST_CHECKPOINT("test_sets_equal_bug");	
  // in case the two lists are not of the same size
  typedef yayi::s_coordinate<2> coordinate_type;
  static const coordinate_type::scalar_coordinate_type coords1 [] = {0,1, -1,0, 0,0, 1,0, 2,0};
  static const coordinate_type::scalar_coordinate_type coords2 [] = {0,1, -1,0, 0,0, 2,0};

  std::vector<coordinate_type> v1(coordinate_type::from_table_multiple(coords1, coords1 + sizeof(coords1)/sizeof(coords1[0])));
  std::vector<coordinate_type> v2(coordinate_type::from_table_multiple(coords2, coords2 + sizeof(coords2)/sizeof(coords2[0])));
  
  BOOST_CHECK(!are_sets_of_points_equal(v1, v2));
  BOOST_CHECK(!are_sets_of_points_equal(v2, v1));
  BOOST_CHECK(!are_sets_of_points_equal(std::list<coordinate_type>(v1.begin(), v1.end()), std::list<coordinate_type>(v2.begin(), v2.end())));
  BOOST_CHECK(!are_sets_of_points_equal(std::list<coordinate_type>(v2.begin(), v2.end()), std::list<coordinate_type>(v1.begin(), v1.end())));

}


void test_coordinate_transpose() {
  BOOST_CHECKPOINT("test_coordinate_transpose");
  typedef yayi::s_coordinate<4> coord_t;
  
  const coord_t::scalar_coordinate_type 
    s1[] = { 10, 3, 2, 7}, 
    s2[] = {-10,-3,-2,-7},
    s3[] = {5, 3, 5, 6},
    s4[] = {0, 3, 8, 5};

  coord_t c1 = coord_t::from_table(s1), c2 = coord_t::from_table(s2);
  
  BOOST_CHECK(transpose(c1) == c2);
  BOOST_CHECK_MESSAGE(transpose(c1, coord_t::from_table(s3)) == coord_t::from_table(s4), "Incorrect transposition relative to a center : " << transpose(c1, coord_t::from_table(s3)) << " != " << coord_t::from_table(s4));
  
}

void test_inside()
{
  BOOST_CHECKPOINT("test_inside");
  using yayi::c2D;
  yayi::s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2));
  BOOST_CHECK(is_point_inside(window, c2D(1,1)));
  BOOST_CHECK(is_point_inside(window, c2D(1,2)));
  BOOST_CHECK(!is_point_inside(window, c2D(1,3)));

  BOOST_CHECK(is_point_inside(window, c2D(2,2)));
  BOOST_CHECK(!is_point_inside(window, c2D(3,2)));


}

void test_disjoint()
{
  BOOST_CHECKPOINT("test_disjoint");
  using yayi::c2D;
  using yayi::are_sets_of_points_disjoint;

  typedef yayi::s_coordinate<2> coord_t;
  const coord_t::scalar_coordinate_type 
    s1[] = { 10, 3, -10,-3, 0,0, 5,2}, 
    s2[] = {  9, 4,  -9,-4, 0,1, 5,3},
    s3[] = {  9, 4,  -9,-4, 0,1, 5,2};

  std::vector<coord_t> 
    c1 = coord_t::from_table_multiple(s1, s1 + sizeof(s1)/sizeof(s1[0])), 
    c2 = coord_t::from_table_multiple(s2, s2 + sizeof(s1)/sizeof(s2[0])), 
    c3 = coord_t::from_table_multiple(s3, s3 + sizeof(s1)/sizeof(s3[0]));

  BOOST_CHECK(are_sets_of_points_disjoint(c1, c2));
  BOOST_CHECK(are_sets_of_points_disjoint(c2, c1));
  BOOST_CHECK(!are_sets_of_points_disjoint(c3, c2));
  BOOST_CHECK(!are_sets_of_points_disjoint(c3, c1));

}


void test_sets_transpose()
{
  BOOST_CHECKPOINT("test_sets_transpose");	
  typedef yayi::s_coordinate<2> coordinate_type;
  static const coordinate_type::scalar_coordinate_type coords [] = {0,1, -1,0, 0,0, 1,0, 0,0};

  std::vector<coordinate_type> v1(coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
  std::vector<coordinate_type> v2 = v1;
  
  transpose_set_in_place(v1);
  
  for(unsigned int i = 0; i < v1.size(); i++)
  { 
    BOOST_CHECK(v1[i] == transpose(v2[i]));
  }

}


void test_stream()
{
  typedef yayi::s_coordinate<1> coordinate_type;
  static const coordinate_type::scalar_coordinate_type coords [] = {0, 1, -1};
  std::vector<coordinate_type> v = coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0]));
  BOOST_CHECK(v.size() == 3);
  for(int i = 0; i < 3; i++)
  {
    std::ostringstream o;
    o << v[i];
    BOOST_CHECK_MESSAGE(o.str() == "(" + yayi::int_to_string(v[i][0], 1, ' ') + ")", "'" << o.str() << "' != '(" << v[i][0] << ")'"); //"(x)"
  }
}

void register_coordinate_lifetime_test(test_suite*& test)
{
  test->add( BOOST_TEST_CASE( &test_construction        ) );
  test->add( BOOST_TEST_CASE( &test_construction_mpl    ) );
  test->add( BOOST_TEST_CASE( &test_from_table_multiple ) );
  test->add( BOOST_TEST_CASE( &test_sets_equal          ) );
  test->add( BOOST_TEST_CASE( &test_sets_equal_bug      ) );
  test->add( BOOST_TEST_CASE( &test_sets_transpose      ) );
  test->add( BOOST_TEST_CASE( &test_inside              ) );
  test->add( BOOST_TEST_CASE( &test_coordinate_transpose) );
  test->add( BOOST_TEST_CASE( &test_disjoint            ) );
  test->add( BOOST_TEST_CASE( &test_stream              ) );
}


