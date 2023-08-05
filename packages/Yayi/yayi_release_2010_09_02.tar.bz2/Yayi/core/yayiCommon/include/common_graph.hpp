/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_GRAPH_HPP__
#define YAYI_COMMON_GRAPH_HPP__

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>

#include <vector>
#include <boost/config.hpp>

#include <boost/version.hpp> 
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
// should be replaced by <boost/property_map/property_map.hpp> and <boost/property_map/dynamic_property_map.hpp> starting from boost 1.40
#if ( (((BOOST_VERSION  / 100) % 1000) >= 40) && ((BOOST_VERSION /  100000) >= 1) )
  #include <boost/property_map/property_map.hpp>
  #include <boost/property_map/dynamic_property_map.hpp>
#else
  #include <boost/property_map.hpp>
  #include <boost/dynamic_property_map.hpp>
#endif

#include <boost/graph/properties.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/graph_utility.hpp>

namespace yayi
{

  
  struct s_empty_node {};     //! Structure for vertices with empty properties
  struct s_empty_edge {};     //! Structure for edges with empty properties

  // forward decl (needed)
  template < class V, class E, bool is_directed_ , class vertex_tag_t_, class edge_tag_t_>
  struct s_graph;

  
  namespace 
  {
    // Some helper structures
  
    template <bool b_directed>
    struct s_directed_helper
    {
      typedef boost::directedS   type;
    };
    template <>
    struct s_directed_helper<false>
    {
      typedef boost::undirectedS type;
    };
    
    //! Helper class for graph vertices
    template <class TAG, class VV>
    struct s_vertex_prop_helper                     
    {
      typedef boost::property<TAG, VV> type;
      
      template <class GG, class vertex_descriptor>
      void operator()(GG& g, vertex_descriptor vd, const VV& value) const
      {
        boost::put(TAG(), g, vd, value);
      }
    };
    
    template <class TAG>
    struct s_vertex_prop_helper<TAG, s_empty_node>
    {
      typedef boost::no_property type;
      template <class GG, class vertex_descriptor>
      void operator()(GG& , vertex_descriptor , const s_empty_node&) const
      {
      }
    };

    template <class TAG, class EE>
    struct s_edge_prop_helper
    {
      typedef boost::property<TAG, EE>     type;
      template <class GG, class edge_descriptor>
      void operator()(GG& g, edge_descriptor ed, const EE& value) const
      {
        boost::put(TAG(), g, ed, value);
      }
      template <class GG, class edge_descriptor>
      EE const& get_edge_data(GG& g, edge_descriptor ed) const
      {
        return boost::get(TAG(), g, ed);;
      }
      template <class GG, class edge_descriptor>
      EE & get_edge_data(GG& g, edge_descriptor ed)
      {
        return boost::get(TAG(), g, ed);;
      }
    };
    
    template <class TAG>
    struct s_edge_prop_helper<TAG, s_empty_edge>
    {
      typedef boost::no_property           type;
      template <class GG, class edge_descriptor>
      void operator()(GG& , edge_descriptor , const s_empty_edge& ) const
      {
      }
      template <class GG, class edge_descriptor>
      s_empty_edge const& get_edge_data(GG& , edge_descriptor ) const
      {
        static s_empty_edge const e = s_empty_edge();
        return e;
      }
      template <class GG, class edge_descriptor>
      s_empty_edge& get_edge_data(GG& , edge_descriptor )
      {
        static s_empty_edge e = s_empty_edge();
        return e;
      }
    };


    template <
      class V = s_empty_node, 
      class E = s_empty_edge,
      bool  is_directed_ = false,
      class vertex_tag_t_ = boost::vertex_name_t,
      class edge_tag_t_   = boost::edge_weight_t
    >
    struct s_graph_inner_traits_helper
    {
      typedef V vertex_data_t;
      typedef E edge_data_t;
          
      typedef vertex_tag_t_ vertex_tag_t;
      typedef edge_tag_t_   edge_tag_t;

      typedef s_vertex_prop_helper<vertex_tag_t, vertex_data_t> vertex_helper_t;
      typedef s_edge_prop_helper<edge_tag_t, edge_data_t>       edge_helper_t;
      
