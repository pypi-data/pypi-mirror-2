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

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/include/common_types_T.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>
#include <Yayi/core/yayiCommon/common_pixels.hpp>
#include <Yayi/core/yayiCommon/common_pixels_T.hpp>




class types_and_variant_test 
{
public:

  struct s_dummy{};
  
  void test_types_class()
  {
    BOOST_CHECKPOINT("test_types_class");    
    using namespace yayi;
    
    
    BOOST_CHECKPOINT("test_types_class : tests de serialisation");  
    yayi::type t;
    t.c_type = yayi::type::c_scalar;
    t.s_type = yayi::type::s_ui32;
    
    
    yayi::string_type s = static_cast<yayi::string_type>(t);
    yayi::type tt = yayi::type::Create(s);
    
    BOOST_CHECK_MESSAGE(t == tt, s << " != " << static_cast<yayi::string_type>(tt));   
    
     
    t.c_type = yayi::type::c_coordinate;
    t.s_type = yayi::type::s_ui32;
    
    s = static_cast<yayi::string_type>(t);
    tt = yayi::type::Create(s);

    BOOST_CHECK_MESSAGE(t == tt, s << " != " << static_cast<yayi::string_type>(tt));   
  }


  void test_basic_types_size()
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test_basic_types_size 1");
    BOOST_CHECK(sizeof(yaUINT8) == 1);
    BOOST_CHECK(sizeof(yaINT8) == 1);
    BOOST_CHECK(sizeof(yaUINT16) == 2);
    BOOST_CHECK(sizeof(yaINT16) == 2);
    BOOST_CHECK_MESSAGE(sizeof(yaUINT32) == 4, "size of yaUINT32 " << sizeof(yaUINT32) << " != 4");
    BOOST_CHECK_MESSAGE(sizeof(yaINT32) == 4, "size of yaINT32 " << sizeof(yaINT32) << " != 4");
    BOOST_CHECK(sizeof(yaUINT64) == 8);
    BOOST_CHECK(sizeof(yaINT64) == 8);
  }

  void test_types_description()
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test_types_description 1");
    BOOST_CHECK(yayi::type_description::type_desc<yaINT8>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<yaINT8>::scalar == yayi::type::s_i8);
    BOOST_CHECK(yayi::type_description::type_desc<yaINT8>::name() == std::string("yaINT8"));
    BOOST_CHECK_NO_THROW(yayi::type_description::type_desc<yaINT8>());

    BOOST_CHECK(yayi::type_description::type_desc<yaUINT8>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<yaUINT8>::scalar == yayi::type::s_ui8);
    BOOST_CHECK(yayi::type_description::type_desc<yaUINT8>::name() == std::string("yaUINT8"));
    BOOST_CHECK_NO_THROW(yayi::type_description::type_desc<yaUINT8>());

    BOOST_CHECK(yayi::type_description::type_desc<yaF_double>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<yaF_double>::scalar == yayi::type::s_double);
    BOOST_CHECK(yayi::type_description::type_desc<yaF_double>::name() == std::string("yaF_double"));
    BOOST_CHECK_NO_THROW(yayi::type_description::type_desc<yaF_double>());

    typedef std::vector<yaUINT8> vector_type;
    BOOST_CHECK(!yayi::type_description::type_desc<vector_type>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<vector_type>::scalar == yayi::type::s_ui8);
    BOOST_CHECK(yayi::type_description::type_desc<vector_type>::compound == yayi::type::c_vector);
    BOOST_CHECK(yayi::type_description::type_desc<vector_type>::name() == std::string("vector<yaUINT8>"));

    /* //should yield a compiler error
    typedef std::complex<yaUINT8> false_complex_type;
    BOOST_CHECK(!yayi::type_description::type_desc<false_complex_type>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<false_complex_type>::scalar == yayi::type::s_ui8);
    BOOST_CHECK(yayi::type_description::type_desc<false_complex_type>::compound == yayi::type::c_complex);
    BOOST_CHECK(yayi::type_description::type_desc<false_complex_type>::name() == std::string("complex<yaUINT8>"));
    */
    typedef std::complex<yaF_simple> complex_type;
    BOOST_CHECK(!yayi::type_description::type_desc<complex_type>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<complex_type>::scalar == yayi::type::s_float);
    BOOST_CHECK(yayi::type_description::type_desc<complex_type>::compound == yayi::type::c_complex);
    BOOST_CHECK(yayi::type_description::type_desc<complex_type>::name() == std::string("complex<yaF_simple>"));


    typedef std::map<yaUINT8, std::vector<yaF_double> > map_type;
    BOOST_CHECK(!yayi::type_description::type_desc<map_type>::is_pod::value);
    BOOST_CHECK(yayi::type_description::type_desc<map_type>::scalar == yayi::type::s_object);
    BOOST_CHECK(yayi::type_description::type_desc<map_type>::compound == yayi::type::c_map);
    BOOST_CHECK_MESSAGE(yayi::type_description::type_desc<map_type>::name() == "map<yaUINT8, vector<yaF_double>>",
      yayi::type_description::type_desc<map_type>::name() << " != " << "map<yaUINT8, vector<yaF_double>>");




