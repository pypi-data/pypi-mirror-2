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
#include <Yayi/core/yayiReconstruction/include/morphological_leveling_t.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

void test_leveling_simple() {
  using namespace yayi;
  BOOST_CHECKPOINT("test_leveling_simple");
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_mark, /*im_test,*/ im_out;
  image_type* p_im[] = {&im_in, /*&im_test,*/ &im_out, &im_mark};
  image_type::coordinate_type coord;
  coord[0] = 10; coord[1] = 10;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input mask image
  {
    static const std::string s = 
      "3  2 3  2 5 6 7 9 7 9 "
      "3  2 3  2 6 6 7 9 7 9 "
      "3  2 2  2 5 6 7 9 7 9 "
      "3  2 3  2 5 6 7 9 7 9 "
      "3  2 3  2 5 6 7 9 7 9 "
      "8 10 8 10 8 4 3 4 3 4 "
      "8 10 8 10 8 4 3 4 3 4 "
      "8 10 8 10 8 4 3 4 3 4 "
      "8 10 8 10 8 4 3 4 3 4 "
      "8 10 8 10 8 4 3 4 3 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // input mark image
  {
    static const std::string s = 
      /*" 4  4  4  4 4 5 3 3 3 3 "
      " 4  4  4  4 4 6 6 5 3 3 "
      " 4  4  3  4 4 3 3 3 3 3 "
      " 4  4  4  4 4 5 3 3 3 3 "
      " 4  4  4  4 4 3 3 3 3 3 "
      " 7  6  7  6 8 4 3 4 3 4 "
      " 7 11 12 10 8 4 3 4 3 4 "
      "11  7 11 10 8 4 3 4 3 4 "
      "11 10  7 10 8 4 3 4 3 4 "
      "11 10  7  7 8 4 3 4 3 4 "*/
      " 4  4  4  4 4 5 3 3 3 3 "
      " 4  4  4  4 4 6 6 5 3 3 "
      " 4  4  3  4 4 3 3 3 3 3 "
      " 4  4  4  4 4 5 3 3 3 3 "
      " 4  4  4  4 4 3 3 3 3 3 "
      " 7  6  7  6 8 4 3 4 3 4 "
      " 7 11  8 10 8 4 3 4 3 4 "
      " 8  7  9 10 8 4 3 4 3 4 "
      " 8 10  7 10 8 4 3 4 3 4 "
      " 8 10  7  7 8 4 3 4 3 4 "      
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mark, "Error during the input streaming of the image");
  }


#if 0
  // output test image
  {
    static const std::string s = 
      /*" 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 6 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 7  7  7  7 8 4 3 4 3 4 "
      " 7 11 11 10 8 4 3 4 3 4 "
      "11  7 11 10 8 4 3 4 3 4 "
      "11 10  7 10 8 4 3 4 3 4 "
      "11 10  7  7 8 4 3 4 3 4 "*/

      " 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 6 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 3  3  3  3 5 6 6 6 6 6 "
      " 7  7  7  7 8 4 3 4 3 4 "
      " 7 10  8 10 8 4 3 4 3 4 "
      " 8  7  9 10 8 4 3 4 3 4 "
      " 8 10  7 10 8 4 3 4 3 4 "
      " 8 10  7  7 8 4 3 4 3 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }
#endif

  BOOST_CHECKPOINT("test_leveling_simple: lev");
  reconstructions::s_generic_leveling_by_double_reconstruction<image_type> lev; 
  BOOST_CHECKPOINT("test_leveling_simple: lev call");
  yaRC res = lev(im_mark, im_in, se::SESquare2D, im_out);
  BOOST_CHECKPOINT("test_leveling_simple: lev ret");
  BOOST_REQUIRE(res == yaRC_ok);
  
  /*for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }*/
  
  
  typedef se::s_neighborlist_se< image_type::coordinate_type > se_t;
  typedef se::s_runtime_neighborhood<image_type const, se_t> neighborhood_t;
  neighborhood_t neighbor(im_out, se::SESquare2D.remove_center());
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) 
  {
    BOOST_CHECK(neighbor.center(i) == yaRC_ok);
    image_type::pixel_type pix_center = im_out.pixel(i);
    
    for(neighborhood_t::const_iterator itn(neighbor.begin()), itne(neighbor.end()); itn != itne; ++itn) 
    {
      // from definition 2 of "Morphological Scale-Space Representation with Levelings", Meyer & Paragos, LNCS 1682 (1999).
      if(*itn < pix_center)
      {

        BOOST_CHECK_MESSAGE(
          im_in.pixel(i) >= im_out.pixel(i), 
          "Leveling error condition 1 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
        
        BOOST_CHECK_MESSAGE(
          im_in.pixel(itn.Offset()) <= im_out.pixel(itn.Offset()), 
          "Leveling error condition 2 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << " and neighbor " << from_offset_to_coordinate(coord, itn.Offset()) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(itn.Offset()) << " !(<=) " << (int)im_out.pixel(itn.Offset()));

      }

    }

    
    //BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
  

}


void test_leveling_simple_1D() {
  using namespace yayi;
  BOOST_CHECKPOINT("test_leveling_simple_1D");
  
  typedef Image<yaUINT8, s_coordinate<1> > image_type;
  
  image_type im_in, im_mark, /*im_test,*/ im_out;
  image_type* p_im[] = {&im_in, /*&im_test,*/ &im_out, &im_mark};
  image_type::coordinate_type coord;
  coord[0] = 11; 
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input mask image
  {
    static const std::string s = 
      "15 12 13  9  7  5  6  7  9  8  9 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // input mark image
  {
    static const std::string s = 
    //"15 12 13  9  7  5  6  7  9  8  9 "
      " 8 10  8  8  8  7  6  8  4  5  2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mark, "Error during the input streaming of the image");
  }

#if 0
  // output test image
  {
    static const std::string s = 
    //"15 12 13  9  7  5  6  7  9  8  9 "
    //" 8 10  8  8  8  7  6  8  4  5  2 "
      "10 10 10  9  7  6  6  7  8  8  8 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }
#endif


  BOOST_CHECKPOINT("test_leveling_simple: lev");
  reconstructions::s_generic_leveling_by_double_reconstruction<image_type> lev; 
  BOOST_CHECKPOINT("test_leveling_simple: lev call");
  yaRC res = lev(im_mark, im_in, se::SESegmentX1D, im_out);
  BOOST_CHECKPOINT("test_leveling_simple: lev ret");
  BOOST_REQUIRE(res == yaRC_ok);
  
  //for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
  //  BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  //}

  #if 0
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    if(i < 9 && im_out.pixel(i) > im_out.pixel(i+1))
    {
      // i+1 = q, i = p
      BOOST_CHECK_MESSAGE(im_in.pixel(i) >= im_out.pixel(i), "Leveling error condition 1 on pixel " << i << " position " << from_offset_to_coordinate(coord, i)[0] << "\n\tbad transition left-to-right - mask/out : " << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
      BOOST_CHECK_MESSAGE(im_out.pixel(i+1) >= im_in.pixel(i+1), "Leveling error condition 2 on pixel " << i << " position " << from_offset_to_coordinate(coord, i)[0] << "\n\tbad transition left-to-right - out/mask: " << (int)im_out.pixel(i+1) << " !(>=) " << (int)im_in.pixel(i+1));
    }
    if(i > 0 && im_out.pixel(i) > im_out.pixel(i-1))
    {
      // i-1= q, i = p
      BOOST_CHECK_MESSAGE(im_in.pixel(i) >= im_out.pixel(i), "Leveling error condition 1 on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tbad transition right-to-left - mask/out : " << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
      BOOST_CHECK_MESSAGE(im_out.pixel(i-1) >= im_in.pixel(i-1), "Leveling error condition 2 on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tbad transition right-to-left - mask/out : " << (int)im_out.pixel(i+1) << " !(>=) " << (int)im_in.pixel(i+1));
    }
    //BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
  #endif
  
  typedef se::s_neighborlist_se< image_type::coordinate_type > se_t;
  typedef se::s_runtime_neighborhood<image_type const, se_t> neighborhood_t;
  neighborhood_t neighbor(im_out, se::SESegmentX1D.remove_center());
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) 
  {
    BOOST_CHECK(neighbor.center(i) == yaRC_ok);
    image_type::pixel_type pix_center = im_out.pixel(i);
    
    for(neighborhood_t::const_iterator itn(neighbor.begin()), itne(neighbor.end()); itn != itne; ++itn) 
    {
      // from definition 2 of "Morphological Scale-Space Representation with Levelings", Meyer & Paragos, LNCS 1682 (1999).
      if(*itn < pix_center)
      {

        BOOST_CHECK_MESSAGE(
          im_in.pixel(i) >= im_out.pixel(i), 
          "Leveling error condition 1 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
        
        BOOST_CHECK_MESSAGE(
          im_in.pixel(itn.Offset()) <= im_out.pixel(itn.Offset()), 
          "Leveling error condition 2 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << " and neighbor " << from_offset_to_coordinate(coord, itn.Offset()) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(itn.Offset()) << " !(<=) " << (int)im_out.pixel(itn.Offset()));

      }

    }

    
    //BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }  

}

void test_leveling_pathological_1D() {
  using namespace yayi;
  BOOST_CHECKPOINT("test_leveling_pathological_1D");
  
  typedef Image<yaUINT8, s_coordinate<1> > image_type;
  
  image_type im_in, im_mark/*, im_test*/, im_out;
  image_type* p_im[] = {&im_in/*, &im_test*/, &im_out, &im_mark};
  image_type::coordinate_type coord;
  coord[0] = 11;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  // input mask image
  {
    static const std::string s = 
      "15 12 13  9  7  5  6  7  9  8  9 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // input mark image
  {
    static const std::string s = 
    //"15 12 13  9  7  5  6  7  9  8  9 "
      " 8 10  8 16 17 16 14  8  4  5  2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mark, "Error during the input streaming of the image");
  }

#if 0
  // output test image
  {
    static const std::string s = 
    //"15 12 13  9  7  5  6  7  9  8  9 "
    //" 8 10  8 16 17 16 14  8  4  5  2 "
      "10 10 10  9  9  9  9  9  5  5  5 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }
#endif


  BOOST_CHECKPOINT("test_leveling_simple: lev");
  reconstructions::s_generic_leveling_by_double_reconstruction<image_type> lev; 
  BOOST_CHECKPOINT("test_leveling_simple: lev call");
  yaRC res = lev(im_mark, im_in, se::SESegmentX1D, im_out);
  BOOST_CHECKPOINT("test_leveling_simple: lev ret");
  BOOST_REQUIRE(res == yaRC_ok);
  
  //for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
  //  BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  //}
#if 0
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    if(i < 9 && im_out.pixel(i) > im_out.pixel(i+1))
    {
      // i+1 = q, i = p
      BOOST_CHECK_MESSAGE(im_in.pixel(i) >= im_out.pixel(i), "Leveling error condition 1 on pixel " << i << " position " << from_offset_to_coordinate(coord, i)[0] << "\n\tbad transition left-to-right - mask/out : " << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
      BOOST_CHECK_MESSAGE(im_out.pixel(i+1) >= im_in.pixel(i+1), "Leveling error condition 2 on pixel " << i << " position " << from_offset_to_coordinate(coord, i)[0] << "\n\tbad transition left-to-right - out/mask: " << (int)im_out.pixel(i+1) << " !(>=) " << (int)im_in.pixel(i+1));
    }
    if(i > 0 && im_out.pixel(i) > im_out.pixel(i-1))
    {
      // i-1= q, i = p
      BOOST_CHECK_MESSAGE(im_in.pixel(i) >= im_out.pixel(i), "Leveling error condition 1 on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tbad transition right-to-left - mask/out : " << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
      BOOST_CHECK_MESSAGE(im_out.pixel(i-1) >= im_in.pixel(i-1), "Leveling error condition 2 on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tbad transition right-to-left - mask/out : " << (int)im_out.pixel(i+1) << " !(>=) " << (int)im_in.pixel(i+1));
    }
    //BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
#endif

  typedef se::s_neighborlist_se< image_type::coordinate_type > se_t;
  typedef se::s_runtime_neighborhood<image_type const, se_t> neighborhood_t;
  neighborhood_t neighbor(im_out, se::SESegmentX1D.remove_center());
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) 
  {
    BOOST_CHECK(neighbor.center(i) == yaRC_ok);
    image_type::pixel_type pix_center = im_out.pixel(i);
    
    for(neighborhood_t::const_iterator itn(neighbor.begin()), itne(neighbor.end()); itn != itne; ++itn) 
    {
      // from definition 2 of "Morphological Scale-Space Representation with Levelings", Meyer & Paragos, LNCS 1682 (1999).
      if(*itn < pix_center)
      {

        BOOST_CHECK_MESSAGE(
          im_in.pixel(i) >= im_out.pixel(i), 
          "Leveling error condition 1 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(i) << " !(>=) " << (int)im_out.pixel(i));
        
        BOOST_CHECK_MESSAGE(
          im_in.pixel(itn.Offset()) <= im_out.pixel(itn.Offset()), 
          "Leveling error condition 2 on pixel " << i << " position " 
            << from_offset_to_coordinate(coord, i) 
            << " and neighbor " << from_offset_to_coordinate(coord, itn.Offset()) 
            << "\n\tbad transition left-to-right - mask/out : " 
            << (int)im_in.pixel(itn.Offset()) << " !(<=) " << (int)im_out.pixel(itn.Offset()));

      }

    }

    
    //BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Leveling error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  } 
}


void register_leveling_tests(test_suite*& test) 
{
  test->add( BOOST_TEST_CASE(&test_leveling_simple) );
  test->add( BOOST_TEST_CASE(&test_leveling_simple_1D) );
  test->add( BOOST_TEST_CASE(&test_leveling_pathological_1D) );
}