      typedef boost::adjacency_list<
        boost::listS, 
        boost::vecS, 
        typename s_directed_helper<is_directed_>::type, 
        typename vertex_helper_t::type, 
        typename edge_helper_t::type
      > graph_t;

      typedef typename boost::graph_traits<graph_t>::edge_descriptor        edge_descriptor;
      typedef typename boost::graph_traits<graph_t>::vertex_descriptor      vertex_descriptor;

      typedef typename boost::property_map<graph_t, vertex_tag_t>::type     vertex_property_map_type;
      typedef typename boost::property_map<graph_t, edge_tag_t>::type       edge_property_map_type;
      
      typedef typename graph_t::vertex_property_type   vertex_property_type;
      typedef typename graph_t::edge_property_type     edge_property_type;
      //typedef typename boost::graph_traits<graph_t>::edge_property_type        edge_property_type;

      
      typedef typename boost::graph_traits<graph_t>::vertex_iterator        vertex_iterator;
      typedef typename boost::graph_traits<graph_t>::adjacency_iterator     adjacency_iterator;
      typedef typename boost::graph_traits<graph_t>::edge_iterator          edge_iterator;
      
      typedef typename boost::graph_traits<graph_t>::vertices_size_type     vertices_size_type;
      typedef typename boost::graph_traits<graph_t>::edges_size_type        edges_size_type;

    };


  }







    template <class V, class E, bool is_directed_, class vertex_tag_t_, class edge_tag_t_>
    struct edge_data_interface
    {
      typedef s_graph_inner_traits_helper<V, E, is_directed_, vertex_tag_t_, edge_tag_t_> traits_t;

      typedef typename traits_t::edge_data_t edge_data_t;
      typedef typename traits_t::edge_descriptor edge_descriptor;
      typedef typename traits_t::edge_tag_t edge_tag_t;
      typedef typename traits_t::vertex_descriptor vertex_descriptor;

      typename traits_t::graph_t * G;

      //edge_data_interface(typename traits_t::graph_t &G_) : G(G_){}

      //! Returns the data associated to an edge (by the edge descriptor)
      edge_data_t const& edge_data(edge_descriptor e) const
      {
        return boost::get(edge_tag_t(), *G, e);
      }

      //! Returns the data associated to an edge (by the pair of vertices)
      edge_data_t const& edge_data(vertex_descriptor u, vertex_descriptor v) const
      {
        std::pair<edge_descriptor, bool> e = boost::edge(u, v, *G);
        DEBUG_ASSERT(e.second, "no edge connects the specified vertices");
        return edge_data(e.first);
      }

      //! Sets the data associated to an edge (identified by its edge_descriptor)
      void set_edge_data(const edge_descriptor e, const edge_data_t& data)
      {
        boost::put(edge_tag_t(), *G, e, data);
      }
      
      //! Sets the data associated to an edge (identified by a pair of vertices)
      void set_edge_data(vertex_descriptor u, vertex_descriptor v, const edge_data_t& data)
      {
        std::pair<edge_descriptor, bool> e = boost::edge(u, v, *G);
        DEBUG_ASSERT(e.second, "no edge connects the specified vertices");
        set_edge_data(e.first, data);
      }

    };

    template <class V, bool is_directed_, class vertex_tag_t_, class edge_tag_t_>
    struct edge_data_interface<V, s_empty_edge, is_directed_, vertex_tag_t_, edge_tag_t_>
    {
      typedef s_graph_inner_traits_helper<V, s_empty_edge, is_directed_, vertex_tag_t_, edge_tag_t_> traits_t;
      //edge_data_interface(typename traits_t::graph_t const &) {}
    };





