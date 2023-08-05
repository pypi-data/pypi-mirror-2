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

#include <Yayi/core/yayiCommon/common_priority_queues.hpp>

void test_priority_queue_begin() {
  BOOST_CHECKPOINT("Priority queue test begin");
}

void test_priority_queue_end() {
  BOOST_CHECKPOINT("Priority queue test begin");
}

void test_priority_queue_generic() {
  
  typedef yayi::priority_queue_t<int, int> pq_t;
  pq_t pq;
  for(int i = 0; i < 100; i++)
  {
    pq.insert(i/10, i);
  }
  
  BOOST_CHECK(pq.size() == 100);
  BOOST_CHECK(pq.number_keys() == 10);
  BOOST_CHECK(pq.min_key() == 0);
  BOOST_CHECK(!pq.empty());
  
  int count = 10;
  for(pq_t::plateau_const_iterator_type it(pq.begin_top_plateau()), ite(pq.begin_top_plateau()); it != ite; ++it)
  {
    BOOST_CHECK(it.key() == 0);
    BOOST_CHECK(*it == count++);
  }
  BOOST_CHECK(count == 10);
  
}


void register_priority_queue_test(test_suite*& test)
{

  test->add( BOOST_TEST_CASE( &test_priority_queue_begin )    );
  test->add( BOOST_TEST_CASE( &test_priority_queue_generic )  );
  test->add( BOOST_TEST_CASE( &test_priority_queue_end )      );
    
}

