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



// test d'appel de fonction, avec test de contenu
void WritePNGTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test png write");	
  
  typedef Image<yaUINT8> image_type;
  typedef Image<yaUINT16> image16_type;
  image_type im;
  image16_type im16;
  
  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  BOOST_REQUIRE(im.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE(im16.SetSize(coord) == yaRC_ok);
  
  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
  BOOST_REQUIRE_MESSAGE(im16.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i) = i;
    im16.pixel(i) = i + 1001;
  }
  
  yaRC ret = yayi::IO::writePNG("test.png", &im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writePNG error " << static_cast<string_type>(ret));
  ret = yayi::IO::writePNG("test16.png", &im16);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writePNG (16bits) error " << static_cast<string_type>(ret));  
}

void ReadPNGTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test png read");	
  
  
  IImage *im = 0, *im16 = 0;
  yaRC ret = yayi::IO::readPNG("test.png", im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "read error " + static_cast<string_type>(ret));
  ret = yayi::IO::readPNG("test16.png", im16);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "read error (16bits) " + static_cast<string_type>(ret));
  
  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");
  BOOST_REQUIRE_MESSAGE(im16->IsAllocated(), "im16 not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension");
  
  coord = im16->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension (16bits)");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension (16bits)");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension (16bits)");

  typedef Image<yaUINT8> image_type;
  typedef Image<yaUINT16> image16_type;
  image_type *im_t = dynamic_cast<image_type*>(im);
  image16_type *im16_t = dynamic_cast<image16_type*>(im16);
  
  BOOST_REQUIRE_MESSAGE(im_t != 0, "cast error");
  BOOST_REQUIRE_MESSAGE(im16_t != 0, "cast error (16 bits)");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_CHECK_MESSAGE(im_t->pixel(i) == i, "pixel bad value");
    BOOST_CHECK_MESSAGE(im16_t->pixel(i) == i + 1001, "pixel bad value (16 bits)");
  }
  
  
  delete im;
  delete im16;

}


void WritePNGTestColor() {
  using namespace yayi;
  BOOST_CHECKPOINT("test png write (color)");	
  
  typedef Image<s_compound_pixel_t<yaUINT8,  mpl::int_<3> > > image_type;
  image_type im;
  
  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  
  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i).a = i % 255;
    im.pixel(i).b = (255-i) % 255;
    im.pixel(i).c = (128+i) % 255;
  }
  
  yaRC ret = yayi::IO::writePNG("test_c.png", &im);
  string_type str = static_cast<string_type>(ret);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeJPG error " << ret);
}


void ReadPNGTestColor() {
  using namespace yayi;
  BOOST_CHECKPOINT("test png read (color)");	
  
  
  IImage *im = 0;
  yaRC ret = yayi::IO::readPNG("test_c.png", im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "read error " + static_cast<string_type>(ret));
  BOOST_CHECKPOINT("test jpg read - 1");
  BOOST_REQUIRE_MESSAGE(im != 0, "im not created");  
  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension");

  typedef Image<s_compound_pixel_t<yaUINT8,  mpl::int_<3> > > image_type;
  image_type *im_t = dynamic_cast<image_type*>(im);
  

  BOOST_REQUIRE_MESSAGE(im_t != 0, "cast error");
  
  int ca(0), cb(0), cc(0), cca(0), ccb(0), ccc(0);
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_CHECK_MESSAGE(im_t->pixel(i).a == (i       % 255),  "pixel bad value (a) : i = " << i << " p = " << (int)im_t->pixel(i).a << " != " << i % 255);
    if(im_t->pixel(i).a != (i % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).a - (i % 255));
      ca += d * d;
      cca++;
    }
    
    
    BOOST_CHECK_MESSAGE(im_t->pixel(i).b == ((255-i) % 255),  "pixel bad value (b) : i = " << i << " p = " << (int)im_t->pixel(i).b << " != " << (255-i)%255);
    if(im_t->pixel(i).b != ((255-i) % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).b - ((255-i) % 255));
      cb += d * d;
      ccb++;
    }

    BOOST_CHECK_MESSAGE(im_t->pixel(i).c == ((128+i) % 255),  "pixel bad value (c) : i = " << i << " p = " << (int)im_t->pixel(i).c << " != " << (128+i)%255);
    if(im_t->pixel(i).c != ((128+i) % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).c - ((128+i) % 255));
      cc += d * d;
      ccc++;
    }
  }
  
  BOOST_CHECK_MESSAGE(cca == 0 || ca == 0 , "The mean quadratic error for component a seems to be too high : " << static_cast<float>(ca)/ (coord[0] * coord[1]) << " > 0");
  BOOST_CHECK_MESSAGE(cca == 0, "The # of biased element for component a seems to be too high : " << static_cast<float>(cca)/(coord[0] * coord[1]) << " > 0");

  BOOST_CHECK_MESSAGE(ccb == 0 || cb == 0 , "The mean quadratic error for component b seems to be too high : " << static_cast<float>(cb)/ (coord[0] * coord[1]) << " > 0");
  BOOST_CHECK_MESSAGE(ccb == 0, "The # of biased element for component b seems to be too high : " << static_cast<float>(ccb)/(coord[0] * coord[1]) << " > 0");

  BOOST_CHECK_MESSAGE(ccc == 0 || cc == 0, "The mean quadratic error for component c seems to be too high : " << static_cast<float>(cc)/ (coord[0] * coord[1]) << " > 0");
  BOOST_CHECK_MESSAGE(ccc == 0, "The # of biased element for component c seems to be too high : " << static_cast<float>(ccc)/(coord[0] * coord[1]) << " > 0");


  //BOOST_CHECK_MESSAGE(ccb == 0 || static_cast<float>(cb)/ccb < 0.01, "The bias for component a seems to be too high : " << static_cast<float>(cb)/ccb << " >= 0.01");
  //BOOST_CHECK_MESSAGE(ccc == 0 || static_cast<float>(cc)/ccc < 0.01, "The bias for component a seems to be too high : " << static_cast<float>(cc)/ccc << " >= 0.01");
  
  
  delete im;

}

void register_io_png_test(test_suite*& test) {
  
  test->add( BOOST_TEST_CASE( &WritePNGTest       ));
  test->add( BOOST_TEST_CASE( &ReadPNGTest        ));
  test->add( BOOST_TEST_CASE( &WritePNGTestColor  ));
  test->add( BOOST_TEST_CASE( &ReadPNGTestColor   ));
  
}

