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
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_hit_or_miss_t.hpp>
#include <Yayi/core/yayiImageCore/yayiImageCoreFunctions.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <iostream>
using namespace yayi;
void test_hit_or_miss() 
{

  BOOST_CHECKPOINT("test_hit_or_miss");
  typedef Image<yaUINT8> image_type;
  typedef image_type::coordinate_type coordinate_type;
  
  static const coordinate_type::scalar_coordinate_type coords_fore [] = {0,0, -1,0};
  static const coordinate_type::scalar_coordinate_type coords_back [] = {1,0, 1,-1, 0,-1};
    
  std::vector<coordinate_type> v(coordinate_type::from_table_multiple(coords_fore, coords_fore + sizeof(coords_fore)/sizeof(coords_fore[0])));

  typedef se::s_neighborlist_se<coordinate_type> neigh_t;
  neigh_t se_fore, se_back;

  BOOST_CHECKPOINT("test_hit_or_miss:init");

  BOOST_CHECK(se_fore.set_coordinates(v) == yaRC_ok);
  v = coordinate_type::from_table_multiple(coords_back, coords_back + sizeof(coords_back)/sizeof(coords_back[0]));
  BOOST_CHECK(se_back.set_coordinates(v) == yaRC_ok);
  
  
  image_type im_in, im_test, im_out;
  image_type::coordinate_type coord;
  coord[0] = 5; coord[1] = 5;
  BOOST_REQUIRE(im_in.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_in.AllocateImage() == yaRC_ok, "im_test.AllocateImage() error");

  BOOST_REQUIRE(im_test.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_test.AllocateImage() == yaRC_ok, "imout.AllocateImage() error");

  BOOST_REQUIRE(im_out.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_out.AllocateImage() == yaRC_ok, "imout.AllocateImage() error");
  
  // input image
  {
    static const std::string s = 
      " 1  2  3  4  5 "
      " 6  7  8  8  2 "
      "11 12 13 14 15 "
      "255 254 253 251 251 "
      "128 254 254 125 124";
      
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "0 0 0 0 4 " // the "outside" is considered as being part of the background (which may not be true in all cases)
      "0 0 0 3 0 "
      "0 0 0 0 12 "
      "1 1 2 0 236 "
      "0 0 1 0 0";
      
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }
  
  BOOST_CHECKPOINT("test_hit_or_miss:test");

  yaRC res = llmm::hit_or_miss_soille_image_t(im_in, se_fore, se_back, im_out);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the erosion, details : \n " << res);

  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Erosion error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }

}


void register_hit_or_miss_tests(test_suite*& test) {
  test->add( BOOST_TEST_CASE(&test_hit_or_miss)       );
}
