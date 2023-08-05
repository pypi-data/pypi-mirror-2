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

#include "Yayi/core/yayiImageCore/include/ApplyToImage_T.hpp"
#include <Yayi/core/yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <Yayi/core/yayiImageCore/include/ApplyToImage_binary_t.hpp>

#include <boost/type_traits/is_same.hpp>
#include <boost/function.hpp>
#include <boost/bind.hpp>

#include <iostream>

using namespace yayi;



struct s_two_times {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T> struct result<op(T)> {
    typedef void type;
  };
  template <class op, class T> struct result<op(const T&)> {
    typedef T type;
  };
  
  
  template <class T>
  void operator()(T& x) throw() {
    x *= 2;
    count ++;
  }

  template <class T1, class T2>
  T2 operator()(const T1& x) throw() {
    count ++;
    return x * 2;
  }

};

struct s_tree_times {
  typedef yayi::ns_operator_tag::operator_commutative operator_tag;
  typedef void result;
  template <class T>
  void operator()(T& x) const throw() {
    x *= 3;
  }
};

struct s_square {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T1, class T2> struct result<op(T1, T2)> {
    typedef typename remove_reference<T2>::type type;
  };
  
  
  template <class T1, class T2>
  typename result<s_square(T1, T2)>::type operator()(T1 x, T2 y) {
    count ++;
    return x * x + y * y;
  }
};


// checks the tags are properly extracted

BOOST_MPL_ASSERT_NOT(( ns_operator_tag::has_operator_tag<s_two_times> ));
BOOST_MPL_ASSERT(( ns_operator_tag::has_operator_tag<s_tree_times> ));

class image_apply_test 
{
public:
  typedef Image<yaUINT16> image_type;
  image_type im, im1, im2;
  
