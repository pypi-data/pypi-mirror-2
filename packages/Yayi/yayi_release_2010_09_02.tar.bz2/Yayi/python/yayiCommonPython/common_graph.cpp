/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiCommonPython/common_python.hpp>
#include <Yayi/core/yayiCommon/include/common_graph.hpp>
#include <boost/python/copy_const_reference.hpp>

bool is_directed_wrap(const yayi::IGraph* g)
{
  return yayi::IGraph::is_directed();
}


#if 0
void add_edge_wrap(yayi::IGraph* g, const yayi::IGraph::vertex_descriptor u, const yayi::IGraph::vertex_descriptor v, const yayi::IGraph::edge_data_t& data)
{
  g->add_edge(u, v, data);
}

const yayi::IGraph::edge_data_t& edge_data_wrap(const yayi::IGraph* g, const yayi::IGraph::vertex_descriptor u, const yayi::IGraph::vertex_descriptor v)
{
  return g->edge_data(u, v);
}
void set_edge_data_wrap(yayi::IGraph* g, const yayi::IGraph::vertex_descriptor u, const yayi::IGraph::vertex_descriptor v, const yayi::IGraph::edge_data_t& data)
{
  g->set_edge_data(u, v, data);
}
#endif

void declare_graph() {

  using namespace yayi;

  boost::python::class_<IGraph::edge_descriptor>("Edge", "An edge structure with no property (for manipulation ease)", bpy::no_init);

  boost::python::class_<IGraph>("Graph", "A generic graph structure that can be converted into a Yayi suitable format without parallel edges")
  .def(boost::python::init<>())
  .def(boost::python::init<IGraph>())
  .def("num_vertices",  &IGraph::num_vertices,  "number of vertices (nodes) of the graph.")
  .def("num_edges",     &IGraph::num_edges,     "number of edges of the graph.")
  .def("clear",         &IGraph::clear,         "removes all edges, vertices and their associated data from the graph.")

  .def("add_vertex",    &IGraph::add_vertex,    "adds a vertex to the graph, returns its index.")
  .def("add_edge",      &IGraph::add_edge,      "adds an edge between vertices v1 and v2.")

  .def("remove_edge",
       (void (IGraph::*)(IGraph::vertex_descriptor, IGraph::vertex_descriptor))&IGraph::remove_edge,
       "removes an edge between vertices v1 and v2.")

  .def("remove_edge",
       (void (IGraph::*)(IGraph::edge_descriptor))&IGraph::remove_edge,
       "removes an edge by its descriptor.")

  .def( "get_edge",
        &IGraph::get_edge,
        "returns the edge connecting the two vertices")
        
  .def( "num_adjacent_vertices",
        &IGraph::num_adjacent_vertices,
        "returns the number of adjacent vertice to the provided vertex")

  .def( "are_vertices_adjacent",	
        &IGraph::are_vertices_adjacent,
        "returns whether there is an edge between two vertices (or nodes) without considering any directed property")

  // This does not work with python 2.6.3
  //.add_static_property("is_directed", &IGraph::is_directed, "returns whether the graph is directed")
  .add_property("is_directed",  &is_directed_wrap, "returns whether the graph is directed (currently only undirected)")


  //.add_property("edge_data",
  //  bpy::make_function(&IGraph::edge_data, bpy::return_value_policy<bpy::copy_const_reference>()), 
  //  &IGraph::set_edge_data)
  // @TODO overload this to get the two type of access to the edges
  .def("get_edge_data",     (const IGraph::edge_data_t& (IGraph::*)(const IGraph::edge_descriptor) const)&IGraph::edge_data,     "returns the data associated to the argument edge", bpy::return_value_policy<bpy::copy_const_reference>())
  .def("set_edge_data",     (void (IGraph::*)(const IGraph::edge_descriptor, const IGraph::edge_data_t&))&IGraph::set_edge_data, "sets the data associated to the argument edge")

  //.add_property("vertex_data",  &IGraph::vertex_data, &IGraph::set_vertex_data)
  // this compiles but does not work at all :))
  //.add_property("vertex_data",
  //  bpy::make_function(&IGraph::vertex_data, bpy::return_value_policy<bpy::copy_const_reference>()), 
  //  &IGraph::set_edge_data)  
  .def("get_vertex_data",   &IGraph::vertex_data,     "returns the data associated by the argument vertex", bpy::return_value_policy<bpy::copy_const_reference>())
  .def("set_vertex_data",   &IGraph::set_vertex_data, "set the data associated by the argument vertex")

  ;
}
