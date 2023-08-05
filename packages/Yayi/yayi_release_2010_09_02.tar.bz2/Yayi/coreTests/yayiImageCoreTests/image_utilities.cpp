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
#include "Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp"
#include "Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp"

#include <iostream>
#include <boost/math/special_functions/modf.hpp>

using namespace yayi;


void test_image_same_type() {
  BOOST_CHECKPOINT("test_image_same_type");	
  Image<yaINT16> im, im2;
  Image<yaUINT8> im3, im4;
  
  BOOST_CHECK(are_images_same_type(im, im2));
  BOOST_CHECK(are_images_same_type(im3, im4));
  BOOST_CHECK(!are_images_same_type(im, im3));

  
}

void test_image_same() {
  BOOST_CHECKPOINT("test_image_same");
  Image<yaINT16> im, im2;
  Image<yaUINT8> im3, im4;
  BOOST_CHECK(!are_images_same(im, im2));
  BOOST_CHECK(!are_images_same(im3, im4));
  BOOST_CHECK(are_images_same(im3, im3));
}


void test_offset_to_coordinate() {
  BOOST_CHECKPOINT("test_offset_to_coordinate");
  typedef Image<yaINT16, s_coordinate<2> > image_t;
  typedef image_t::coordinate_type coord_t;
  
  
  const coord_t size = c2D(10,10);
  const offset center = 10 * 3 + 3;

  
  const coord_t center_coord = from_offset_to_coordinate(size, center);
  BOOST_REQUIRE(center_coord == c2D(3, 3));
  
  BOOST_CHECK_MESSAGE(from_offset_to_coordinate(c2D(3, 3), 0) == c2D(0,0), "Error on the first point");
  
  // Raffi error: from_offset_to_coordinate can only run on the positive half-space. 
  #if 0
  offset delta = -9;
  BOOST_CHECK_MESSAGE(from_offset_to_coordinate(size, delta) == c2D(1, -1), "The shift is uncorrect : " << from_offset_to_coordinate(size, delta) << " != " << c2D(1, -1));
  BOOST_CHECK_MESSAGE(center_coord + from_offset_to_coordinate(size, delta) == c2D(4, 2), "The shift is uncorrect : " << center_coord + from_offset_to_coordinate(size, delta) << " != " << c2D(4, 2));
  
  BOOST_CHECK_MESSAGE(
    is_point_inside(size, center_coord + from_offset_to_coordinate(size, delta)), 
    "The point is incorrectly outside the image : " 
      << center_coord + from_offset_to_coordinate(size, delta) 
      << " should be inside (" 
      << c2D(4, 2)
      << ")");
  
  delta = -19;
  BOOST_CHECK_MESSAGE(from_offset_to_coordinate(size, delta) == c2D(1, -2), "The shift is uncorrect : " << from_offset_to_coordinate(size, delta) << " != " << c2D(1, -2));

  delta = -28;
  BOOST_CHECK_MESSAGE(from_offset_to_coordinate(size, delta) == c2D(2, -3), "The shift is uncorrect : " << from_offset_to_coordinate(size, delta) << " != " << c2D(2, -3));
  
  
  
  typedef Image<yaINT16, s_coordinate<4> > image_t4;
  typedef image_t4::coordinate_type coord_t4;
  
  const coord_t4 size4 = c4D(11, 26, 17, 5), pos = c4D(1, -1, 5, 4);
  //const offset center4 = 11 * 3 + 3;
  delta = 1 + (-1 + (5 + 4*17) * 26) * 11; // position : 1, -1, 5, 4
  
  BOOST_CHECK(delta == from_coordinate_to_offset(size4, pos));
  BOOST_CHECK_MESSAGE(from_offset_to_coordinate(size4, delta) == pos, "The shift is uncorrect : " << from_offset_to_coordinate_test(size4, delta) << " != " << pos);
  
  #endif
  
  
  
}

void test_last_dimension() {
  BOOST_CHECK(get_last_dimension(c2D(5,5)) == 2);
  BOOST_CHECK(get_last_dimension(c4D(5,5, 6,0)) == 3);
}


void register_image_utility_test(test_suite*& test) {
  test->add( BOOST_TEST_CASE( test_image_same_type ) );
  test->add( BOOST_TEST_CASE( test_image_same ) );
  test->add( BOOST_TEST_CASE( test_offset_to_coordinate ) );
  test->add( BOOST_TEST_CASE( test_last_dimension ) );
  
}


