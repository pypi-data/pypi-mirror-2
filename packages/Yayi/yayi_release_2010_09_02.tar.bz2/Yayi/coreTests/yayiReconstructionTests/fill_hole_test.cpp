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
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <Yayi/core/yayiReconstruction/include/morphological_fill_holes_t.hpp>

void test_fill_hole() {
  using namespace yayi;
  BOOST_CHECKPOINT("test_fill_hole");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test, im_out;
  image_type* p_im[] = {&im_in, &im_test, &im_out};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 4;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input mask image
  {
    static const std::string s = 
      "1 2 1 0 "
      "1 0 1 0 "
      "2 1 3 0 "
      "0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output test image
  {
    static const std::string s = 
      "1 2 1 0 "
      "1 1 1 0 "
      "2 1 3 0 "
      "0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }


  BOOST_CHECKPOINT("test_fill_hole: fill_holes_image_t");
  yaRC res = reconstructions::fill_holes_image_t(im_in, se::SESquare2D, im_out);
  BOOST_CHECKPOINT("test_fill_hole: ret");
  BOOST_REQUIRE(res == yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Erosion error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}


void register_fill_hole_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_fill_hole) );
}



