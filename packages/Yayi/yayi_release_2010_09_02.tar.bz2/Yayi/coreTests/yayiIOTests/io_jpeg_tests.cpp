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
void WriteJPGTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test jpg write");	
  
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
  
  yaRC ret = yayi::IO::writeJPG("test.jpg", &im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeJPG error " << ret);
}

void ReadJPGTest() {
  using namespace yayi;
  BOOST_CHECKPOINT("test jpg read");	
  
  
  IImage *im = 0;
  yaRC ret = yayi::IO::readJPG("test.jpg", im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "read error " + static_cast<string_type>(ret));
  
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


void WriteJPGTestColor() {
  using namespace yayi;
  BOOST_CHECKPOINT("test jpg write (color)");	
  
  typedef Image<s_compound_pixel_t<yaUINT8,  mpl::int_<3> > > image_type;
  image_type im;
  
  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  
  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i).a = i % 255;
    im.pixel(i).b = std::abs(255-i) % 255;
    im.pixel(i).c = (128+i) % 255;
  }
  
  yaRC ret = yayi::IO::writeJPG("test_c.jpg", &im);
  string_type str = static_cast<string_type>(ret);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeJPG error " << ret);
}


void ReadJPGTestColor() {
  using namespace yayi;
  BOOST_CHECKPOINT("test jpg read");	
  
  
  IImage *im = 0;
  yaRC ret = yayi::IO::readJPG("test_c.jpg", im);
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
  
  // Since JPEG is non-lossless, we should use a more appropriate measurement of the bias
  int ca(0), cb(0), cc(0), cca(0), ccb(0), ccc(0);
  unsigned int max_diff_a(0), max_diff_b(0), max_diff_c(0);
  
  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_WARN_MESSAGE(im_t->pixel(i).a == (i % 255),  "pixel bad value (a) : i = " << i << " p = " << (int)im_t->pixel(i).a << " != " << i % 255);
    if(im_t->pixel(i).a != (i % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).a - (i % 255));
      max_diff_a = std::max(max_diff_a, d);
      ca += d * d;
      cca++;
    }
    
    
    BOOST_WARN_MESSAGE(im_t->pixel(i).b == (std::abs(255-i) % 255),  "pixel bad value (b) : i = " << i << " p = " << (int)im_t->pixel(i).b << " != " << std::abs(255-i)%255);
    if(im_t->pixel(i).b != (std::abs(255-i) % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).b - (std::abs(255-i) % 255));
      cb += d * d;
      max_diff_b = std::max(max_diff_b, d);
      ccb++;
    }

    BOOST_WARN_MESSAGE(im_t->pixel(i).c == ((128+i) % 255),  "pixel bad value (c) : i = " << i << " p = " << (int)im_t->pixel(i).c << " != " << (128+i)%255);
    if(im_t->pixel(i).c != ((128+i) % 255)) {
      unsigned int d = std::abs(im_t->pixel(i).c - ((128+i) % 255));
      cc += d * d;
      max_diff_b = std::max(max_diff_b, d);
      ccc++;
    }
  }
  
  BOOST_CHECK_MESSAGE(cca == 0 || static_cast<float>(ca)/ (coord[0] * coord[1]) < 0.01, "The mean quadratic error for component a seems to be too high : " << static_cast<float>(ca)/ (coord[0] * coord[1]) << " >= 0.01");
  BOOST_CHECK_MESSAGE(cca == 0 || static_cast<float>(cca)/(coord[0] * coord[1]) < 0.01, "The # of biased element for component a seems to be too high : " << static_cast<float>(cca)/(coord[0] * coord[1]) << " >= 0.01");

  BOOST_CHECK_MESSAGE(ccb == 0 || static_cast<float>(cb)/ (coord[0] * coord[1]) <= 0.04, "The mean quadratic error for component b seems to be too high : " << static_cast<float>(cb)/ (coord[0] * coord[1]) << " > 0.04");
  BOOST_CHECK_MESSAGE(ccb == 0 || static_cast<float>(ccb)/(coord[0] * coord[1]) <= 0.04, "The # of biased element for component b seems to be too high : " << static_cast<float>(ccb)/(coord[0] * coord[1]) << " > 0.04");

  BOOST_CHECK_MESSAGE(ccc == 0 || static_cast<float>(cc)/ (coord[0] * coord[1]) <= 0.04, "The mean quadratic error for component c seems to be too high : " << static_cast<float>(cc)/ (coord[0] * coord[1]) << " > 0.04");
  BOOST_CHECK_MESSAGE(ccc == 0 || static_cast<float>(ccc)/(coord[0] * coord[1]) <= 0.04, "The # of biased element for component c seems to be too high : " << static_cast<float>(ccc)/(coord[0] * coord[1]) << " > 0.04");

  BOOST_CHECK_MESSAGE(max_diff_a < 2, "The max deviation for component a seems to be too high : " << max_diff_a << " > 1");
  BOOST_CHECK_MESSAGE(max_diff_b < 2, "The max deviation for component b seems to be too high : " << max_diff_b << " > 1");
  BOOST_CHECK_MESSAGE(max_diff_c < 2, "The max deviation for component c seems to be too high : " << max_diff_c << " > 1");


  //BOOST_CHECK_MESSAGE(ccb == 0 || static_cast<float>(cb)/ccb < 0.01, "The bias for component a seems to be too high : " << static_cast<float>(cb)/ccb << " >= 0.01");
  //BOOST_CHECK_MESSAGE(ccc == 0 || static_cast<float>(cc)/ccc < 0.01, "The bias for component a seems to be too high : " << static_cast<float>(cc)/ccc << " >= 0.01");
  
  
  delete im;

}

void register_io_jpeg_test(test_suite*& test) {
  
  test->add( BOOST_TEST_CASE( &WriteJPGTest       ));
  test->add( BOOST_TEST_CASE( &ReadJPGTest        ));
  test->add( BOOST_TEST_CASE( &WriteJPGTestColor  ));
  test->add( BOOST_TEST_CASE( &ReadJPGTestColor   ));
  
}

