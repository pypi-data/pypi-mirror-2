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
#include <Yayi/core/yayiSegmentation/include/isotropic_watershed_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

using namespace yayi;

void test_watershed_seeded() {
  BOOST_CHECKPOINT("test_watershed_seeded");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_labels, im_test_label, im_out_label;
  image_type* p_im[] = {&im_in, &im_labels, &im_test_label, &im_out_label};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 3 1 "
      "2 2 4 1 "
      "2 2 3 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical residu image
  {
    static const std::string s = 
      "0 0 0 0 "
      "0 1 0 2 "
      "0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_labels, "Error during the input streaming of the image");
  }

  // theoretical distance image
  {
    static const std::string s = 
      "1 1 0 2 "
      "1 1 0 2 "
      "1 1 0 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_label, "Error during the input streaming of the image");
  }
  
  yaRC res = segmentation::isotropic_seeded_watershed_t(im_in, im_labels, se::SESquare2D, im_out_label);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_label.pixel(i) == im_test_label.pixel(i), "Watershed error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_label.pixel(i) << " != " << (int)im_test_label.pixel(i));
  }

}


void register_watershed_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_watershed_seeded) );

}
