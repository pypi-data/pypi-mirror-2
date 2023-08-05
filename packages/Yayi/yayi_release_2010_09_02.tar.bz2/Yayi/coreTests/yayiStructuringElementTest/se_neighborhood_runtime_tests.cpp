/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */





/*!@file
 * This file test the functions associated to runtime neighborhoods elements
 *
 * @author Raffi Enficiaud
 */

#include "main.hpp"
#include "Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp"
#include "Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp"
#include "Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp"

#include <set>

using namespace yayi;
using namespace yayi::se;


#define SE_FROM_TABLE(x) image_t::coordinate_type::from_table_multiple(x, x + sizeof(x)/sizeof(x[0]))

Image<yaUINT8>::coordinate_type::scalar_coordinate_type const coords[] = {0,0, 1,0, -1,0, 0,1};

class se_runtime_Neigh_basic {
public:
  
  typedef Image<yaUINT8> image_t;
  typedef s_neighborlist_se<image_t::coordinate_type> se_t;
  //static const image_t::coordinate_type::scalar_coordinate_type coords [];

  typedef Image<yaUINT8, s_coordinate<3> > image3D_t;
  typedef s_neighborlist_se<image3D_t::coordinate_type> se3D_t;


  se_t se;
  se_t const sec;
  se3D_t const se3D;
  image_t im;
  image3D_t im3D;
  
  se_runtime_Neigh_basic() : se(SE_FROM_TABLE(coords)), sec(SE_FROM_TABLE(coords)), se3D(SESquare3D), im(), im3D()
  {
    im.SetSize(c2D(10, 10));
    if(im.AllocateImage() != yaRC_ok)
      throw std::runtime_error("error while allocating the image");
      
    for(offset o = 0; o < 10*10; o++) {
      im.pixel(o) = o % 7;
    }
    
    im3D.SetSize(c3D(10,5,5));
    if(im3D.AllocateImage() != yaRC_ok)
      throw std::runtime_error("error while allocating the image");
      
    for(offset o = 0; o < 10*5*5; o++) {
      im3D.pixel(o) = o % 7;
    }


  }
  

  // Basic tests for centering the structuring element (inside the image, on the borders, fast centering...)
  void test_basics() {
    BOOST_CHECKPOINT("test_basics");
    
    BOOST_REQUIRE(se.size() == 4);
    BOOST_REQUIRE(im.IsAllocated());
    
    BOOST_REQUIRE(se3D.size() == 27);
    BOOST_REQUIRE(im3D.IsAllocated());    
    
    BOOST_CHECKPOINT("test_basics:1");
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se);
    
