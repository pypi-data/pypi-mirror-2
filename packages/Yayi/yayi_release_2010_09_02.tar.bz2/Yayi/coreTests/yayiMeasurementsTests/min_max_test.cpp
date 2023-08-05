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
#include <Yayi/core/yayiMeasurements/measurements_min_max.hpp>
#include <Yayi/core/yayiMeasurements/include/measurements_min_max_t.hpp>

void test_min_max_simple() {
  using namespace yayi;
  BOOST_CHECKPOINT("test_min_max_simple");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in;
  image_type* p_im[] = {&im_in};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 5 2 "
      "1 1 3 2 "
      "1 3 10 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }


  
  variant out;
  yaRC res = measurements::image_meas_min_max_t(im_in, out);
  BOOST_REQUIRE(res == yaRC_ok);
  std::pair<image_type::pixel_type, image_type::pixel_type> v = out;
  
  BOOST_CHECK_MESSAGE(v.first == 1, "Bad output for min: " << v.first << " (result) != 1 (test)");
  BOOST_CHECK_MESSAGE(v.second == 10, "Bad output for max: " << v.second << " (result) != 10 (test)");
  
}


void register_min_max_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_min_max_simple) );
}