  /*!@brief Template graph
   * 
   * This structure codes a graph with vertices of type V and edges of type E.
   * 
   * @author Raffi Enficiaud
   */
  template <
    class V = s_empty_node, 
    class E = s_empty_edge,
    bool  is_directed_ = false,
    class vertex_tag_t_ = boost::vertex_name_t,        //!< The tag under which the vertex properties are encored
    class edge_tag_t_   = boost::edge_weight_t           //!< The tag under which the edge properties are encoded (maybe useful for some algorithms)
  >
  struct s_graph :
    public edge_data_interface<V, E, is_directed_, vertex_tag_t_, edge_tag_t_>,
    public s_graph_inner_traits_helper<V, E, is_directed_, vertex_tag_t_, edge_tag_t_>
  {
  
  
  public:
    typedef s_graph<V, E, is_directed_, vertex_tag_t_, edge_tag_t_> this_type;
    typedef s_graph_inner_traits_helper<V, E, is_directed_, vertex_tag_t_, edge_tag_t_> traits_t;
    typedef edge_data_interface<V, E, is_directed_, vertex_tag_t_, edge_tag_t_> edge_traits_t;

    typedef typename traits_t::edge_descriptor    edge_descriptor;
    typedef typename traits_t::vertex_descriptor  vertex_descriptor;

    typedef typename traits_t::vertex_data_t vertex_data_t;
    typedef typename traits_t::edge_data_t   edge_data_t;

    typedef typename traits_t::vertex_tag_t vertex_tag_t;
    typedef typename traits_t::edge_tag_t   edge_tag_t;
    
    typedef typename traits_t::vertices_size_type vertices_size_type;
    typedef typename traits_t::edges_size_type edges_size_type;
    typedef typename traits_t::vertex_iterator vertex_iterator;
    typedef typename traits_t::edge_iterator edge_iterator;
    typedef typename traits_t::adjacency_iterator adjacency_iterator;

    typedef typename traits_t::vertex_property_map_type vertex_property_map_type;
    typedef typename traits_t::edge_property_map_type edge_property_map_type;
    
    typename traits_t::edge_helper_t   edge_helper;
    typename traits_t::vertex_helper_t vertex_helper;

    //! The graph type
    typedef typename traits_t::graph_t graph_t;
    

    graph_t G;

    //! Sets the number of vertices in the graph
    //! Removes the first elements of the graph if the required size is bigger than the actual number of vertices.
    //! Adds vertices with default values otherwise.
    void set_number_vertices(vertices_size_type s)
    {
      vertices_size_type ss = num_vertices();
      if(s == ss)
        return;
      
      if(s < ss)
      {
        vertex_iterator vi, vi_end, next;
        boost::tie(vi, vi_end) = vertices(G);
        for (next = vi; (vi != vi_end) && (s < ss); vi = next) 
        {
          ++next;
          remove_vertex(*vi, G);
          ss--;
        }
      }
      else
      {
        while(s > ss)
        {
          add_vertex();
          ss++;
        }
      }
    }
    
    //! Returns whether the current graph is directed
    static bool is_directed() 
    {
      return is_directed_;
    }
    
    //! Clears the content of the graph
    void clear() 
    {
      G.clear();
    }
    
    template <class VV, class EE>
    this_type& operator=(const s_graph<VV, EE, is_directed_>& r_)
    {
      // copy the graph structure
      typedef s_graph<VV, EE, is_directed_> r_graph_t;
      
      G = graph_t(r_.num_vertices());
      
      // copy the properties
      std::pair<typename r_graph_t::vertex_iterator, typename r_graph_t::vertex_iterator> iters_v;
      for(boost::tie(iters_v.first, iters_v.second) = r_.vertices(); iters_v.first != iters_v.second; ++iters_v.first)
      {
        set_vertex_data(*iters_v.first, static_cast<vertex_data_t>(r_.vertex_data(*iters_v.first)));
      }

      std::pair<typename r_graph_t::edge_iterator, typename r_graph_t::edge_iterator> iters;
      for(boost::tie(iters.first, iters.second) = r_.edges(); iters.first != iters.second; ++iters.first)
      {
        add_edge(r_.source(*iters.first), r_.target(*iters.first), static_cast<edge_data_t>(r_.edge_data(*iters.first)));
      }
    
      return *this;
    }


    //! Returns a new graph with no parallel edges
    //! There is no "ordering concerning the edges so the associated properties are not garantied
    this_type remove_parallel_edges() const
    {
      // copy the graph structure
      this_type g;
      g.G = graph_t(this->num_vertices());
      
      // copy the properties
      std::pair<vertex_iterator, vertex_iterator> iters_v;
      for(boost::tie(iters_v.first, iters_v.second) = this->vertices(); iters_v.first != iters_v.second; ++iters_v.first)
      {
        g.set_vertex_data(*iters_v.first, this->vertex_data(*iters_v.first));
      }

      std::pair<edge_iterator, edge_iterator> iters;
      for(boost::tie(iters.first, iters.second) = this->edges(); iters.first != iters.second; ++iters.first)
      {
        vertex_descriptor s(this->source(*iters.first)), t(this->target(*iters.first));
        if(g.are_vertices_adjacent(s, t))
          continue;
        g.add_edge(s, t, edge_helper.get_edge_data(G, *iters.first));
      }
    
      return g;
    }


    vertex_descriptor add_vertex(const vertex_data_t& v = vertex_data_t())
    {
      vertex_descriptor vd = boost::add_vertex(G);
      vertex_helper(G, vd, v);
      return vd;
    }
    
    const vertex_data_t& vertex_data(const vertex_descriptor v) const
    {
      return boost::get(vertex_tag_t(), G, v);
    }
    

    void set_vertex_data(const vertex_descriptor v, const vertex_data_t& data)
    {
      vertex_helper(G, v, data);
    }
    
    //! Number of vertices in the graph
    vertices_size_type num_vertices() const
    {
      return boost::num_vertices(G);
    }
    
    //! Returns a pair of iterators over the vertices
    std::pair<vertex_iterator, vertex_iterator> vertices() const
    {
      return boost::vertices(G);
    }
    
    //! Returns a pair of iterators over the adjacent vertices of the input vertex u
    std::pair<adjacency_iterator, adjacency_iterator>
    adjacent_vertices(vertex_descriptor u) const
    {
      return boost::adjacent_vertices(u, G);
    }
    
    //! Returns the number of adjacent vertices connected to u
    unsigned int num_adjacent_vertices(vertex_descriptor u) const
    {
      std::pair<adjacency_iterator, adjacency_iterator> p = adjacent_vertices(u);
      return std::distance(p.first, p.second);
    }

    //! Adds an edge from u to v (or if the graph is not directed, between u and v)
    edge_descriptor add_edge(vertex_descriptor u, vertex_descriptor v, const edge_data_t& data = edge_data_t())
    {
      edge_descriptor ed = boost::add_edge(u, v, G).first;
      edge_helper(G, ed, data);
      return ed;
    }

    //! Removes an edge as well as the associated data
    void remove_edge(edge_descriptor e)
    {
      boost::remove_edge(e, G);
      return;
    }

    //! Removes an edge going from u to v (no parallel egde possible) as well as the associated data 
    void remove_edge(vertex_descriptor u, vertex_descriptor v)
    {
      boost::remove_edge(u,v, G);
      return;
    }
    
    //! Gets the edge connecting u to v
    edge_descriptor get_edge(vertex_descriptor u, vertex_descriptor v) const
    {
      std::pair<edge_descriptor, bool> e = boost::edge(u, v, G);
      DEBUG_ASSERT(e.second, "no edge connects the specified vertices");
      return e.first;
    }
    
    
    //! Returns the source vertex of an edge
    vertex_descriptor source(edge_descriptor e) const
    {
      return boost::source(e, G);
    }

    //! Returns the target vertex of an edge
    vertex_descriptor target(edge_descriptor e) const
    {
      return boost::target(e, G);
    }
    
    
    
    //! Returns true if there is an edge connecting u to v or v to u
    bool are_vertices_adjacent(vertex_descriptor u, vertex_descriptor v) const
    {
      return boost::edge(u, v, G).second || (is_directed_ && boost::edge(v, u, G).second);
    }

    
    //! Returns a pair of iterators over the edges
    std::pair<edge_iterator, edge_iterator> edges() const
    {
      return boost::edges(G);
    }
    
    //! Returns the total number of edges in the graph (may be costly)
    edges_size_type num_edges() const
    {
      return boost::num_edges(G);
    }
  };
  





