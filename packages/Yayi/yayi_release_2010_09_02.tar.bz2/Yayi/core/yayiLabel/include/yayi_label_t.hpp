/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_T_HPP__
#define YAYI_LABEL_T_HPP__

/*!@file
 * This file defines generic functions for image labelling
 * @author Raffi Enficiaud
 */

#include <boost/call_traits.hpp>
#include <functional>
#include <queue>
#include <vector>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>

#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>

namespace yayi
{
  namespace label
  {
  
    //! Functor always returning true
    //! This functor allows the labelling of every pixels
    template <class pixel_type>
    struct s_always_true
    {
      bool operator()(typename boost::call_traits<pixel_type>::param_type v) const throw() {return true;}
    };

    //! Functor returning true for non-black pixels
    //! This functor allows the labelling of marked pixels
    template <class pixel_type>
    struct s_filter_non_black
    {
      bool operator()(typename boost::call_traits<pixel_type>::param_type v) const throw() {return v != pixel_type(0);}
    };

    //! Functor returning true for non-black pixels
    //! This functor allows the labelling of marked pixels
    template <>
    struct s_filter_non_black<yaF_simple>
    {
      bool operator()(boost::call_traits<yaF_simple>::param_type v) const throw() {return std::abs(v) < 1E-10;}
    };


    //! Functor generating a new value for each component (scalar values)
    template <class pixel_type>
    struct s_id_generator
    {
      pixel_type current;
      s_id_generator() : current() {}
      pixel_type operator()() throw() {return ++current;}
    };


    //! Functor keeping tracks of the offsets of the current connected component
    //! This functor puts every offsets of the current connected component into an internal queue, that can
    //! then been iterated over
    struct s_post_process_connected
    {
      typedef std::vector<offset> subcontainer_type;
      typedef subcontainer_type::const_iterator iterator;

      subcontainer_type q;
      void reset() throw() 
      {
        q.clear();
      }
      void operator()(const offset o) throw() 
      {
        q.push_back(o);
      }
      
      iterator begin()  const {return q.begin();}
      iterator end()    const {return q.end();}
      
      subcontainer_type& internal_storage() {return q;}
    };


    //! Functor keeping tracks of the offsets and values of the neighbors elements of the current connected component
    //! This implementation does nothing
    template <class pixel_type>
    struct s_no_post_process_unconnected
    {
      void reset() throw() 
      {
      }
      void operator()(
        const offset o_center, 
        const offset o_neigh,
        typename boost::call_traits<pixel_type>::param_type v_center,
        typename boost::call_traits<pixel_type>::param_type v_neighbor) throw() 
      {
      }
    };
    
    
    
    
    //! Functor labelling the output image with a new id for each component
    template <
      class image_out_t, 
      class connected_component_id_generator_t = s_id_generator<typename image_out_t::pixel_type> >
    struct s_finalize_component_by_image_labeling
    {
      typedef s_finalize_component_by_image_labeling<image_out_t, connected_component_id_generator_t> this_type;
      image_out_t& im_out;
      connected_component_id_generator_t gen;
      
      s_finalize_component_by_image_labeling(this_type& r) : im_out(r.im_out), gen(r.gen) {}
      s_finalize_component_by_image_labeling(image_out_t& im_out_) : im_out(im_out_), gen() 
      {
        yaRC res = constant_image_t(typename image_out_t::pixel_type(0), im_out);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error while initializing the output image");
          YAYI_THROW(res);
        }
      }
      
      template <class connected_comp_container, class unconnected_comp_container>
      typename image_out_t::pixel_type operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        typename image_out_t::pixel_type const id = gen();
        for(typename connected_comp_container::iterator it(p.begin()), ite(p.end()); it != ite; ++it)
        {
          im_out.pixel(*it) = id;
        }
        
