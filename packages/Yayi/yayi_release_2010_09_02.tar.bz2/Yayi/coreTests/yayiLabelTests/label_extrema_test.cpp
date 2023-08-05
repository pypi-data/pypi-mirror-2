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

#include <Yayi/core/yayiLabel/include/yayi_label_extrema_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

using namespace yayi;

void test_label_extrema() {
  BOOST_CHECKPOINT("test_label_extrema");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_lab, im_out_lab;
  image_type* p_im[] = {&im_in, &im_test_lab, &im_out_lab};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "2 2 3 2 "
      "1 1 3 1 "
      "2 3 2 1 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical label image
  {
    static const std::string s = 
      "0 0 0 0 "
      "1 1 0 2 "
      "0 0 0 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_lab, "Error during the input streaming of the image");
  }

  
  yaRC res = label::image_label_minima_t(im_in, se::SESquare2D, im_out_lab);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_lab.pixel(i) == im_test_lab.pixel(i), "Label error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_lab.pixel(i) << " != " << (int)im_test_lab.pixel(i));
  }
  
  
}


void test_label_extrema_on_queue() {
  BOOST_CHECKPOINT("test_label_extrema_on_queue");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_lab;
  image_type* p_im[] = {&im_in, &im_test_lab};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input image
  {
    static const std::string s = 
      "2 2 3 2 "
      "1 1 3 1 "
      "2 3 2 1 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }
  
  
  std::vector<std::pair<yaUINT16, std::vector<offset> > > out_queue;

  // theoretical label image
  {
    static const std::string s = 
      "0 0 0 0 "
      "1 1 0 2 "
      "0 0 0 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_lab, "Error during the input streaming of the image");
  }

  
  yaRC res = label::image_label_minima_into_queue_t(im_in, se::SESquare2D, out_queue);
  BOOST_REQUIRE(res == yaRC_ok);
  
  BOOST_REQUIRE_MESSAGE(out_queue.size() == 2, "Bad size for the output : " << out_queue.size() << " != 2");
  BOOST_CHECK(out_queue[0].second.size() == 2);
  BOOST_CHECK(out_queue[0].first == 1);
  BOOST_CHECK(out_queue[1].second.size() == 2);
  BOOST_CHECK(out_queue[1].first == 2);
  
  // check des sorties
  std::map<yaUINT16, int> m;
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) 
  {
    if(im_test_lab.pixel(i) != 0)
    {
      BOOST_CHECK_MESSAGE(im_test_lab.pixel(i) == out_queue[im_test_lab.pixel(i)-1].first, "Label error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\ttest_label_id != result_label_id : " << (int)im_test_lab.pixel(i) << " != " << (int)out_queue[im_test_lab.pixel(i)-1].first);
      BOOST_CHECK_MESSAGE(i == out_queue[im_test_lab.pixel(i)-1].second[m[im_test_lab.pixel(i)]], "Label error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\ttest_offset != result_offset : " << i << " != " << (int)out_queue[im_test_lab.pixel(i)-1].second[m[im_test_lab.pixel(i)]]);
      m[im_test_lab.pixel(i)]++;
    }
  }
  
  
}




void register_label_extrema_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_label_extrema) );
  test->add( BOOST_TEST_CASE(&test_label_extrema_on_queue) );
}