  //! Generic graph for interface exchanges
  //! It would be better to replace this in order to avoid all the copies between the variants and the real data
  typedef s_graph<variant, variant> IGraph;
  
  


  //! Entry property writer for nodes
  //! The node property type should have a stringification function.
  template <class entry_property_t, class map_t>
  class entry_writer_m {
  public:
    template <class graph_t, class tag_t>
    entry_writer_m(graph_t &g, const tag_t &t = tag_t(), const std::string& txt_property_ = "name") : 
      entry_property(boost::get(tag_t(), g)), 
      txt_property(txt_property_)
    {
    }

    //! Node writer method
    template <class vertex_or_edge_desc>
    void operator()(std::ostream& out, const vertex_or_edge_desc& v) const {
      out << "[" << txt_property << "=\"" << any_to_string(entry_property[v]) << "\"]";
    }

  private:
    map_t entry_property;
    const std::string txt_property;
  };

  template <class map_t>
  class entry_writer_m<boost::no_property, map_t> {
  public:
    template <class graph_t, class tag_t>
    entry_writer_m(graph_t &g, const tag_t &t = tag_t(), const std::string& txt_property_ = "undefined")
    {}

    //! Node writer method
    template <class vertex_or_edge_desc>
    void operator()(std::ostream& out, const vertex_or_edge_desc& v) const {
    }
  };

    
  //! Utility method for writing out graphs
  template <class out_stream, class graph_t>
  void write_graph(out_stream& out, graph_t const& g, const string_type& nodes_property_name = "name", const string_type& edge_property_name = "weight")
  {
    typedef typename graph_t::vertex_tag_t  vertex_prop_tag;
    typedef typename graph_t::edge_tag_t    edge_property_tag;
    
    typename boost::property_map<typename graph_t::graph_t/*::vertex_property_map_type*/, vertex_prop_tag>::type tamere = boost::get(vertex_prop_tag(), const_cast<typename graph_t::graph_t&>(g.G));
  
    entry_writer_m<
      typename graph_t::vertex_property_type, 
      typename graph_t::vertex_property_map_type
    > op(const_cast<typename graph_t::graph_t&>(g.G), vertex_prop_tag(), nodes_property_name);
    entry_writer_m<
      typename graph_t::edge_property_type, 
      typename graph_t::edge_property_map_type
    > ope(const_cast<typename graph_t::graph_t&>(g.G), edge_property_tag(), edge_property_name);
    write_graphviz(out, g.G, op, ope);
  }