        return id;
      }
    
    };


    //! Functor labelling the elements of the connected component by inserting their offset into a internal storage (pair(id, vector))
    template <
      class pixel_type,
      class connected_component_id_generator_t = s_id_generator<pixel_type> >
    struct s_finalize_component_by_internal_storage
    {
      typedef s_finalize_component_by_internal_storage<connected_component_id_generator_t> this_type;
      
      typedef std::vector<offset> coordinate_storage_type;
      typedef std::vector< std::pair<pixel_type, coordinate_storage_type > > internal_storage_type;
      internal_storage_type internal_queue;
      connected_component_id_generator_t gen;
      
      s_finalize_component_by_internal_storage(this_type& r) : internal_queue(r.internal_queue), gen(r.gen) {}
      s_finalize_component_by_internal_storage() : internal_queue(), gen() {}
      
      
      //! Note that the p container should be empty at the end of the call (storage swaping instead of cpoying)
      template <class connected_comp_container, class unconnected_comp_container>
      void operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        pixel_type const id = gen();
        internal_queue.push_back(std::make_pair(id, coordinate_storage_type()));
        internal_queue.back().second.swap(p.internal_storage());
        assert(p.internal_storage().empty());
      }
      
      typename internal_storage_type::const_iterator begin()  const throw() {return internal_queue.begin();}
      typename internal_storage_type::const_iterator end()    const throw() {return internal_queue.end();}
      
      internal_storage_type& internal_storage() {return internal_queue;}
    
    };




    //! Simple helper for stating the default behaviour of s_image_label, about the pixels input filtering
    template <class image_t> struct label_default_accept    {typedef s_always_true<typename image_t::pixel_type> type;};
    //! Simple helper for stating the default behaviour of s_image_label, about the relation for two pixels being in the same connected component
    template <class image_t> struct label_default_relation  {typedef std::equal_to<typename image_t::pixel_type> type;};

        
  
    /*! Labelling generic structure
     *  The template parameters are the following:
     *  image_t:    image type on which the labelling is performed
     *  se_t:       neighborhood graph for connected components
     *  finalize_t: binary functor finalizing the elements of post_process_t and post_process_unconnected_t
     *  accept_t:   unary functor filtering the possible values of image_t
     *  relation_t: binary functor used as a predicate for two pixels being in the same connected component
     *  post_process_t: unary functor called each time a new point is discovered in the connected component
     *  post_process_unconnected_t: 4-ary functor called each time a point neighbor to the current connected component is discovered
     *
     */
    template <
      class image_t, 
      class se_t, 
      class finalize_t,
      class accept_t    = typename label_default_accept<image_t>::type,
      class relation_t  = typename label_default_relation<image_t>::type,
      class post_process_t = s_post_process_connected,
      class post_process_unconnected_t = s_no_post_process_unconnected<typename image_t::pixel_type>
    >
    struct s_image_label
    {
      finalize_t  finalize;
      relation_t  relation;
      accept_t    accept;
      post_process_t post_process;
      post_process_unconnected_t post_process_unconnected;


    
      s_image_label() : finalize(), relation(), accept() {}
      s_image_label(finalize_t& finalize_) : finalize(finalize_), relation(), accept() {}
    
    
      yaRC operator()(const image_t&im_in, const se_t& se)
      {
        post_process.reset();
        post_process_unconnected.reset();
        
        typedef se::s_runtime_neighborhood<image_t const, se_t> neighborhood_t;// to be delegated to another structure      
        neighborhood_t neighbor(im_in, se.remove_center());
        
        std::queue<offset>  q;

        
        typedef typename s_get_same_image_of_t<label_image_pixel_t, image_t>::type label_image_type;
        
        label_image_type im_labeled_points; 
        yaRC res = im_labeled_points.set_same(im_in);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in set_same");
          return res;
        }
        
        res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), im_labeled_points);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in constant_image_t");
          return res;
        }


        // iterator over the image
        for(typename image_t::const_iterator it(im_in.begin_block()), ite(im_in.end_block()); it != ite; ++it)
        {
        
          if(!accept(*it))
            continue;
          
          offset const oo = it.Offset();
          if(im_labeled_points.pixel(oo) == static_cast<label_image_pixel_t>(e_lab_processed))
            continue;
            
          q.push(oo);

          while(!q.empty())
          {
            offset const o = q.front();
            q.pop();
            post_process(o);
            im_labeled_points.pixel(o) = static_cast<label_image_pixel_t>(e_lab_processed);
            
            typename image_t::pixel_type const v = im_in.pixel(o);
            
            neighbor.center(o);
            
            for(typename neighborhood_t::const_iterator itn(neighbor.begin()), itne(neighbor.end()); itn != itne; ++itn) 
            {
              typename image_t::pixel_type const n_v = *itn;  
              if(accept(n_v))
              {
                offset const n_o = itn.Offset();
                if(relation(v, n_v))
                {
                  // new element in the connected component
                  if(im_labeled_points.pixel(n_o) != static_cast<label_image_pixel_t>(e_lab_processed))
                  {
                    assert(n_o != o);
                    q.push(n_o);
                    im_labeled_points.pixel(n_o) = static_cast<label_image_pixel_t>(e_lab_processed);
                  }
                }
                else 
                {
                  // connected component's neighborhood : for instance adjacency graph or minima
                  // if(im_labeled_points.pixel(n_o) == static_cast<label_image_pixel_t>(e_lab_processed))
                  // neighbor can be unlabelled (extrema)
                  post_process_unconnected(o, n_o, v, n_v);
                }
              }                
            
            }
          }
        
          finalize(post_process, post_process_unconnected);
          
          post_process.reset();
          post_process_unconnected.reset();
        }
        
        return yaRC_ok;
      }
    };




    //! Image labelling with a single id by connected component
    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_label_t(const image_in_t &imin, const se_t& se, image_out_t& imout)
    {
      typedef s_finalize_component_by_image_labeling<image_out_t> finalize_t;
      finalize_t finalizer(imout);
      
      s_image_label<image_in_t, se_t, finalize_t> label_op(finalizer);
      
      return label_op(imin, se);    
    };
  
  
  }
}



#endif /* YAYI_LABEL_T_HPP__ */