    BOOST_CHECKPOINT("test_basics:2");
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics:3");    
    BOOST_CHECK(n.center(c2D(3, 3)) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics:4");    
    BOOST_CHECK_MESSAGE(n.begin().Position() == c2D(3,3), "bad first element: position = " << n.begin().Position() << " != " << c2D(3,3));

    BOOST_CHECKPOINT("test_basics:5");
    unsigned int count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it) {
      count ++;
    }
    BOOST_REQUIRE_MESSAGE(count == 4, "bad number of neighbors : # = " << count << " != " << 4);
    
    
    BOOST_CHECKPOINT("test_basics:6");    
    count = 0;
    offset off[] = {0, 1, -1, 10};
    offset center = 10*3 + 3;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
      
    }
    BOOST_CHECK_MESSAGE(count == 4, "bad number of neighbors : # = " << count << " != " << 4);

    count = 0;
    for(neigh_t::const_iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
      
    }
    BOOST_CHECK_MESSAGE(count == 4, "bad number of neighbors : # = " << count << " != " << 4);    
    
    count = 0;
    BOOST_CHECK(n.shift_center() == yaRC_ok);
    center++;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    }
    BOOST_CHECK_MESSAGE(count == 4, "bad number of neighbors : # = " << count << " != " << 4);    
    
    BOOST_CHECK(n.safe_center(c2D(4, 7)) == yaRC_ok);
    center = 10*7 + 4;
    count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    }
    BOOST_CHECK_MESSAGE(count == 4, "bad number of neighbors : # = " << count << " != " << 4);    
  
    BOOST_CHECK(n.center(c2D(9, 7)) == yaRC_ok);
    center = 10*7 + 9;
    count = 0;
    offset off2[] = {0, -1, 10};
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      if(count < 3)
        BOOST_CHECK_MESSAGE(it.Offset() == center + off2[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    }    
    BOOST_CHECK_MESSAGE(count == 3, "bad number of neighbors : # = " << count << " != " << 3);  
    
    BOOST_CHECK(n.center(c2D(9, 9)) == yaRC_ok);
    center = 10*9 + 9;
    count = 0;
    offset off3[] = {0, -1};
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      if(count < 2)
        BOOST_CHECK_MESSAGE(it.Offset() == center + off3[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    }    
    BOOST_CHECK_MESSAGE(count == 2, "bad number of neighbors : # = " << count << " != " << 2);  
    
  
  }
  
  void test_basics3D() {
    BOOST_REQUIRE(se3D.size() == 27);
    BOOST_REQUIRE(im3D.IsAllocated());

    BOOST_CHECKPOINT("test_basics3D:1");
    typedef s_runtime_neighborhood<image3D_t, se3D_t> neigh_t;
    neigh_t n(im3D, se3D);
    
    BOOST_CHECKPOINT("test_basics3D:2");
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics3D:3");
    BOOST_CHECK(n.center(c3D(3, 3, 3)) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics:4");    
    BOOST_CHECK_MESSAGE(n.begin().Position() == c3D(3,3,3), "bad first element: position = " << n.begin().Position() << " != " << c3D(3,3,3));

    int count = 0;
    std::set<image3D_t::coordinate_type> s;
    for(int z = 2; z <= 4; z++)
    {
      for(int y = 2; y <= 4; y++)
      {
        for(int x = 2; x <= 4; x++)
        {
          s.insert(c3D(x,y,z));
        }
      }
    }
    BOOST_CHECK_MESSAGE(s.size() == 27, "Incorrect size of the set");
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im3D.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im3D.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(s.count(it.Position()) > 0, "error : an incorrect neighbor found for index " << count << " position " << it.Position());
    }    
    BOOST_CHECK_MESSAGE(count == 27, "bad number of neighbors : # = " << count << " != " << 27);  


    BOOST_CHECK(n.center(c3D(3, 4, 4)) == yaRC_ok);
    count = 0;
    s.clear();
    for(int z = 3; z <= 4; z++)
    {
      for(int y = 3; y <= 4; y++)
      {
        for(int x = 2; x <= 4; x++)
        {
          s.insert(c3D(x,y,z));
        }
      }
    }
    BOOST_CHECK_MESSAGE(s.size() == 12, "Incorrect size of the set " << s.size() << " != 12 (should be)");
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im3D.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im3D.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(s.count(it.Position()) > 0, "error : an incorrect neighbor found for index " << count << " position " << it.Position());
    }    
    BOOST_CHECK_MESSAGE(count == 12, "bad number of neighbors : # = " << count << " != " << 12);  


  }
  
  void test_shifts() {
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se);
    
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);
    BOOST_CHECK(n.center(c2D(3, 3)) == yaRC_ok);

    offset off[] = {0, 1, -1, 10};
    offset center = 10*3 + 3;
  
    for(int i = 0; i < 5; i++) {
      int count = 0;
      for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
        BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
        BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
        BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
        BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
      }          
    
      BOOST_CHECK(n.shift_center() == yaRC_ok);
      BOOST_CHECK(count == 4);
      center++;
    }
  
  }

  void test_remove_center() {
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se.remove_center());
    
    BOOST_CHECK(n.center(c2D(3, 3)) == yaRC_ok);

    offset center = 10*3 + 3;
  
    int count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(it.Offset() != center, "error for the remove center: on center at iteration " << count);
    }          
  
    BOOST_CHECK_MESSAGE(count == 3, "Bad number of neighbors for the SE without center : " << count << " != " << 3);
  
  }



  
  void test_crops() {
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se);
    
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);
    BOOST_CHECK(n.center(c2D(9, 3)) == yaRC_ok);  
    
    offset off[] = {0, -1, 10};
    offset center = 10*3 + 9;
    int count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    } 
    BOOST_CHECK(count == 3);
    

    
    
    
    
    neigh_t n2(im, SESquare2D);
    BOOST_CHECK(n2.center(c2D(7, 9)) == yaRC_ok);  
    
    offset off2[] = {0, 1, -1, -10, -9, -11};
    center = 10*9 + 7;
    count = 0;
    for(neigh_t::iterator it(n2.begin()), ite(n2.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off2[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off2[count]);
    } 
    BOOST_CHECK_MESSAGE(count == 6, "bad count " << count << "(real) != 6 (theory)"); 
    
  }
  
  
  