  void CreateImages() {
    BOOST_REQUIRE(im1.SetSize(c2D(5,5)) == yaRC_ok);
    BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
    BOOST_REQUIRE(im2.SetSize(c2D(5,5)) == yaRC_ok);
    BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);  
    BOOST_REQUIRE(im.SetSize(c2D(5,5)) == yaRC_ok);
    BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);  
  }
  
  void PrepareImages() {
    static const std::string s = 
      "1 2 3 4 5 "
      "6 7 8 8 10 "
      "11 12 13 14 15 "
      "255 254 253 252 251 "
      "128 127 126 125 124";

    std::istringstream is(s);
    BOOST_REQUIRE_MESSAGE(is >> im1, "Error during the input streaming of the image");
    BOOST_CHECK_MESSAGE(im1.pixel(c2D(4,0)) == 5, "(pixel(4,0) = " << (int)im1.pixel(c2D(4,0)) << ") != 5");  

    std::istringstream is2(s);
    BOOST_REQUIRE_MESSAGE(is2 >> im2, "Error during the input streaming of the image");
  }

  void test_image_application1() {
    // Unary operator in-place
    BOOST_CHECKPOINT("test_image_application1");	
    
    s_apply_unary_operator/*<s_two_times>*/ op_im;
    s_two_times op;
    op.count = 0;
    
    BOOST_CHECK(op_im(im1, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 25, "Number of counted operations " << op.count << " !=  " << 25);
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
      BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
    }
    
    
    // fonction Process à tester également
  }
  
  void test_image_application1_inplace() {
    // Unary operator in-place
    BOOST_CHECKPOINT("test_image_application1_inplace");
    
    PrepareImages();
    
    s_apply_unary_operator op_im;
    s_two_times op;
    op.count = 0;
    
    BOOST_CHECK(op_im(im1, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 25, "Number of counted operations " << op.count << " !=  " << 25);
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
      BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
    }
    
    
    // fonction Process à tester également
  }


  void test_image_application1_notinplace() {
    // Unary operator in-place
    BOOST_CHECKPOINT("test_image_application1_notinplace");
    
    PrepareImages();
    
    s_two_times op;
    
    // Adapting the appropriate overloaded method of the object
    boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
    f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
    
    s_apply_unary_operator op_im;

    op.count = 0;
    
    BOOST_CHECK(op_im(im1, im, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 25, "Number of counted operations " << op.count << " !=  " << 25);
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) {
      BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
      BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
    }
    
    
    // fonction Process à tester également
  }


  void test_image_application2() {
    BOOST_CHECKPOINT("test_image_application2");	

    PrepareImages();

    s_apply_binary_operator op_im;
    s_square op;
    op.count = 0;
    
    BOOST_CHECK(op_im(im1, im1, im2, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 25, "Number of counted operations " << op.count << " !=  " << 25);
    
    for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
      BOOST_CHECK_MESSAGE(*it2 == static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/, "failure with *it2 = " << (int)(*it2) << " and 2 * (*it1) *  (*it1) = " << static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/);
    }

    PrepareImages();
    op.count = 0;
    BOOST_CHECK(op_im(im1, im1, im1, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 25, "Number of counted operations " << op.count << " !=  " << 25);
    
    for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
      BOOST_CHECK_MESSAGE(*it1 == static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/, "failure with *it1 = " << (int)(*it1) << " and 2 * (*it2) *  (*it2) = " << static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/);
    }

   
  }


  void test_image_windowed_unary_application() {
    BOOST_CHECKPOINT("test_image_windowed_unary_application");	
    
    PrepareImages();
    
    s_two_times op;
    
    // Adapting the appropriate overloaded method of the object
    boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
    f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
    
    s_apply_unary_operator op_im;

    op.count = 0;
    
    s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2));
    
    for(int i = 0; i < total_number_of_points(im.Size()); i++)
      im.pixel(i) = i;
    
    BOOST_CHECK(op_im(im1, window, im, window, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(total_number_of_points(window.Size()) == 4, "Number of point mistake " << total_number_of_points(window.Size()) << " !=  " << 4);
    BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) 
    {
      if(is_point_inside(window, it.Position()))
      {
        BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
      }
      else
      {
        BOOST_CHECK_MESSAGE(*it2 == it.Offset(), "failure with it.Offset() = " << (int)(it.Offset()) << " and *it2 = " << *it2 << " - operation made outside the window");
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));      
      }
    }
    
    
    PrepareImages();
    op.count = 0;
    s_hyper_rectangle<2> window2(c2D(3,3), c2D(3,3));
    for(int i = 0; i < total_number_of_points(im.Size()); i++)
      im.pixel(i) = i;

    BOOST_CHECK(op_im(im1, window, im, window2, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);

    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) 
    {
      if(is_point_inside(s_hyper_rectangle<2>(c2D(3,3), c2D(2,2)), it.Position()))
      {
        BOOST_CHECK(is_point_inside(window2, it.Position()));
        BOOST_CHECK_MESSAGE(*it2 == 2 * im1.pixel(it2.Position() - c2D(3,3) + c2D(1,1)), 
          "failure with *it = " << (int)(*it) 
          << " and 2 * im1.pixel(it2.Position() - c2D(3,3) + c2D(1,1)) = " << 2 * im1.pixel(it2.Position() - c2D(3,3) + c2D(1,1))
          << " for position " << it2.Position()
          );
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
      }
      else
      {
        BOOST_CHECK_MESSAGE(*it2 == it.Offset(), 
          "failure with it.Offset() = " << (int)(it.Offset()) 
          << " and *it2 = " << *it2 
          << " at position " << it.Position()
          << " - operation made outside the window");
        BOOST_CHECK_MESSAGE(*it == *it3, "failure of const original with *it (result) = " << (int)(*it) << " and *it3 (original) = " << (int)(*it3));      
      }
    }
    
  }





  
  // TODO add more tests for different type of images
  
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<image_apply_test> instance( new image_apply_test );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::CreateImages,                          instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::PrepareImages,                         instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::test_image_application1,               instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::test_image_application1_inplace,       instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::test_image_application1_notinplace,    instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::test_image_application2,               instance ) );
    test->add( BOOST_CLASS_TEST_CASE( &image_apply_test::test_image_windowed_unary_application, instance ) );
  }
  
};






void register_image_apply_test(test_suite*& test) {
  image_apply_test::register_tests(test);
}

