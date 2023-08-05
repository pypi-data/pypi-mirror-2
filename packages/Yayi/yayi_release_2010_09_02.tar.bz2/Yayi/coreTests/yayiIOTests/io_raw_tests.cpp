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



#include "Yayi/core/yayiIO/include/yayi_IO.hpp"
#include "Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp"

void WriteRAWTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test raw write");	
  
  typedef Image<yaUINT8> image_type;
  image_type im;
  
  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  
  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i) = i;
  }
  
  yaRC ret = yayi::IO::writeRAW("test.raw", &im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeRAW error " << ret);

}

void ReadRAWTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test raw read");	
  
  
  IImage *im = 0;
  yaRC ret = yayi::IO::readRAW("test.raw", c2D(10, 20), yayi::type(yayi::type::c_scalar, yayi::type::s_ui8), im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "readRAW error \"" << ret << "\"");
  
  BOOST_REQUIRE(im != 0);
  
  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension");

  typedef Image<yaUINT8> image_type;
  image_type *im_t = dynamic_cast<image_type*>(im);
  

  BOOST_CHECK_MESSAGE(im_t != 0, "cast error");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_CHECK_MESSAGE(im_t->pixel(i) == i, "pixel bad value");
  }
  
  
  delete im;
  
}

void register_io_raw_test(test_suite*& test) {
  test->add( BOOST_TEST_CASE( &WriteRAWTest       ));
  test->add( BOOST_TEST_CASE( &ReadRAWTest        ));
}

