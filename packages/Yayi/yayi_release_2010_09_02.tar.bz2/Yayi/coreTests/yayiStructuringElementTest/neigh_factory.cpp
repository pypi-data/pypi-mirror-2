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
#include "Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp"
#include "Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp"
#include "Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp"
#include "Yayi/core/yayiIO/include/yayi_IO.hpp"

#include <Yayi/coreTests/yayiCommonCoreTests/data_path_for_tests.hpp>
using namespace yayi;
using namespace yayi::se;

class neigh_factory_test {
public:

  void test_basics() {
  
    std::string im_file_name(get_data_from_data_path("release-grosse bouche.jpg"));
    BOOST_TEST_MESSAGE("Reading the image " + im_file_name);  
    
    IImage *im = 0;
    yaRC res = yayi::IO::readJPG(im_file_name, im);
    BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "An error occured while reading the image " << im_file_name << " error follows \n" << res);
    
    IConstNeighborhood* neigh = IConstNeighborhood::Create(*im, /*(IStructuringElement*)*/ SEHex2D);
    BOOST_CHECK_MESSAGE(neigh, "Combination not supported imin " << im->Description() << " se " << SEHex2D.Description());
    if(neigh) delete neigh;
    delete im;
  }

public:
  static void register_tests(test_suite*& test) {
    boost::shared_ptr<neigh_factory_test> instance( new neigh_factory_test );
    test->add( BOOST_CLASS_TEST_CASE( &neigh_factory_test::test_basics, instance ) );

  }
};


void register_neighborhood_factory_test(test_suite*& test) {  
  neigh_factory_test::register_tests(test);
}

