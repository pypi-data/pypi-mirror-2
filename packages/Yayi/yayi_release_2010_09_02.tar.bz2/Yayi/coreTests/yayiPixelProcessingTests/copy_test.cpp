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
#include "Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp"  


void test_copy_no_optim()
{
  using namespace yayi;
  BOOST_CHECKPOINT("test_copy_no_optim");
  typedef Image<yaF_simple, s_coordinate<3> > image_3f_t;  
  typedef Image<yaF_double, s_coordinate<3> > image_3d_t;
  
  image_3f_t im3D;
  BOOST_REQUIRE(im3D.SetSize(c3D(5, 6, 7)) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im3D.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c3D(50, 40, 30));

  
  image_3d_t im3Dd; 
  BOOST_REQUIRE(im3Dd.set_same(im3D) == yaRC_ok);
  
  
  int i = 0;
  for(image_3d_t::iterator it = im3Dd.begin_block(), ite = im3Dd.end_block(); it != ite; ++it, i++) {
    *it = i / double(5 * 6 * 7);
    BOOST_CHECK_CLOSE(im3Dd.pixel(i), i / double(5 * 6 * 7), 1E-4);
  }    
  BOOST_CHECK_MESSAGE(i == 5 * 6 * 7, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");     
  
  // from the biggest to the smallest
  BOOST_CHECKPOINT("test_copy_no_optim: copy");
  yaRC res = copy_image_t(im3Dd, im3D);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the copy : " << res);
  
  BOOST_CHECKPOINT("test_copy_no_optim: check");
  i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_CLOSE(im3D.pixel(i), static_cast<float>(i / float(5 * 6 * 7)), 1E-4);
  }
  BOOST_CHECK_MESSAGE(i == 5 * 6 * 7, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");     
}

void test_copy_optim()
{
  using namespace yayi;
  BOOST_CHECKPOINT("test_copy_optim");
  typedef Image<yaF_simple, s_coordinate<3> > image_3f_t;  
    
  image_3f_t im3D;
  BOOST_REQUIRE(im3D.SetSize(c3D(5, 6, 7)) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im3D.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c3D(50, 40, 30));

  
  image_3f_t im3D_2; 
  BOOST_REQUIRE(im3D_2.set_same(im3D) == yaRC_ok);
  
  
  int i = 0;
  for(image_3f_t::iterator it = im3D_2.begin_block(), ite = im3D_2.end_block(); it != ite; ++it, i++) {
    *it = i / float(5 * 6 * 7);
    BOOST_CHECK_CLOSE(im3D_2.pixel(i), i / float(5 * 6 * 7), 1E-4);
  }    
  BOOST_CHECK_MESSAGE(i == 5 * 6 * 7, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");     
  
  // from the biggest to the smallest
  BOOST_CHECKPOINT("test_copy_optim: copy");
  yaRC res = copy_image_t(im3D_2, im3D);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the copy : " << res);
  
  BOOST_CHECKPOINT("test_copy_optim: check");
  i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_CLOSE(im3D.pixel(i), i / float(5 * 6 * 7), 1E-4);
  }
  BOOST_CHECK_MESSAGE(i == 5 * 6 * 7, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");     
}

void test_copy_windowed()
{
  using namespace yayi;
  BOOST_CHECKPOINT("test_copy_windowed");
  typedef Image<yaF_simple, s_coordinate<3> > image_3f_t;  
    
  image_3f_t im3D;
  BOOST_REQUIRE(im3D.SetSize(c3D(50, 101, 42)) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im3D.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c3D(50, 101, 42));

  typedef Image<yaF_simple> image_2f_t;
  image_2f_t im2D; 
  BOOST_REQUIRE(im2D.SetSize(c2D(50, 101)) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im2D.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c2D(50, 101));

  
  
  int i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    *it = i / float(50 * 101 * 42);
    BOOST_CHECK_CLOSE(im3D.pixel(i), i / float(50 * 101 * 42), 1E-4);
  }    
  BOOST_CHECK_MESSAGE(i == 50 * 101 * 42, "The number of points " << i << " is different from the number of pixels in the image (50 * 101 * 42)");     
  
  // from the biggest to the smallest
  BOOST_CHECKPOINT("test_copy_windowed: copy");
  yaRC res = copy_image_windowed_t(im3D, s_hyper_rectangle<3>(c3D(50, 101, 20), c3D(50, 101, 1)), s_hyper_rectangle<2>(c2D(0, 0), c2D(50, 101)), im2D);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the copy : " << res);
  
  
  for(unsigned int current_slice = 0; current_slice < 42; current_slice++)
  {

    res = copy_image_windowed_t(im3D, s_hyper_rectangle<3>(c3D(0, 0, current_slice), c3D(50, 101, 1)), s_hyper_rectangle<2>(c2D(0, 0), c2D(50, 101)), im2D);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the copy : " << res);


    // there is a bug anyway
    BOOST_CHECKPOINT("test_copy_windowed: check");
    i = 0;
    for(image_2f_t::iterator it = im2D.begin_block(), ite = im2D.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_CLOSE(im2D.pixel(i), (i + 50 * 101 * current_slice) / float(50 * 101 * 42), 1E-4);
    }
    BOOST_CHECK_MESSAGE(i == 50 * 101, "The number of points " << i << " is different from the number of pixels in the image (50 * 101)");     
  }
}


void register_copy_tests(test_suite*& test) {
  test->add( BOOST_TEST_CASE( &test_copy_no_optim ) );
  test->add( BOOST_TEST_CASE( &test_copy_optim ) );
  test->add( BOOST_TEST_CASE( &test_copy_windowed ) );
}
