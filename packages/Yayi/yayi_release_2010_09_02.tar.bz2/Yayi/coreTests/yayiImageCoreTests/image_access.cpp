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
#include "Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp"
#include "Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp"

#include <iostream>

using namespace yayi;

class image_access_test 
{
public:
  typedef Image<yaUINT8> image_type;
  image_type im;


  void test_access()
  {
    BOOST_CHECKPOINT("test_access");
    
    image_type::coordinate_type coord;
    coord[0] = 10;
    coord[1] = 20;
    BOOST_CHECK(im.SetSize(coord) == yaRC_ok);

    BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
    
    //BOOST_CHECK_THROW(im.Size() = coord);

    image_type::interface_type& interface_ = dynamic_cast<image_type::interface_type&>(im);

    coord[0] = coord[1] = 0;
    image_type::interface_type::coordinate_type icoord = coord;
    image_type::interface_type::pixel_reference_type ref = interface_.pixel(icoord);

    *ref = static_cast<yaUINT8>(0);
    BOOST_CHECK_MESSAGE(*ref == variant(static_cast<yaUINT8>(0)), "The reference pixel value is != 0");
    yaUINT8 val = **ref;//->getPixel();
    BOOST_CHECK_MESSAGE(val == 0, "The reference pixel value is " << val << " != 0");
    
    
    *interface_.pixel(icoord) = variant(static_cast<yaUINT8>(0));

    val = **ref;
    BOOST_CHECK_MESSAGE(val == 0, "The reference pixel value is " << val << " != 0");
    *interface_.pixel(icoord) = variant(static_cast<yaUINT8>(0));
  }

