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
 * This file test the functions associated to structuring elements (ie. not the neighborhoods)
 *
 * @author Raffi Enficiaud
 */

#include "main.hpp"
#include "Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp"
#include "Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp"
#include <iostream>

using namespace yayi;
using namespace yayi::se;


class se_predefined_basic_tests
{
public:

  void test_predefined_se()
  {
    BOOST_CHECKPOINT("test_predefined_se");
    
    BOOST_CHECK(SEHex2D.size() == 14);
    BOOST_CHECK(SEHex2D.number_of_list() == 2);
    BOOST_CHECK(SEHex2D.has_multiple_list());
    BOOST_CHECK(SEHex2D.GetType() == e_set_neighborlist);
    BOOST_CHECK(SEHex2D.GetSubType() == e_sest_neighborlist_hexa);

    BOOST_CHECK(SEHex2D.maximum_extension().first == c2D(-1,-1));
    BOOST_CHECK_MESSAGE(SEHex2D.maximum_extension().second == c2D(1,1), "Maximal extension error : " << SEHex2D.maximum_extension().second << " != " << c2D(1,1));
    
    BOOST_CHECK(SESquare2D.size() == 9);
    BOOST_CHECK(SESquare2D.number_of_list() == 1);
    BOOST_CHECK(!SESquare2D.has_multiple_list());
    BOOST_CHECK(SESquare2D.GetType() == e_set_neighborlist);
    BOOST_CHECK(SESquare2D.GetSubType() == e_sest_neighborlist_generic_single);


    BOOST_CHECK(SESquare3D.size() == 27);
    BOOST_CHECK(SESquare3D.number_of_list() == 1);
    BOOST_CHECK(!SESquare3D.has_multiple_list());
    BOOST_CHECK(SESquare3D.GetType() == e_set_neighborlist);
    BOOST_CHECK(SESquare3D.GetSubType() == e_sest_neighborlist_generic_single);
    
  }


  void test_operations()
  {
    BOOST_CHECKPOINT("test_operations");
    
    BOOST_CHECK(SEHex2D == SEHex2D);
    BOOST_CHECK(!(SEHex2D != SEHex2D));

    BOOST_CHECK(SEHex2D.remove_center() != SEHex2D);
    BOOST_CHECK(!(SEHex2D.remove_center() == SEHex2D));
    
    BOOST_CHECK(SEHex2D.is_equal_unordered(SEHex2D));
    BOOST_CHECK(!SEHex2D.remove_center().is_equal_unordered(SEHex2D));
    BOOST_CHECK(!SEHex2D.is_equal_unordered(SEHex2D.remove_center()));
    
    BOOST_CHECK(SESquare2D.size() == SESquare2D.remove_center().size() + 1);
    
    
    
    BOOST_CHECK(dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal(&SESquare2D));
    BOOST_CHECK(!dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal(&SEHex2D));
    BOOST_CHECK(dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal_unordered(&SESquare2D));
    BOOST_CHECK(!dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal_unordered(&SEHex2D));


  }
  



  
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<se_predefined_basic_tests> instance( new se_predefined_basic_tests );
    test->add( BOOST_CLASS_TEST_CASE( &se_predefined_basic_tests::test_predefined_se,   instance ) );  
    test->add( BOOST_CLASS_TEST_CASE( &se_predefined_basic_tests::test_operations,      instance ) );
  }
  
};


class se_test_basic
{
public:

  void test_interface_se()
  {
    BOOST_CHECKPOINT("test_interface_se");	
  }

  void test_clone()
  {
    BOOST_CHECKPOINT("test_predefined_se");
    
    const IStructuringElement* se_ = &SEHex2D, *se2_ = se_->Clone(), *se3_ = se_->Transpose();
    
    BOOST_CHECK(se_);
    BOOST_CHECK(se2_);
    BOOST_CHECK(se3_);
        
    delete se2_;
    delete se3_;
  }
  
  void test_remove_center()
  {
    typedef s_coordinate<2> coordinate_type;
    BOOST_CHECKPOINT("test_remove_center");
    BOOST_CHECK(SEHex2D.size() == 14);
    BOOST_CHECK(SEHex2D.remove_center().size() == 12);
    BOOST_CHECK(SEHex2D.number_of_list() == 2);
    BOOST_CHECK(SEHex2D.remove_center().number_of_list() == 2);
    BOOST_CHECK(SEHex2D.has_multiple_list());
    BOOST_CHECK(SEHex2D.remove_center().has_multiple_list());
    BOOST_CHECK(SEHex2D.GetType() == e_set_neighborlist);
    BOOST_CHECK(SEHex2D.remove_center().GetType() == e_set_neighborlist);
    BOOST_CHECK(SEHex2D.GetSubType() == e_sest_neighborlist_hexa);
    BOOST_CHECK(SEHex2D.remove_center().GetSubType() == e_sest_neighborlist_hexa);
    
    s_neighborlist_se_hexa_x<coordinate_type> se, sep;
    
    static const coordinate_type::scalar_coordinate_type coords [] = {0,0, 1,0, -1,0, 0,1,   0,0, 1,0, -1,0, 0,-1};
    
    std::vector<coordinate_type> v(coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
    BOOST_REQUIRE(v.size() == 8);
    
    BOOST_CHECK_MESSAGE(se.size() == 0, "SE size = " << se.size() << " != 0");
    BOOST_CHECK(se.set_coordinates(v) == yaRC_ok);
    BOOST_CHECK_MESSAGE(se.size() == 8, "SE size = " << se.size() << " != 6");
    BOOST_CHECK_MESSAGE(*se.begin() == c2D(0,0), "First element corrupted " << *se.begin() << " != " << c2D(0,0));
    
    BOOST_CHECK_MESSAGE(se.remove_center().size() == 6, "SE size = " << se.size() << " != 6");
    BOOST_CHECK_MESSAGE(*se.remove_center().begin() == c2D(1,0), "First element (removed center) corrupted " << *se.remove_center().begin() << " != " << c2D(1,0));
    BOOST_CHECK_MESSAGE(*(se.remove_center().begin() + 3) == c2D(1,0), "Forth element (removed center) corrupted " << *se.remove_center().begin() << " != " << c2D(1,0));

    sep = se.remove_center();
    BOOST_CHECK_MESSAGE(sep.size() == 6, "SE size = " << sep.size() << " != 6");
    BOOST_CHECK_MESSAGE(*sep.begin() == c2D(1,0), "First element (removed center) corrupted " << *sep.begin() << " != " << c2D(1,0));
    BOOST_CHECK_MESSAGE(*(sep.begin() + 3) == c2D(1,0), "Forth element (removed center) corrupted " << *sep.begin() << " != " << c2D(1,0));

    
  }
  
  
  
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<se_test_basic> instance( new se_test_basic );
    test->add( BOOST_CLASS_TEST_CASE( &se_test_basic::test_interface_se,  instance ) );  
    test->add( BOOST_CLASS_TEST_CASE( &se_test_basic::test_clone,         instance ) );  
    test->add( BOOST_CLASS_TEST_CASE( &se_test_basic::test_remove_center, instance ) );
  
  }
  
};






void register_se_test(test_suite*& test)
{
  se_predefined_basic_tests::register_tests(test);
  se_test_basic::register_tests(test);
}