public:
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<se_runtime_Neigh_basic> instance( new se_runtime_Neigh_basic );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_basic::test_basics, instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_basic::test_shifts, instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_basic::test_crops,  instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_basic::test_basics3D,instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_basic::test_remove_center, instance ) );

  }
};






Image<yaUINT8>::coordinate_type::scalar_coordinate_type const coords_hexa[] = {
  0,0, 1,0, -1,0, 0,1, 0,-1, 1,-1, 1,1,
  0,0, 1,0, -1,0, 0,1, 0,-1, -1,-1, -1,1
  };
class se_runtime_Neigh_hexa {
public:
  
  typedef Image<yaUINT8> image_t;
  typedef s_neighborlist_se_hexa_x<image_t::coordinate_type> se_t;


  se_t se;
  se_t const sec;
  image_t im;
  se_runtime_Neigh_hexa() : se(SE_FROM_TABLE(coords_hexa)), sec(SE_FROM_TABLE(coords_hexa)), im()
  {
    im.SetSize(c2D(10, 10));
    if(im.AllocateImage() != yaRC_ok)
      throw std::runtime_error("error while allocating the image");
      
    for(offset o = 0; o < 10*10; o++) {
      im.pixel(o) = o % 7;
    }      
  }
  
  void test_basics() {
    BOOST_CHECKPOINT("test_basics");
    
    BOOST_REQUIRE(se.size() == 14);
    BOOST_REQUIRE(im.IsAllocated());
    
    BOOST_CHECK(se.has_multiple_list());
    BOOST_CHECK(se.number_of_list() == 2);

    BOOST_CHECKPOINT("test_basics:1");
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se);
    
    BOOST_CHECKPOINT("test_basics:2");
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics:3");    
    BOOST_CHECK(n.center(c2D(3, 3)) == yaRC_ok);

    BOOST_CHECKPOINT("test_basics:4");    
    BOOST_CHECK_MESSAGE(n.begin().Position() == c2D(3,3), "bad first element: position = " << n.begin().Position() << " != " << c2D(3,3));

