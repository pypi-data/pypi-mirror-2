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

#include <Yayi/core/yayiDistances/include/morphological_distance_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

using namespace yayi;

void test_distance_morpho() {
  BOOST_CHECKPOINT("test_distance_morpho");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_dist, im_out_dist;
  image_type* p_im[] = {&im_in, &im_test_dist, &im_out_dist};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "1 0 1 2 "
      "0 0 1 8 "
      "0 1 3 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical distance transform
  {
    static const std::string s = 
      "1 0 1 2 "
      "0 0 1 2 "
      "0 1 2 3 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_dist, "Error during the input streaming of the image");
  }
  
  
  yaRC res = distances::distance_from_sets_boundary(im_in, se::SECross2D, im_out_dist);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_dist.pixel(i) == im_test_dist.pixel(i), "Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
  }
 

}



void test_distance_morpho_geodesic() {
  BOOST_CHECKPOINT("test_distance_morpho_geodesic");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_mask, im_test_dist, im_test_dist_cross, im_out_dist;
  image_type* p_im[] = {&im_in, &im_mask, &im_test_dist, &im_test_dist_cross, &im_out_dist};
  image_type::coordinate_type coord;
  coord[0] = 5; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "1 0 1 1 0 "
      "0 0 0 0 0 "
      "0 0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // mask image
  {
    static const std::string s = 
      "1 0 1 0 1 "
      "0 0 1 1 0 "
      "1 1 1 2 1 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mask, "Error during the input streaming of the image");
  }


  // theoretical distance transform for Square2D
  {
    static const std::string s = 
      "1 0 1 0 3 "
      "0 0 2 2 0 "
      "4 3 3 3 3 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_dist, "Error during the input streaming of the image");
  }

  // theoretical distance transform for Cross2D
  {
    static const std::string s = 
      "1 0 1 0 0 "
      "0 0 2 3 0 "
      "5 4 3 4 5 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_dist_cross, "Error during the input streaming of the image");
  }  
  
  yaRC res = distances::geodesic_distance_from_sets_boundary(im_mask, im_in, se::SESquare2D, im_out_dist);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_dist.pixel(i) == im_test_dist.pixel(i), "Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
  }

  res = distances::geodesic_distance_from_sets_boundary(im_mask, im_in, se::SECross2D, im_out_dist);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_dist.pixel(i) == im_test_dist_cross.pixel(i), "Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist_cross.pixel(i));
  }
  
  // mask image
  {
    static const std::string s = 
      "0 1 1 1 1 "
      "0 1 1 1 1 "
      "1 1 1 1 1 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mask, "Error during the input streaming of the image");
  }

  // theoretical distance transform for Square2D
  {
    static const std::string s = 
      "0 2 1 1 2 "
      "0 2 2 2 2 "
      "3 3 3 3 3 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_dist, "Error during the input streaming of the image");
  }
  
  res = distances::geodesic_distance_from_sets_boundary(im_mask, im_in, se::SESquare2D, im_out_dist);
  BOOST_REQUIRE(res == yaRC_ok);  

  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_dist.pixel(i) == im_test_dist.pixel(i), "Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
  }

}





void register_morpho_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_distance_morpho) );
  test->add( BOOST_TEST_CASE(&test_distance_morpho_geodesic) );

}
