/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_PRIORITY_QUEUES_HPP__
#define YAYI_COMMON_PRIORITY_QUEUES_HPP__


/*!@file
 * Defines the priority queues
 *
 */

#include <map>
#include <vector>
#include <functional>


#include <Yayi/core/yayiCommon/common_errors.hpp>

namespace yayi
{
  
  // forward declaration
  template <class key_t, class value_t, class order_t>
  class priority_queue_t;
  
  template <class key_t, class plateau_container_t>
  class priority_queue_iterator_t;
  
  template <class key_t, class plateau_container_t>
  class priority_queue_plateau_iterator_t;
  
  
  
  
  /*!@brief Iterator on plateaus
   * This iterator iterates a generic iterator on a constant plateau. Since fewer data is handled during this iteration,
   * the iterator is faster than the generic @ref priority_queue_iterator_t iterator.
   *
   * @see priority_queue_iterator_t
   */
  template <class key_t, class plateau_container_iterator_t>
  class priority_queue_plateau_iterator_parent_t {
  
  protected:
    key_t key_value;
    plateau_container_iterator_t it;
    
  public: 
    typedef priority_queue_plateau_iterator_parent_t<key_t, plateau_container_iterator_t> this_type;
    typedef typename plateau_container_iterator_t::value_type value_type;
    typedef typename plateau_container_iterator_t::reference  reference_type;

    
    priority_queue_plateau_iterator_parent_t(const key_t& k, const plateau_container_iterator_t& it_) : key_value(k), it(it_)
    {}
    
    //! Returns the actual height of the plateau 
    const key_t& key() const {
      return key_value;
    }
  
    //! Increments iterator
    this_type& operator++() {
      ++it;
      return *this;
    }
    
    //! Deference operator
    reference_type operator*() {
      return *it;
    }
    
    //! Compares iterators
    bool operator==(const this_type& r_) const throw() {
      return (r_.key_value == key_value) && (r_.it == it); // second can be cheched, so we can avoid first test if no chech is done (no debug ?)
    }
    
    //! Compares iterators
    bool operator!=(const this_type& r_) const throw() {
      return (r_.key_value != key_value) || (r_.it != it); // second can be cheched, so we can avoid first test if no chech is done (no debug ?)
    }
  };



  template <class key_t, class plateau_container_const_iterator_t>
  class priority_queue_plateau_iterator_const_t;

  template <class key_t, class plateau_container_iterator_t>//class plateau_container_iterator_t>
  class priority_queue_plateau_iterator_t//<key_t, typename std::deque<value_t>::iterator>
    : public priority_queue_plateau_iterator_parent_t<key_t,plateau_container_iterator_t>// typename std::deque<value_t>::iterator>//plateau_container_iterator_t>
  {
    //typedef typename std::deque<value_t>::iterator plateau_container_iterator_t;

    typedef priority_queue_plateau_iterator_t<
      key_t, 
      plateau_container_iterator_t> this_type;
    
    typedef priority_queue_plateau_iterator_parent_t<
      key_t, 
      plateau_container_iterator_t> parent_type;
      
    friend class priority_queue_plateau_iterator_const_t<
      key_t, 
      typename std::vector<typename std::iterator_traits<plateau_container_iterator_t>::value_type>::const_iterator >;
      //typename std::deque<typename plateau_container_iterator_t::value_type>::const_iterator>; 

      
  public:
    //priority_queue_plateau_iterator_t(const key_t& k, const plateau_container_const_iterator_t& it_) : parent_type(k, it_) {}
    priority_queue_plateau_iterator_t(const key_t& k, const plateau_container_iterator_t& it_) : parent_type(k, it_) {}
  
  };
  
  template <class key_t, class plateau_container_const_iterator_t>//, class order_t>
  class priority_queue_plateau_iterator_const_t 
    : public priority_queue_plateau_iterator_parent_t<key_t, plateau_container_const_iterator_t>//typename std::deque<value_t>::const_iterator > //typename priority_queue_t<key_t, value_t, order_t>::plateau_container_type::const_iterator>
  {
    //typedef typename std::deque<value_t>::iterator plateau_container_iterator_t;//typename priority_queue_t<key_t, value_t, order_t>::plateau_container_type::iterator plateau_container_iterator_t;
    //typedef typename std::deque<value_t>::const_iterator plateau_container_const_iterator_t; //priority_queue_t<key_t, value_t, order_t>::plateau_container_type::const_iterator plateau_container_const_iterator_t;

    typedef priority_queue_plateau_iterator_const_t<
      key_t, 
      plateau_container_const_iterator_t> this_type;

    //typedef priority_queue_plateau_iterator_t<
    //  key_t, 
    //  plateau_container_iterator_t> this_other_type;
    
    typedef priority_queue_plateau_iterator_parent_t<
      key_t, 
      plateau_container_const_iterator_t> parent_type;
      
  public:
    priority_queue_plateau_iterator_const_t(const key_t& k, const plateau_container_const_iterator_t& it_) : parent_type(k, it_) {}

    template <class other_type>
    priority_queue_plateau_iterator_const_t(const priority_queue_plateau_iterator_t<key_t, other_type>& it_) : parent_type(it_.key_value, it_.it) {}

    
    //template <class it_t>
    //priority_queue_plateau_iterator_t(const key_t& k, const it_t& it_) : parent_type(k, it_) {}
  
  }; 



  
  /*!@brief Iterator on the whole priority queue
   * This iterator iterates a generic iterator on the priority queue, ordered in the same order
   * as the ke elements and the insertion of value elements (FIFO style).
   * There is an other version iterating on a constant priority level (@ref priority_queue_plateau_iterator_t)
   *
   * @see priority_queue_plateau_iterator_t
   */
  template <class order_container_iterator_t, class plateau_container_iterator_t>
  class priority_queue_iterator_t {
    plateau_container_iterator_t  it, ite;
    order_container_iterator_t    itm;
    