#ifndef YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
    typedef s_dummy unsupported_type;
    BOOST_CHECK_THROW(yayi::type_description::type_desc<unsupported_type>(), yayi::errors::yaException);
    BOOST_CHECK(yayi::type_description::type_desc<unsupported_type>::scalar == type::s_undefined);
#endif



  }


  void test_types_transforms()
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test_types_transforms 1");
    variant test_var;
    test_var.element.ui8_value  = 10;
    test_var.element_type.s_type= type_support<yaUINT8>::scalar;
    test_var.element_type.c_type= type_support<yaUINT8>::compound;
    BOOST_CHECK(test_var.element_type.c_type == yayi::type::c_scalar);

    BOOST_CHECKPOINT("test_types_transforms 2");
    variant test_var2 = test_var;
    BOOST_CHECK(test_var.element_type == test_var2.element_type);
    BOOST_CHECK(test_var.element.ui8_value == test_var2.element.ui8_value);

    BOOST_CHECKPOINT("test_types_transforms 3");
    variant test_var3 = (yaUINT8)10;
    
    BOOST_CHECKPOINT("test_types_transforms 4");
    yaF_simple f = test_var3;
    BOOST_CHECK(abs(f - 10.f) < 1.0E-10);
    
    BOOST_CHECKPOINT("test_types_transforms 5 : yaUINT16->yaF_simple");
    test_var3 = (yaUINT16)1000;
    BOOST_CHECKPOINT("test_types_transforms 6 : yaUINT16->yaF_simple");
    f = test_var3;
    BOOST_CHECK_CLOSE(f, 1000.f, 1E-8);


    std::vector<yaF_double> vect;
    for(int i = 0; i < 10; i++)
      vect.push_back(5-i);

    BOOST_CHECKPOINT("test_types_transforms 7: vectors (1)");
    variant *test_var4 = new variant(vect);
    variant &test_var4ref = *test_var4;
    variant test_var4_bis = *test_var4;

    BOOST_CHECKPOINT("test_types_transforms 8: vectors (2)");
    std::vector<yaINT8> vect2 = test_var4ref;
    for(int i = 0; i < 10; i++)
    {
      BOOST_CHECK(vect[i] == vect2[i]);
    }

    delete test_var4;


    BOOST_CHECKPOINT("test_types_transforms 9: pairs");
    std::pair<yaF_simple, yaUINT16> pa(0.5f, 2000);
    variant test_var5 = pa;
    std::pair<yaF_double, yaUINT32> pb = test_var5;
    BOOST_CHECK(pa.first == pb.first);
    BOOST_CHECK(pa.second == pb.second);

    
    // variant cleanup/copy tests
    BOOST_CHECK_NO_THROW(test_var4_bis = test_var5);
    variant test_var5_bis;
    BOOST_CHECK_NO_THROW(test_var5_bis = test_var5);
    
    BOOST_CHECKPOINT("test_types_transforms 9: string type");
    test_var5 = string_type("titi");
    BOOST_CHECK(test_var5.operator string_type() == "titi");
    BOOST_CHECK_NO_THROW(test_var4_bis = test_var5);


#ifndef YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
    BOOST_CHECK_THROW(test_var3 = (int)100);
