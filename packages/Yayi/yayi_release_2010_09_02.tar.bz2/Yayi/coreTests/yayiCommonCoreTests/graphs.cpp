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


#include <Yayi/core/yayiCommon/include/common_graph.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>

void test_graph1()
{
  BOOST_CHECKPOINT("test_graph1");
  typedef yayi::s_graph<int, float> graph_t;
  graph_t g;
  
  graph_t::vertex_descriptor vd1 = g.add_vertex(32);
  BOOST_CHECK(g.vertex_data(vd1) == 32);
  
  graph_t::vertex_descriptor vd2 = g.add_vertex();
  BOOST_CHECK(g.vertex_data(vd2) == int());
  
  BOOST_CHECK(g.num_vertices() == 2);
  graph_t::edge_descriptor ed1 = g.add_edge(vd1, vd2, 5.5);
  BOOST_CHECK_CLOSE(g.edge_data(ed1), 5.5f, 1E-8f);
  
  BOOST_CHECK(g.num_edges() == 1);
  BOOST_CHECK(!graph_t::is_directed());

  BOOST_CHECK(g.num_adjacent_vertices(vd1) == 1);
  BOOST_CHECK(g.num_adjacent_vertices(vd2) == 1);


  std::stringstream s;
  
  BOOST_CHECKPOINT("write graph");
  write_graph(s, g, "name", "weight");
  
  std::string ss(s.str());
  std::cout << ss << std::endl;
  
  std::istringstream is(ss);//is("graph G { 0[name=\"32\"]; 1[name=\"0\"]; 0--1 [weight=\"5.5\"]; }");
  
  BOOST_CHECKPOINT("read graph");
  graph_t gp;
  read_graph(is, gp);
  BOOST_CHECK(gp.num_vertices() == 2);
  BOOST_CHECK(gp.num_edges() == 1);


}


void test_graph2()
{
  BOOST_CHECKPOINT("test_graph2");
  typedef yayi::s_graph<yayi::variant, yayi::variant> graph_t;
  graph_t g;
  
  BOOST_CHECKPOINT("test_graph2 : add_vertex");
  graph_t::vertex_descriptor vd1 = g.add_vertex(yayi::yaUINT8(32));
  BOOST_CHECKPOINT("test_graph2 : add_vertex - read");
  BOOST_CHECK((yayi::yaUINT32)g.vertex_data(vd1) == 32);
  
  BOOST_CHECKPOINT("test_graph2 : add_vertex (2)");
  graph_t::vertex_descriptor vd2 = g.add_vertex();
  BOOST_CHECK(g.vertex_data(vd2).element_type == yayi::variant().element_type);
  
  BOOST_CHECK(g.num_vertices() == 2);
  graph_t::edge_descriptor ed1 = g.add_edge(vd1, vd2, 5.5);
  BOOST_CHECK_CLOSE((float)g.edge_data(ed1), 5.5f, 1E-8f);

  BOOST_CHECKPOINT("test_graph2 : add_vertex (3)");
  graph_t::vertex_descriptor vd3 = g.add_vertex(std::string("toto1"));
  std::string ss = /*(yayi::string_type)*/g.vertex_data(vd3).operator yayi::string_type();
  BOOST_CHECK(ss == std::string("toto1"));

  
  BOOST_CHECK(g.num_edges() == 1);
  BOOST_CHECK(!graph_t::is_directed());

}



void register_graph_test(test_suite*& test)
{
  test->add( BOOST_TEST_CASE( &test_graph1 )    );
  test->add( BOOST_TEST_CASE( &test_graph2 )    );    
}