  void test_swap()
  {
    BOOST_CHECKPOINT("test_swap");
    BOOST_REQUIRE_MESSAGE(im.FreeImage() == yaRC_ok, "im.FreeImage() error");
    image_type::coordinate_type coord, coord2;
    coord[0] = 10; coord[1] = 20;
    coord2[0] = 20; coord2[1] = 20;
    BOOST_CHECK(im.SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
    
    image_type im2;
    BOOST_CHECK(im2.SetSize(coord2) == yaRC_ok);
    
    for(int i = 0; i < coord[0] * coord[1]; i++)
      im.pixel(i) = i;
    
    BOOST_CHECK(im.swap(im2) == yaRC_ok);
    BOOST_CHECK(im.Size() == coord2);
    BOOST_CHECK(!im.IsAllocated());
    BOOST_REQUIRE(im2.Size() == coord);
    BOOST_REQUIRE(im2.IsAllocated());
    for(int i = 0; i < coord[0] * coord[1]; i++)
      BOOST_CHECK(im2.pixel(i) == i);
    
  }


  
  void test_access_errors()
  {
    BOOST_CHECKPOINT("test_access_errors");
    
    BOOST_REQUIRE_MESSAGE(im.FreeImage() == yaRC_ok, "im.FreeImage() error");
    #ifndef NDEBUG
    BOOST_CHECK_THROW(im.pixel(0), errors::yaException);
    #endif
    
    IImage::coordinate_type c_origin;
    c_origin.set_dimension(im.Size().dimension());
    for(unsigned int i = 0; i < im.Size().dimension(); i++)
      c_origin[i] = 0;
    BOOST_CHECK_THROW(dynamic_cast<const IImage&>(im).pixel(c_origin), errors::yaException);
    
    
    image_type::coordinate_type coord;
    coord[0] = 10;
    coord[1] = 20;
    BOOST_CHECK(im.SetSize(coord) == yaRC_ok);
    #ifndef NDEBUG
    BOOST_CHECK_THROW(im.pixel(0), errors::yaException);    
    #endif
    BOOST_CHECK_THROW(dynamic_cast<const IImage&>(im).pixel(c_origin), errors::yaException);    
    BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");
    BOOST_CHECK(im.SetSize(coord) != yaRC_ok);


    #ifndef NDEBUG
    BOOST_CHECK_THROW(im.pixel(-1), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(201), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(204031), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(c2D(10, 10)), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(c2D(11, 10)), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(c2D(5, 20)), errors::yaException);
    BOOST_CHECK_THROW(im.pixel(c2D(5, 21)), errors::yaException);
    #endif

  
  }
  
  
  void test_locks() {
    BOOST_CHECKPOINT("test_locks");
    
    BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock an empty image ?");
    BOOST_CHECK_MESSAGE(im.CanWriteLock(), "Cannot write lock an empty image ?");
    
    {
      image_type::read_lock_type o(im.ReadLock());
      BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock after read locking");
      BOOST_CHECK_MESSAGE(!im.CanWriteLock(), "Can write lock while read locked");
      image_type::read_lock_type o1(im.ReadLock());
      BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock after read locking");
      BOOST_CHECK_MESSAGE(!im.CanWriteLock(), "Can write lock while read locked");
      image_type::read_lock_type o2(im.ReadLock());
      BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock after read locking");
      BOOST_CHECK_MESSAGE(!im.CanWriteLock(), "Can write lock while read locked");
    
    }
    BOOST_CHECK_MESSAGE(im.CanWriteLock(), "Cannot write lock after emptying the read locks");  
    BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock after emptying the read locks");
    
    {
      image_type::write_lock_type o(im.WriteLock());
      BOOST_CHECK_MESSAGE(!im.CanReadLock(), "Can read lock after write locking");
      BOOST_CHECK_MESSAGE(!im.CanWriteLock(), "Can write lock while write locked");
    
    }

    BOOST_CHECK_MESSAGE(im.CanWriteLock(), "Cannot write lock after emptying the read locks");  
    BOOST_CHECK_MESSAGE(im.CanReadLock(), "Cannot read lock after emptying the read locks");


  }
  
  void test_streams() {
    BOOST_CHECKPOINT("test_streams");
  
    image_type im_test;
    image_type::coordinate_type coord;
    coord[0] = 5;
    coord[1] = 4;
    BOOST_REQUIRE(im_test.SetSize(coord) == yaRC_ok);

    BOOST_REQUIRE_MESSAGE(im_test.AllocateImage() == yaRC_ok, "im_test.AllocateImage() error");
    
    static const std::string s = 
      "1 2 3 4 5 "
      "6 7 8 8 10 "
      //"11 12 13 14 15 "
      "255 254 253 252 251 "
      "128 127 126 125 124";
    
    
    //std::cout << "Testing the streaming function " << std::endl;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
    
    image_type im_test2;
    BOOST_CHECK_MESSAGE(!(is >> im_test2), "Error during the input streaming of the unitialized image");

    int v = im_test.pixel(c2D(0,0));
    BOOST_CHECK(v == 1);

    v = 0;
    v = im_test.pixel(0);
    BOOST_CHECK(v == 1);
    
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(0,0)) == 1, "(pixel(0,0) = " << (int)im_test.pixel(c2D(0,0)) << ") != 1");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(1,0)) == 2, "(pixel(1,0) = " << (int)im_test.pixel(c2D(1,0)) << ") != 2");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(2,0)) == 3, "(pixel(2,0) = " << (int)im_test.pixel(c2D(2,0)) << ") != 3");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(3,0)) == 4, "(pixel(3,0) = " << (int)im_test.pixel(c2D(3,0)) << ") != 4");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(4,0)) == 5, "(pixel(4,0) = " << (int)im_test.pixel(c2D(4,0)) << ") != 5");

    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(0,1)) == 6, "(pixel(0,1) = " << (int)im_test.pixel(c2D(0,1)) << ") != 6");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(1,1)) == 7, "(pixel(1,1) = " << (int)im_test.pixel(c2D(1,1)) << ") != 7");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(2,1)) == 8, "(pixel(2,1) = " << (int)im_test.pixel(c2D(2,1)) << ") != 8");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(3,1)) == 8, "(pixel(3,1) = " << (int)im_test.pixel(c2D(3,1)) << ") != 8");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(4,1)) == 10, "(pixel(4,1) = "<< (int)im_test.pixel(c2D(4,1)) << ") != 10");

    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(0,2)) == 255, "(pixel(0,2) = " << (int)im_test.pixel(c2D(0,2)) << ") != 255");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(1,2)) == 254, "(pixel(1,2) = " << (int)im_test.pixel(c2D(1,2)) << ") != 254");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(2,2)) == 253, "(pixel(2,2) = " << (int)im_test.pixel(c2D(2,2)) << ") != 253");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(3,2)) == 252, "(pixel(3,2) = " << (int)im_test.pixel(c2D(3,2)) << ") != 252");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(4,2)) == 251, "(pixel(4,2) = " << (int)im_test.pixel(c2D(4,2)) << ") != 251");

    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(0,3)) == 128, "(pixel(0,3) = " << (int)im_test.pixel(c2D(0,3)) << ") != 128");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(1,3)) == 127, "(pixel(1,3) = " << (int)im_test.pixel(c2D(1,3)) << ") != 127");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(2,3)) == 126, "(pixel(2,3) = " << (int)im_test.pixel(c2D(2,3)) << ") != 126");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(3,3)) == 125, "(pixel(3,3) = " << (int)im_test.pixel(c2D(3,3)) << ") != 125");
    BOOST_CHECK_MESSAGE(im_test.pixel(c2D(4,3)) == 124, "(pixel(4,3) = " << (int)im_test.pixel(c2D(4,3)) << ") != 124");

    {
      static const std::string s_bad = 
        "1 3 4 5 " // one missing value
        "6 7 8 8 10 "
        //"11 12 13 14 15 "
        "255 254 253 252 251 "
        "128 127 126 125 124";
      std::istringstream is(s_bad);
      BOOST_CHECK_MESSAGE(!(is >> im_test), "Error not reported properly (missing value)");
    }
    
    // This is not an error
    /*{
      static const std::string s_bad = 
        "1 2 3 4 5 6" // one additionnal value
        "6 7 8 8 10 "
        //"11 12 13 14 15 "
        "255 254 253 252 251 "
        "128 127 126 125 124";
      std::istringstream is(s_bad);
      BOOST_CHECK_MESSAGE(!(is >> im_test), "Error not reported properly (too many value)");
    }*/
    
    {
      static const std::string s_bad = 
        "1 2 3 4 5 " 
        "6 7 8 8 10 "
        //"11 12 13 14 15 "
        "255 254 q 252 251 " // bad format
        "128 127 126 125 124";
      std::istringstream is(s_bad);
      BOOST_CHECK_MESSAGE(!(is >> im_test), "Error not reported properly (one bad format)");
    }        
  }
  
  void test_get_same()
  {
    BOOST_CHECKPOINT("test_get_same");
    
    
    image_type imtemp; imtemp.set_same(im);
    BOOST_CHECK(imtemp.Size() == im.Size());
    BOOST_CHECK(!imtemp.IsAllocated());
    
    typedef Image<yaUINT8, s_coordinate<3> > image_type3D;
    
    image_type3D im3D;
    BOOST_CHECK(im3D.SetSize(c3D(10, 15, 20)) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(im3D.AllocateImage() == yaRC_ok, "im3D.AllocateImage() error");
    
    Image<yaF_simple, s_coordinate<3> > im3Dtemp; im3Dtemp.set_same(im3D);
    BOOST_CHECK(im3Dtemp.Size() == im3D.Size());
    BOOST_REQUIRE_MESSAGE(im3Dtemp.IsAllocated(), "im3Dtemp.IsAllocated() error");
    
    
    
  }
  
  
  
  
  
  static void declare_tests(test_suite*& test) {
    boost::shared_ptr<image_access_test> instance( new image_access_test );
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_access,  instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_access_errors, instance));
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_swap,    instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_locks,   instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_streams, instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_access_test::test_get_same,instance ) );
  }

  
};


void register_image_access_test(test_suite*& test)
{
  image_access_test::declare_tests(test);
}