#endif

    BOOST_CHECKPOINT("test_types_transforms 10 (complex)");
    test_var = std::complex<double>(4., 3.);
    BOOST_CHECKPOINT("test_types_transforms 10 (complex2)");
    std::complex<float> com_test = test_var;
    BOOST_CHECK_CLOSE(std::real(com_test), 4.f, 1E-8);
    BOOST_CHECK_CLOSE(std::imag(com_test), 3.f, 1E-8);
    
    
    BOOST_CHECKPOINT("test_types_transforms 11 (pixel_4)");
    s_compound_pixel_t<yaUINT32, mpl::int_<4> > test_pix(5);
    test_pix[2] = 3;
    
    BOOST_CHECKPOINT("test_types_transforms 11 (pixel_4-2)");
    test_var4_bis = test_pix;
    BOOST_CHECKPOINT("test_types_transforms 11 (pixel_4-3)");
    test_var5 = test_pix;
    BOOST_CHECKPOINT("test_types_transforms 11 (pixel_4-4)");
    s_compound_pixel_t<yaUINT32, mpl::int_<4> > test_pix2, test_pix3 = test_var5;
    BOOST_CHECK_THROW(test_pix2 = test_var, errors::yaException);
    test_pix2 = test_var4_bis;
    
    BOOST_CHECK(test_pix == test_pix2);
    BOOST_CHECK(test_pix == test_pix3);
    
    variant test_var6 = std::string("blablabl");
    std::string ss = test_var6.operator std::string();
    BOOST_CHECK(ss == "blablabl");
    test_var5 = test_var6;
    BOOST_CHECK(test_var5.operator std::string() == "blablabl");

  }
  
  void test_types_transforms_map()
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test_types_transforms_map 1");

    std::map<yaF_double, yaUINT8> map;
    for(int i = 0; i < 10; i++)
      map.insert(std::make_pair(5-i, i + 10));

    BOOST_CHECKPOINT("test_types_transforms_map 2");
    variant test_var(map);

    BOOST_CHECKPOINT("test_types_transforms_map 3");
    std::map<yaF_double, yaUINT8> map2 = test_var;
    for(int i = 0; i < 10; i++)
    {
      BOOST_CHECK(map[5-i] == map2[5-i]);
    }
    BOOST_CHECK(map2.size() == 10);

    BOOST_CHECKPOINT("test_types_transforms_map 3");
    std::map<yaF_simple, yaUINT8> map3 = test_var;
    for(int i = 0; i < 10; i++)
    {
      BOOST_CHECK(map[5-i] == map3[float(5-i)]);
    }
    BOOST_CHECK(map3.size() == 10);
    
    

  }
  
  void test_types_transforms_coordinates()
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test_types_transforms_coordinates 1");

    s_coordinate<2> c(c2D(5, 6));
    variant test_var(c);
    s_coordinate<2> c_test = test_var;
    
    BOOST_CHECK_MESSAGE(c == c_test, "Points are different left (theory) = " << c << " right (test) = " << c_test);

  }  
  
  
  void test_types_pixel_types()
  {
    using namespace yayi;
    typedef s_compound_pixel_t<yaUINT32, mpl::int_<5> > pix_5_t;
    BOOST_CHECK(pix_5_t::dimension::value == 5);
    
    pix_5_t v1, v2;
    
    v1[0] = v2[0] = 1;
    v1[1] = v2[1] = 2;    
    v1[2] = v2[2] = 3;
    v1[3] = v2[3] = 3;
    v1[4] = v2[4] = 3;    
    
    
    // Comparisons
    BOOST_CHECK(v1 == v2);
    BOOST_CHECK(!(v1 != v2));
    
    v2[2] = 4;
    BOOST_CHECK(v1 != v2);
    BOOST_CHECK(!(v1 == v2));

    v1 = v2;
    BOOST_CHECK(v1 == v2); 

#ifndef NDEBUG
    BOOST_CHECK_THROW(v2[7], errors::yaException);
#endif

    pix_5_t v3(v2);
    BOOST_CHECK(v3 == v2);
    
   

    // copy constructor
    pix_5_t v4(v2);
    BOOST_CHECK(v4 == v2);
    
    
    s_compound_pixel_t<yaUINT64, mpl::int_<5> > pp(v2);
    
    BOOST_CHECK(pp == v2);

  }

  
  
};

void register_types_and_variant_lifetime_test(test_suite*& test)
{
  boost::shared_ptr<types_and_variant_test> instance( new types_and_variant_test );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_class,        instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_description,  instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_transforms,   instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_transforms_map, instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_pixel_types,  instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_basic_types_size,   instance ) );
  test->add( BOOST_CLASS_TEST_CASE( &types_and_variant_test::test_types_transforms_coordinates, instance ) );


}