    BOOST_CHECKPOINT("test_basics:5");
    unsigned int count = 0;
    static const image_t::coordinate_type coords_test[] = {c2D(3,3), c2D(4,3), c2D(2,3), c2D(3,4), c2D(3,2), c2D(4,2), c2D(4,4)};
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it) {
      BOOST_CHECK_MESSAGE(it.Position() == coords_test[count], "Inconsistent position for index " << count << " : " << it.Position() << " != " << coords_test[count]);
      count ++;
    }
    BOOST_CHECK_MESSAGE(count == 7, "bad number of neighbors : # = " << count << " != " << 7);

    BOOST_CHECKPOINT("test_basics:6");
    BOOST_CHECK(n.center(c2D(7, 4)) == yaRC_ok);
    BOOST_CHECK_MESSAGE(n.begin().Position() == c2D(7,4), "bad first element: position = " << n.begin().Position() << " != " << c2D(7,4));
    count = 0;
    static const image_t::coordinate_type coords_test2[] = {c2D(7,4), c2D(8,4), c2D(6,4), c2D(7,5), c2D(7,3), c2D(6,3), c2D(6,5)};
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it) {
      BOOST_CHECK_MESSAGE(it.Position() == coords_test2[count], "Inconsistent position for index " << count << " : " << it.Position() << " != " << coords_test[count]);
      count ++;
    }
    BOOST_CHECK_MESSAGE(count == 7, "bad number of neighbors : # = " << count << " != " << 7);

    BOOST_CHECKPOINT("test_basics:6 bis (transpose)");
    static const image_t::coordinate_type coords_test3[] = {c2D(7,4), c2D(8,4), c2D(6,4), c2D(7,5), c2D(7,3), c2D(8,3), c2D(8,5)};
    neigh_t nt(im, se.transpose());
    BOOST_CHECK(nt.center(c2D(7, 4)) == yaRC_ok);
    BOOST_CHECK_MESSAGE(nt.begin().Position() == c2D(7,4), "bad first element: position = " << nt.begin().Position() << " != " << c2D(7,4));
    count = 0;
    for(neigh_t::iterator it(nt.begin()), ite(nt.end()); it != ite; ++it) {
      BOOST_CHECK_MESSAGE(it.Position() == coords_test3[count], "Inconsistent position for index " << count << " : " << it.Position() << " != " << coords_test3[count]);
      count ++;
    }
    BOOST_CHECK_MESSAGE(count == 7, "bad number of neighbors : # = " << count << " != " << 7);


    
    // test for center removed
    BOOST_CHECKPOINT("test_basics:7 (remove_center)");    
    neigh_t n2(im, se.remove_center());
    BOOST_CHECK(n2.center(c2D(7, 4)) == yaRC_ok);
    BOOST_CHECK_MESSAGE(n2.begin().Position() == c2D(8,4), "bad first element: position = " << n2.begin().Position() << " != " << c2D(8,4));
    count = 0;
    for(neigh_t::iterator it(n2.begin()), ite(n2.end()); it != ite; ++it) {
      if(count < sizeof(coords_test2)/sizeof(coords_test2[0]) - 1)
        BOOST_CHECK_MESSAGE(it.Position() == coords_test2[count+1], "Inconsistent position for index " << count << " : " << it.Position() << " != " << coords_test2[count+1]);
      count ++;
    }
    BOOST_CHECK_MESSAGE(count == 6, "bad number of neighbors : # = " << count << " != " << 6);

    BOOST_CHECK(n2.center(c2D(3, 3)) == yaRC_ok);
    BOOST_CHECK_MESSAGE(n2.begin().Position() == c2D(4,3), "bad first element: position = " << n2.begin().Position() << " != " << c2D(4,3));
    count = 0;
    for(neigh_t::iterator it(n2.begin()), ite(n2.end()); it != ite; ++it) {
      if(count < sizeof(coords_test)/sizeof(coords_test[0]) - 1)
        BOOST_CHECK_MESSAGE(it.Position() == coords_test[count+1], "Inconsistent position for index " << count << " : " << it.Position() << " != " << coords_test[count+1]);
      count ++;
    }
    BOOST_CHECK_MESSAGE(count == 6, "bad number of neighbors : # = " << count << " != " << 6);
    
    
  }
  
  void test_crops() {
    typedef s_runtime_neighborhood<image_t, se_t> neigh_t;
    neigh_t n(im, se);
    
    BOOST_CHECK(n.set_shift(1) == yaRC_ok);
    BOOST_CHECK(n.center(c2D(9, 3)) == yaRC_ok);  
    
    offset off[] = {0, -1, 10, -10};
    offset center = 10*3 + 9;
    int count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off[count]);
    } 
    BOOST_CHECK(count == 4);

    BOOST_CHECK(n.center(c2D(9, 4)) == yaRC_ok);  
    
    offset off2[] = {0, -1, 10, -10, -11, 9};
    center = 10*4 + 9;
    count = 0;
    for(neigh_t::iterator it(n.begin()), ite(n.end()); it != ite; ++it, count ++) {
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Position()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == im.pixel(it.Offset()), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(*it == (it.Offset() % 7), "error on neighborhood consistency for neighbor " << count);
      BOOST_CHECK_MESSAGE(it.Offset() == center + off2[count], "error on neighborhood consistency for neighbor " << count << " offset = " << it.Offset() << " != " << center + off2[count]);
    } 
    BOOST_CHECK(count == 6);     
        
  }    
  
public:
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<se_runtime_Neigh_hexa> instance( new se_runtime_Neigh_hexa );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_hexa::test_basics, instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &se_runtime_Neigh_hexa::test_crops, instance ) );

  }
};





void register_neighborhood_runtime_test(test_suite*& test) {
  
  se_runtime_Neigh_basic::register_tests(test);
  se_runtime_Neigh_hexa::register_tests(test);
}
