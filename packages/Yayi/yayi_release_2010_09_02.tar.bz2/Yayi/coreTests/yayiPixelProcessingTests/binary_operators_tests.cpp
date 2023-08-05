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
#include <Yayi/core/yayiPixelProcessing/image_copy.hpp>
#include <Yayi/core/yayiPixelProcessing/image_arithmetics.hpp>
#include <Yayi/core/yayiPixelProcessing/image_channels_process.hpp>

using namespace yayi;

class image_binary_interface
{
public:

  typedef Image<yaUINT8> image_t;
  typedef Image<yaF_simple, s_coordinate<3> > image_3f_t;

  image_t im, im2;
  image_3f_t im3D, im3D_2;
  
  void test_create()
  {
    BOOST_CHECKPOINT("image_binary_interface::test_create");

    BOOST_REQUIRE(im.SetSize(c2D(10, 20)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c2D(10, 20));

    BOOST_CHECK_MESSAGE(im.Size()[0] == 10, "Bad image size : " << im.Size()[0] << " != " << 10);
    BOOST_CHECK_MESSAGE(im.Size()[1] == 20, "Bad image size : " << im.Size()[1] << " != " << 20);
    BOOST_CHECK(im.IsAllocated());

    BOOST_REQUIRE(im2.SetSize(c2D(10, 20)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im2.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c2D(10, 20));

    BOOST_CHECK_MESSAGE(im2.Size()[0] == 10, "Bad image size : " << im2.Size()[0] << " != " << 10);
    BOOST_CHECK_MESSAGE(im2.Size()[1] == 20, "Bad image size : " << im2.Size()[1] << " != " << 20);
    BOOST_CHECK(im2.IsAllocated());



    BOOST_REQUIRE(im3D.SetSize(c3D(50, 40, 30)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im3D.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c3D(50, 40, 30));

    BOOST_CHECK_MESSAGE(im3D.Size()[0] == 50, "Bad image size : " << im3D.Size()[0] << " != " << 50);
    BOOST_CHECK_MESSAGE(im3D.Size()[1] == 40, "Bad image size : " << im3D.Size()[1] << " != " << 40);
    BOOST_CHECK_MESSAGE(im3D.Size()[2] == 30, "Bad image size : " << im3D.Size()[2] << " != " << 30);
    BOOST_CHECK(im3D.IsAllocated());
    
    BOOST_REQUIRE(im3D_2.SetSize(c3D(50, 40, 30)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im3D_2.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c3D(50, 40, 30));

    BOOST_CHECK_MESSAGE(im3D_2.Size()[0] == 50, "Bad image size : " << im3D_2.Size()[0] << " != " << 50);
    BOOST_CHECK_MESSAGE(im3D_2.Size()[1] == 40, "Bad image size : " << im3D_2.Size()[1] << " != " << 40);
    BOOST_CHECK_MESSAGE(im3D_2.Size()[2] == 30, "Bad image size : " << im3D_2.Size()[2] << " != " << 30);
    BOOST_CHECK(im3D_2.IsAllocated());
  }
  
  void test_multiply_constant()
  {
    BOOST_CHECKPOINT("image_binary_interface::test_multiply_constant");
    
    int i = 0;
    for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
      *it = i % 17;
      BOOST_CHECK_MESSAGE(im.pixel(i) == i % 17, "failure with *it = i at pixel " << i << " : it = " << (int)(*it) << " != " << i % 17);
    }
    BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
    
    BOOST_CHECKPOINT("image_binary_interface::test_set_constant - copy");
    yaRC res = yayi::image_multiply_constant(&im, yaUINT8(255), &im);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

    BOOST_CHECKPOINT("image_binary_interface::test_multiply_constant - check");
    i = 0;
    for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_MESSAGE(im.pixel(i) == static_cast<yaUINT8>((i % 17) * 255), "failure with *it = i at pixel " << i << " : it = " << *it << " != " << (int)static_cast<yaUINT8>(i % 17 % 255));
    }
    BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
  }
  
  void test_copy_channel_into_another()
  {
    BOOST_CHECKPOINT("image_binary_interface::test_copy_channel_into_another");
    typedef Image< pixel8u_3 > image_3c;
    
    image_3c imc;
    
    BOOST_REQUIRE(imc.SetSize(c2D(10, 20)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(imc.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c2D(10, 20));

    
    int i = 0;
    for(image_3c::iterator it = imc.begin_block(), ite = imc.end_block(); it != ite; ++it, i++) {
      *it = pixel8u_3(i % 17, i%11, i%37);
      BOOST_CHECK_MESSAGE(imc.pixel(i)[1] == i % 11, "failure with *it = i at pixel " << i << " : it = " << (int)(*it)[1] << " != " << i % 11);
    }
    BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
    
    BOOST_CHECKPOINT("image_binary_interface::test_copy_channel_into_another - do");
    yaRC res = yayi::copy_one_channel_to_another(&imc, 0,2, &imc);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

    BOOST_CHECKPOINT("image_binary_interface::test_copy_channel_into_another - check");
    i = 0;
    for(image_3c::iterator it = imc.begin_block(), ite = imc.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_MESSAGE(imc.pixel(i)[0] == imc.pixel(i)[2] && imc.pixel(i) == pixel8u_3(i % 17, i%11, i%17) && *it == pixel8u_3(i % 17, i%11, i%17), "failure with *it = i at pixel " << i << " : it = " << *it << " != " << pixel8u_3(i % 17, i%11, i%17));
    }
    BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
      
      
  }
  
  
  void test_set_constant()
  {
    BOOST_CHECKPOINT("image_binary_interface::test_set_constant");
    
    int i = 0;
    for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
      *it = i / float(50*40*30);
      BOOST_CHECK_CLOSE(im3D.pixel(i), static_cast<float>(i / float(50*40*30)), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << (float)(*it) << " != " << i / float(50*40*30));
    }
    BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
    
    BOOST_CHECKPOINT("image_binary_interface::test_set_constant - copy");
    yaRC res = copy(&im3D, &im3D_2);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

    BOOST_CHECKPOINT("image_binary_interface::test_set_constant - check");
    i = 0;
    for(image_3f_t::iterator it = im3D_2.begin_block(), ite = im3D_2.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_CLOSE(im3D_2.pixel(i), i / float(50*40*30), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << *it);
      BOOST_CHECK_CLOSE(*it, i / float(50*40*30), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << *it);
    }
    BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
      
      
  }  

  
  static void declare_tests(test_suite*& test) {
    boost::shared_ptr<image_binary_interface> instance( new image_binary_interface );
    test->add( BOOST_CLASS_TEST_CASE( &image_binary_interface::test_create,        instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_binary_interface::test_set_constant,  instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_binary_interface::test_multiply_constant, instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_binary_interface::test_copy_channel_into_another, instance ) );
  }
};




void register_binary_operators_tests(test_suite*& test) {
  image_binary_interface::declare_tests(test);
}

