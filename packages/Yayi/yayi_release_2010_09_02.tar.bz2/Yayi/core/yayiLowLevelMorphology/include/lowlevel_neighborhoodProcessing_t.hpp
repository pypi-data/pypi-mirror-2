/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__

/*!@file
 * This file defines several operators for neighborhood processing.
 * The following processing methods are implemented:
 * - generic algorithm
 * 
 */

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

namespace yayi { namespace llmm {


  /*!@brief This class defines a generic process on the neighborhoods of an image
   *
   * The neighborhood is centered at each point of the image, without using any redundancy between two successive neighborhood.
   * Only two functionalities of the neighborhoods are used: centering and iteration. This neighbor processor is hence applicable
   * on the most general neighborhood/se concept.
   *
   * @author Raffi Enficiaud
   */
  struct s_generic_processor {
  
  
    /*! Processor for operators returning void (computation over the neighborhoods)
     */
    template <class image_t, class se_t, class op_t>
    yaRC operator()(const image_t& im, const se_t& se, op_t& op) {
    
      typedef se::s_runtime_neighborhood<image_t const, se_t> neighborhood_t; // to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
    
      for(typename image_t::const_iterator it(im.begin()), ite(im.end()); it != ite; ++it) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }

    //! The same as the previous operator, but with write access to the neighbors
    template <class image_t, class se_t, class op_t>
    yaRC operator()(image_t& im, const se_t& se, op_t& op) {
    
      typedef se::s_runtime_neighborhood<image_t, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
    
      for(typename image_t::iterator it(im.begin()), ite(im.end()); it != ite; ++it) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }


    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC operator()(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it != ite && ito != itoe; ++it, ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        *ito = op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }



    /*! Neighborhood processor with the center value
     *  The operator should model a ternary functor, with a return value.
     *  This is used for instance for inf-sup half morphological gradients.
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it != ite && ito != itoe; ++it, ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        *ito = op(neighbor.begin(), neighbor.end(), *it);
      }

      return yaRC_ok;
    }



    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction/addition. 
     *  op_t should be a model of ternary functor. Its return value is ignored.
     *  We cannot remove the center directly in this function. In case op is a idempotent operator,
     *  the center of the structuring element can be safely removed by the caller. 
     */
    template <class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center_to_neighborhood(const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_out_t, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(imout, se);
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      for(; ito != itoe; ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(ito) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(ito);
        #endif
        
        op(neighbor.begin(), neighbor.end(), *ito);
      }
           
      return yaRC_ok;
    }


  };
  
  
  
  
  template <class se_type, class operator_type>
  struct neighborhood_processing_strategy {
    typedef s_generic_processor processor_t;
  };


}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__ */
