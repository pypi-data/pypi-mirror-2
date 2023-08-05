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
#include <Yayi/core/yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <Yayi/core/yayiIO/include/yayi_IO.hpp>
#include <Yayi/core/yayiImageCore/yayiImageCoreFunctions.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <Yayi/core/yayiPixelProcessing/image_channels_process.hpp>
#include <iostream>
#include <Yayi/core/yayiCommon/include/common_time.hpp>



// for data paths
#include <Yayi/coreTests/yayiCommonCoreTests/data_path_for_tests.hpp>

using namespace yayi;

struct fixture {
  IImage *im, *imtemp, *imout;
  fixture() : im(0), imtemp(0), imout(0) {}
  ~fixture() {
    delete im;
    delete imtemp;
    delete imout;
  }
};

void test_erosion_interface()
{
  fixture fix_;

  
  std::string im_file_name(get_data_from_data_path("release-grosse bouche.jpg"));
  BOOST_TEST_MESSAGE("Reading the image " + im_file_name);
  
  BOOST_REQUIRE(yayi::IO::readJPG(im_file_name, fix_.im) == yaRC_ok);
  fix_.imtemp = GetSameImage(fix_.im, type_scalar_uint8);
  BOOST_REQUIRE(fix_.imtemp != 0);
  fix_.imout = GetSameImage(fix_.imtemp);
  BOOST_REQUIRE(fix_.imout != 0);
  
  yaRC res(yaRC_ok);
  
  res = copy_one_channel(fix_.im, 0, fix_.imtemp);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, 
    "An errror occured during the extraction of the first channel. Details follows: \n" << res << "\nInput image " << fix_.im->Description() << "\nOutput image " << fix_.imtemp->Description() << "\n");

  #define NB_LOOP 5

  yayi::time::s_time_elapsed time_e;
  for(int i = 0; i < NB_LOOP; i++)
  {
    res = llmm::erosion(fix_.imtemp, &se::SESquare2D, fix_.imout);
    BOOST_CHECK_MESSAGE(res == yaRC_ok, "An errror occured during the erosion. Details follows: \n" << res);
  }
  
  std::cout << "Erosion total microseconds = " << time_e.total_microseconds()/NB_LOOP << std::endl;

  yayi::time::s_time_elapsed time_e2;
  for(int i = 0; i < NB_LOOP; i++)
  {
    res = llmm::erode_image_t(dynamic_cast< Image<yaUINT8> const& >(*fix_.imtemp), se::SESquare2D, dynamic_cast< Image<yaUINT8> & >(*fix_.imout));
    BOOST_CHECK_MESSAGE(res == yaRC_ok, "An errror occured during the erosion. Details follows: \n" << res);
  }
  
  std::cout << "Erosion total microseconds (template) = " << time_e2.total_microseconds()/NB_LOOP << std::endl;

}

void register_simple_operators_interface_tests(test_suite*& test) {
  test->add( BOOST_TEST_CASE(&test_erosion_interface)       );
}

