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

#include "Yayi/core/yayiPixelProcessing/image_constant.hpp"
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include "Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp"

#include <iostream>

using namespace yayi;

class image_unary_interface
{
public:

  typedef Image<yaUINT8> image_t;
  typedef Image<yaF_simple, s_coordinate<3> > image_3f_t;

  image_t im;
  image_3f_t im3D;
  

  void test_create()
  {
    BOOST_CHECKPOINT("image_unary_interface::test_create");

    image_t::coordinate_type coord;

    coord[0] = 10;
    coord[1] = 20;
      
    yaRC res = im.SetSize(coord);
    BOOST_REQUIRE(res == yaRC_ok);


    res = im.AllocateImage();
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Allocate failed with coords : " << coord);

    BOOST_CHECK_MESSAGE(im.Size()[0] == 10, "Bad image size : " << im.Size()[0] << " != " << 10);
    BOOST_CHECK_MESSAGE(im.Size()[1] == 20, "Bad image size : " << im.Size()[1] << " != " << 20);
    BOOST_CHECK(im.IsAllocated());
    
    
    res = im3D.SetSize(c3D(50, 40, 30));
    BOOST_REQUIRE(res == yaRC_ok);

    res = im3D.AllocateImage();
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Allocate failed with coords : " << coord);

    BOOST_CHECK_MESSAGE(im3D.Size()[0] == 50, "Bad image size : " << im3D.Size()[0] << " != " << 50);
    BOOST_CHECK_MESSAGE(im3D.Size()[1] == 40, "Bad image size : " << im3D.Size()[1] << " != " << 40);
    BOOST_CHECK_MESSAGE(im3D.Size()[2] == 30, "Bad image size : " << im3D.Size()[2] << " != " << 30);
    BOOST_CHECK(im3D.IsAllocated());
    
   
  }
  
  void test_set_constant()
  {
    BOOST_CHECKPOINT("image_unary_interface::test_set_constant");
    
    int i = 0;
    for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
      *it = i;
      BOOST_CHECK_MESSAGE(im.pixel(i) == i, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
    }
    BOOST_CHECK_MESSAGE(i == 200, "The number of points " << i << " is different from the number of pixels in the image (200)");
      
    yaRC res = constant(&im, (yaUINT8)11);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of constant shows an error : " << "\n\t\"" << res << "\"");

    i = 0;
    for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_MESSAGE(im.pixel(i) == 11, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
    }
    BOOST_CHECK_MESSAGE(i == 200, "The number of points " << i << " is different from the number of pixels in the image (200)");
      
      
  }

  void test_set_constant2()
  {
    BOOST_CHECKPOINT("image_unary_interface::test_set_constant2");
    
    int i = 0;
    for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
      *it = image_3f_t::pixel_type(i);
      BOOST_CHECK_MESSAGE(im3D.pixel(i) == i, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
    }
    BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
      
    yaRC res = constant(&im3D, 0.3f);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of constant shows an error : " << "\n\t\"" << res << "\"");

    i = 0;
    for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
      BOOST_CHECK_MESSAGE(std::abs(im3D.pixel(i) - 0.3f) < 1E-10, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
    }
    BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
      
      
  }
  


  
  
  static void declare_tests(test_suite*& test) {
    boost::shared_ptr<image_unary_interface> instance( new image_unary_interface );
    test->add( BOOST_CLASS_TEST_CASE( &image_unary_interface::test_create,        instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_unary_interface::test_set_constant,  instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_unary_interface::test_set_constant2, instance ) );
  }
};


void register_simple_interface_tests(test_suite*& test)
{
  image_unary_interface::declare_tests(test);
}
