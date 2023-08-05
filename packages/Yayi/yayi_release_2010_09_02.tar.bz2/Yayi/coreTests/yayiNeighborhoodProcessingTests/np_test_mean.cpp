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

#include <ios>	
#include <iostream>	
#include <Yayi/core/yayiNeighborhoodProcessing/include/np_local_statistics_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>


void test_mean()
{
  using namespace yayi;
  BOOST_CHECKPOINT("test_mean");
  
  typedef Image<yaF_double> image_type;
  
  image_type im_in, im_out_mean, im_test_mean;
  image_type* p_im[] = {&im_in, &im_out_mean, &im_test_mean};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "1.0 2.0 3.0 1.0 "
      "2.0 2.0 4.0 1.0 "
      "2.0 2.0 3.0 2.0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical image mean
  {
    static const std::string s = 
      "1.75 2.33 2.17 2.25 "
      "1.83 2.33 2.22 2.33 "
      "2.00 2.50 2.33 2.50 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_mean, "Error during the input streaming of the image");
  }

  yaRC res = np::image_local_mean_t(im_in, se::SESquare2D, im_out_mean);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    // "1" here means 1% of the value, which is the accuracy with which I filled the im_test image
    BOOST_CHECK_CLOSE(im_out_mean.pixel(i), im_test_mean.pixel(i), 1);//"Mean error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << im_out_mean.pixel(i) << " != " << im_test_mean.pixel(i));
  }

}


void register_simple_local_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_mean) );

}