  public: 
    typedef priority_queue_iterator_t<order_container_iterator_t, plateau_container_iterator_t> this_type;
    typedef typename plateau_container_iterator_t::value_type value_type;
    typedef typename plateau_container_iterator_t::reference_type reference_type;
    
    typedef typename order_container_iterator_t::mapped_type key_type;
    
    
    priority_queue_iterator_t(
      const order_container_iterator_t& itm_, const plateau_container_iterator_t& it_) : itm(itm_), it(it_)
    {}
    
    //! Returns the actual height of the plateau
    const key_type& key() const {
      return itm->first;
    }
    
    //! Increments iterator
    this_type& operator++() {
      ++it;
      if(it == ite) {
        ++itm;
        ite = itm->second.end();      // attention: faux
        it = itm->second.begin();
      }
      return *this;
    }
    
    //! Deference operator
    reference_type operator*() {
      return *it;
    }
    
    //! Compares iterators
    bool operator==(const this_type& r_) const throw() {
      return (r_.itm == itm) && (r_.it == it); // second can be cheched, so we can avoid first test if no chech is done (no debug ?)
    }
    
    //! Compares iterators
    bool operator!=(const this_type& r_) const throw() {
      return (r_.itm != itm) || (r_.it != it); // second can be checked, so we can avoid first test if no check is done (no debug ?)
    }
  };
  
  
  /*!@brief Generic priority queue
   *
   * @author Raffi Enficiaud
   */
  template <class key_t, class value_t, class order_t = std::less<key_t> >
  class priority_queue_t 
  {

  public:
    typedef std::vector<value_t> plateau_container_type;
    typedef std::vector< std::pair<key_t, value_t> > temporary_queue_type;
    typedef typename temporary_queue_type::size_type size_type;
  
    typedef std::map<key_t, plateau_container_type, order_t> map_type;
    typedef typename map_type::iterator map_iterator_t;
    typedef typename map_type::const_iterator map_const_iterator_t;
    typedef typename map_type::size_type key_size_type;
  
  private:
    map_type              map_object;
    temporary_queue_type  temp_q;
  
    // mettre des static assert pour les types supportés
  
  
  
  public:
    
    typedef key_t     key_type;
    typedef value_t   value_type;
    typedef order_t   order_type;
  
  
    typedef priority_queue_plateau_iterator_t<key_t, typename plateau_container_type::iterator> plateau_iterator_type;
    typedef priority_queue_plateau_iterator_const_t<key_t, typename plateau_container_type::const_iterator> plateau_const_iterator_type;
    friend class priority_queue_plateau_iterator_t<key_t, typename plateau_container_type::iterator>;
    friend class priority_queue_plateau_iterator_const_t<key_t, typename plateau_container_type::const_iterator>;
    
    typedef priority_queue_iterator_t<map_iterator_t, typename plateau_container_type::iterator> iterator;
    typedef priority_queue_iterator_t<map_const_iterator_t, typename plateau_container_type::const_iterator> const_iterator;
    friend class priority_queue_iterator_t<map_iterator_t, typename plateau_container_type::iterator>;
    friend class priority_queue_iterator_t<map_const_iterator_t, typename plateau_container_type::const_iterator>;
  
    priority_queue_t() : map_object(), temp_q()
    {}
    
    priority_queue_t(const priority_queue_t& r) : map_object(r.map_object), temp_q(r.temp_q)
    {}
    
    priority_queue_t(const order_type& o) : map_object(o), temp_q()
    {}    
    
    
    // plateau iteration
    plateau_iterator_type begin_plateau(const key_type& k) {
      map_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return plateau_iterator_type(k, itm->second.begin());
    }
    plateau_iterator_type end_plateau(const key_type& k) {
      map_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return plateau_iterator_type(k, itm->second.end());
    }
    std::pair<plateau_iterator_type, plateau_iterator_type> range_plateau(const key_type& k) {
      map_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return std::make_pair(
        plateau_iterator_type(k, itm->second.begin()),
        plateau_iterator_type(k, itm->second.end())
        );
    }
    