  //! Utility function for reading back a graph writer with write_graph
  template <class in_stream, class graph_t>
  void read_graph(in_stream &is, graph_t &graph, const string_type& node_property_name = "name", const string_type& edge_property_name = "weight")
  {

    graph.G.clear();
    
    boost::dynamic_properties dp2;

    //typename graph_t::vertex_helper_t::type read_names;
    //boost::associative_property_map<typename graph_t::vertex_property_map_type> nodes_names(read_names);
    //dp2.property(node_property_name, nodes_names);

    typename graph_t::vertex_property_map_type vertex_prop = boost::get(typename graph_t::vertex_tag_t(), graph.G);
    dp2.property(node_property_name, vertex_prop);

    typename graph_t::edge_property_map_type edges_prop = boost::get(typename graph_t::edge_tag_t(), graph.G);
    dp2.property(edge_property_name, edges_prop);
    
    //std::set<int> ids;
    //boost::associative_property_map<typename graph_t::vertex_property_map_type> nids(ids);
    
    
    typedef std::map<typename graph_t::vertex_descriptor, int> map_id_t;
    map_id_t map_id;
    boost::associative_property_map< map_id_t > nids(map_id);
    dp2.property("node_id", nids);
    
    try 
    {
      if(!read_graphviz(is, graph.G, dp2))
      {
        YAYI_THROW("Error during the reading of the graph from the input stream");
      }
    }
    catch(boost::bad_parallel_edge &e) {
      YAYI_THROW("Error during the reading of the graph from the input stream (bad parallel edge): " + std::string(e.what()));    
    }
    catch(boost::graph_exception& e)
    {
      YAYI_THROW("Graph error during the reading of the graph from the input stream : " + std::string(e.what()));
    }
    catch(std::exception &e)
    {
      YAYI_THROW("Error during the reading of the graph from the input stream : " + std::string(e.what()));    
    }
    

    //typename graph_t::vertex_property_map_type name = boost::get(typename graph_t::vertex_tag_t(), graph.G);
    typename graph_t::vertex_iterator it, ite;
    boost::tie(it, ite) = graph.vertices();
    for(;it != ite; ++it)
    {
      std::cout << "Node : \"" << map_id[*it] <<  "\" \"" << boost::get(vertex_prop, *it) << "\" " << std::endl;
    }
    
    
    return;
  
  }
  



}

#endif