    plateau_iterator_type begin_top_plateau() {
      map_iterator_t itm = map_object.begin();
      if(itm == map_object.end()) {
        YAYI_THROW("The map is empty");;
      }
      return plateau_iterator_type(itm->first, itm->second.begin());
    }
    plateau_iterator_type end_top_plateau() {
      map_iterator_t itm = map_object.begin();
      if(itm == map_object.end()) {
        YAYI_THROW("The map is empty");
      }
      return plateau_iterator_type(itm->first, itm->second.end());
    }
    std::pair<plateau_iterator_type, plateau_iterator_type> range_top_plateau() {
      if(map_object.empty()) {
        YAYI_THROW("The map is empty"); // on doit envoyer quelque chose de correct dans ce cas
      }
      
      map_iterator_t itm = map_object.begin();
      return std::make_pair(
        plateau_iterator_type(itm->first, itm->second.begin()),
        plateau_iterator_type(itm->first, itm->second.end())
        );
    }
    
    
    // plateau iteration (const)
    plateau_const_iterator_type begin_plateau(const key_type& k) const {
      map_const_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return plateau_const_iterator_type(k, itm->second.begin());    
    }
    plateau_const_iterator_type end_plateau(const key_type& k) const {
      map_const_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return plateau_const_iterator_type(k, itm->second.end());    
    }
    std::pair<plateau_const_iterator_type, plateau_const_iterator_type> range_plateau(const key_type& k) const {
      map_const_iterator_t itm = map_object.find(k);
      if(itm == map_object.end()) {
        YAYI_THROW("The key " << k << " does not exist");
      }
      return std::make_pair(
        plateau_const_iterator_type(k, itm->second.begin()),
        plateau_const_iterator_type(k, itm->second.end())
        );
    }
    
    
    plateau_const_iterator_type begin_top_plateau() const {
      map_const_iterator_t itm = map_object.begin();
      if(itm == map_object.end()) {
        YAYI_THROW("The map is empty");;
      }
      return plateau_const_iterator_type(itm->first, itm->second.begin());
    }
    plateau_const_iterator_type end_top_plateau() const {
      map_const_iterator_t itm = map_object.begin();
      if(itm == map_object.end()) {
        YAYI_THROW("The map is empty");
      }
      return plateau_const_iterator_type(itm->first, itm->second.end());
    }
    std::pair<plateau_const_iterator_type, plateau_const_iterator_type> range_top_plateau() const {
      if(map_object.empty()) {
        YAYI_THROW("The map is empty"); // on doit envoyer quelque chose de correct dans ce cas
      }
      
      map_const_iterator_t itm = map_object.begin();
      return std::make_pair(
        plateau_const_iterator_type(itm->first, itm->second.begin()),
        plateau_const_iterator_type(itm->first, itm->second.end())
        );
    }
    
    
    // poping the top plateau
    void pop_top_plateau() {
      if(!map_object.empty())
      {
        typename map_type::const_iterator it = map_object.begin();
        map_object.erase(it->first);
      }
      for(typename temporary_queue_type::const_iterator it(temp_q.begin()), ite(temp_q.end()); it != ite; ++it)
        map_object[it->first].push_back(it->second);
      
      temp_q.clear();
    }
    
    // Generic iteration
    iterator begin() {
      return iterator(map_object.begin(), map_object.begin()->second.begin());
    }
    
    iterator end() {
      return iterator(--(map_object.end()), map_object.begin()->second.begin());
    }
    
    
    
    // Insertion
    void insert(const key_type& k, const value_type &v) {
      map_object[k].push_back(v);
    }
    
    void insert_buffered(const key_type& k, const value_type &v) {
      temp_q.push_back(std::make_pair(k, v));
    }
    
    
    // informations
    //! Returns the number of elements for all keys
    size_type size() const {
      size_type s = 0;
      for(typename map_type::const_iterator it(map_object.begin()), ite(map_object.end()); it != ite; ++it)
        s += it->second.size();      
      return s;
    }

    //! Returns the number of keys
    size_type number_keys() const {
      return map_object.size();
    }

    //! Returns the minimal key
    key_type const& min_key() const {
      if(map_object.empty()) {
        YAYI_THROW("The map is empty"); // on doit envoyer quelque chose de correct dans ce cas
      }
      return map_object.begin()->first;
    }
    
    //! Returns true if empty
    bool empty() const 
    {
      return map_object.size() == 0;
    }
  
  };
 

  
}


#endif /* YAYI_COMMON_PRIORITY_QUEUES_HPP__ */

