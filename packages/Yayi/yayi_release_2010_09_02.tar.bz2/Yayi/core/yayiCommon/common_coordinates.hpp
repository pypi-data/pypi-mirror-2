/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_COORDINATES_HPP__
#define YAYI_COMMON_COORDINATES_HPP__

/*!@file
 * This file contains the coordinates structure, which is a template class parametrized by the dimension of the space.
 * It contains also some usefull functions for manipulating coordinates.
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <vector>
#include <algorithm>


namespace yayi
{
  // Forward declarations
  template <int dim, class scalar_coordinate_t> struct s_coordinate;
  template <class scalar_coordinate_t>          struct s_coordinate<0, scalar_coordinate_t>;

  /*!@rief Main coordinates type
   *
   * @author Raffi Enficiaud
   */
  template <int dim, class scalar_coordinate_t = scalar_coordinate> struct s_coordinate
  {
  public:

    typedef scalar_coordinate_t scalar_coordinate_type;		//!< Type contained in each dimension
    enum {static_dimensions = dim};

  private:
    scalar_coordinate_type coords[dim];
    typedef s_coordinate<dim, scalar_coordinate_t> this_type;

  public:
    s_coordinate()
    {
      //for(int i = 0; i < dim; i++) coords[i] = r.coords[i];
    }
    s_coordinate(const this_type& r)
    {
      for(int i = 0; i < dim; i++) coords[i] = r.coords[i];
    }
    explicit s_coordinate(const scalar_coordinate_type r)
    {
      for(int i = 0; i < dim; i++) coords[i] = r;
    }
    /*explicit s_coordinate(const scalar_coordinate_type r[dim])
    {
      for(int i = 0; i < dim; i++) coords[i] = r[i];
    }*/

    explicit s_coordinate(const s_coordinate<0, scalar_coordinate_type>& r);
#if 0
    {
      int i = 0;
      for(int j = std::min(r.dimension(), dim); i < j; i++) coords[i] = r[i];
      if(i < dim)
      {
        for(; i < dim; i++)
        {
          coords[i] = 0;
        }
      }
      else
      {
        for(int j = r.dimension(); i < j; i++)
        {
          DEBUG_ASSERT(
            r[i] == 0, 
            "Trying to copy a generic coordinate of dimension " + int_to_string(r.dimension())
            + std::string(" into a coordinate of dimension ") + int_to_string(dim));
        }
      }
    }
#endif


    template <class it_t>
    static this_type from_table(it_t it)
    {
      this_type out;
      for(int i = 0; i < dim; i++) out.coords[i] = *it++;
      return out;
    }

    template <class it_t>
    static std::vector<this_type> from_table_multiple(it_t r_begin, const it_t r_end)
    {
      DEBUG_ASSERT(((r_end - r_begin) % dim) == 0, "Incorrect number of elements");
      std::vector<this_type> out;
      for(; r_begin != r_end; r_begin += dim) out.push_back(from_table(r_begin));
      return out;
    }


    //! Assignement
    this_type& operator=(const this_type& r)
    {
      for(int i = 0; i < dim; i++) coords[i] = r.coords[i];
      return *this;
    }



    //! Comparison between two instances of coordinates
    bool operator==(const this_type& r) const throw()
    {
      for(int i = 0; i < dim; i++) if(coords[i] != r.coords[i]) return false;
      return true;
    }
    //! Comparison between two instances of coordinates
    bool operator!=(const this_type& r) const throw()
    {
      for(int i = 0; i < dim; i++) if(coords[i] != r.coords[i]) return true;
      return false;
    }
    
    /*! Simple lexicographical order between two coordinates of the same type
     *  Intended for convenience
     */
    bool operator<(const this_type& r) const throw() {
      for(int i = 0; i < dim; i++)
      {
        if(coords[i] == r.coords[i])
          continue;
        return coords[i] < r.coords[i];
      }
      return false;
    }

    //! Compare the coordinates to a scalar value
    bool operator==(const scalar_coordinate_type v) const throw()
    {
      for(int i = 0; i < dim; i++) if(coords[i] != v) return false;
      return true;
    }


    //! Shift
    this_type& operator+=(const this_type& r) throw()
    {
      for(int i = 0; i < dim; i++) coords[i] += r.coords[i];
      return *this;
    }

    //! Arithmetic
    this_type operator+(const this_type& r_) const throw()
    {
      this_type return_;
      for(int i = 0; i < dim; i++) return_.coords[i] = coords[i] + r_.coords[i];
      return return_;
    }

    //! Shift
    this_type& operator-=(const this_type& r) throw()
    {
      for(int i = 0; i < dim; i++) coords[i] -= r.coords[i];
      return *this;
    }

    //! Arithmetic
    this_type operator-(const this_type& r_) const throw()
    {
      this_type return_;
      for(int i = 0; i < dim; i++) return_.coords[i] = coords[i] - r_.coords[i];
      return return_;
    }
    
    //! Returns the "min" of two coordinates, which is the dimensionwise minimum
    friend this_type min_coordinate(this_type l, const this_type& r)
    {
      for(int i = 0; i < dim; i++)
        l[i] = std::min(l[i], r[i]);
      return l;
    }



    //! Returns true if the coordinate is set to the origin of the space
    bool is_origin() const throw()
    {
      for(int i = 0; i < dim; i++) if(coords[i] != 0) return false;
      return true;
    }


    scalar_coordinate_type operator[](unsigned int i) const
    {
      DEBUG_ASSERT(i < dim, "Error out of range");
      return coords[i];
    }
    scalar_coordinate_type& operator[](unsigned int i)
    {
      DEBUG_ASSERT(i < dim, "Error out of range");
      return coords[i];
    }

    void clear() throw()
    {
      for(int i = 0; i < dim; i++) coords[i] = 0;
    }

    //! For compatibility with s_coordinate<0> ... bad design
    void set_dimension(int) throw() {}

    //! The coordinate dimension
    const unsigned int dimension() const throw() {return static_cast<unsigned int>(dim);}
  };


  /*!@brief Specializing of coordinates for unknown (any) dimension
  *
  * @author Raffi Enficiaud
  */
  template <class scalar_coordinate_t> struct s_coordinate<0, scalar_coordinate_t>
  {

    //! Storage class of the coordinates
    typedef scalar_coordinate_t scalar_coordinate_type;

  private:
    std::vector<scalar_coordinate_type> coords;
    typedef s_coordinate<0, scalar_coordinate_t> this_type;

  public:

    //! Default constructor
    s_coordinate() : coords(){}


    //! Copy constructor
    s_coordinate(const this_type& r) : coords(r.coords.begin(), r.coords.end())
    {
    }

    //! Copy constructor from a coordinate of diffferent dimension
    template <int i_dim>
      s_coordinate(const s_coordinate<i_dim>& r) : coords()
    {
      coords.resize(r.dimension());
      for(int i = 0, j = r.dimension(); i < j; i++)
        coords[i] = r[i];
    }

    
    /*! Simple lexicographical order between two coordinates of the same type
     *  Intended for convenience
     */
    bool operator<(const this_type& r) const throw() 
    {
      if(dimension() != r.dimension())
        return dimension() < r.dimension();
      for(int i = 0, j = dimension(); i < j; i++)
      {
        if(coords[i] == r.coords[i])
          continue;
        return coords[i] < r.coords[i];
      }
      return false;
    }

    //! Comparison between two instances of coordinates
    bool operator==(const this_type& r) const throw()
    {
      if(r.dimension() != dimension())
        return false;
      for(int i = 0, j = dimension(); i < j; i++) if(coords[i] != r.coords[i]) return false;
      return true;
    }
    //! Comparison between two instances of coordinates
    bool operator!=(const this_type& r) const throw()
    {
      if(r.dimension() != dimension())
        return true;
      for(int i = 0, j = dimension(); i < j; i++) if(coords[i] != r.coords[i]) return true;
      return false;
    }


    //! Compare the coordinates to a scalar value
    bool operator==(const scalar_coordinate_type v) const throw()
    {
      for(int i = 0, j = dimension(); i < j; i++) if(coords[i] != v) return false;
      return true;
    }

    //! Returns true if the coordinate is set to the origin of the space
    bool is_origin() const throw()
    {
      for(int i = 0, j = dimension(); i < j; i++) if(coords[i] != 0) return false;
      return true;
    }

    //! Shift
    this_type& operator+=(const this_type& r)
    {
      // Raffi : il faut changer ce comportement
      for(int i = 0, j = std::min(dimension(), r.dimension()); i < j; i++)
        coords[i] += r[i];
      if(dimension() < r.dimension())
      {
        for(int i = dimension(), j = r.dimension(); i < j; i++)
          coords.push_back(r[i]);
      }
      return *this;
    }

    this_type operator+(const this_type& r) const
    {
      this_type out(*this);
      out.set_dimension(std::max(dimension(), r.dimension()));
      for(int i = 0, j = std::min(dimension(), r.dimension()); i < j; i++)
        out.coords[i] += r[i];
      if(dimension() < r.dimension())
      {
        for(int i = dimension(), j = r.dimension(); i < j; i++)
          out.coords.push_back(r[i]);
      }
      return out;
    }

    //! Shift
    this_type& operator-=(const this_type& r)
    {
      // Raffi : il faut changer ce comportement
      for(int i = 0, j = std::min(dimension(), r.dimension()); i < j; i++)
        coords[i] -= r[i];
      if(dimension() < r.dimension())
      {
        for(int i = dimension(), j = r.dimension(); i < j; i++)
          coords.push_back(-r[i]);
      }
      return *this;
    }

    this_type operator-(const this_type& r) const
    {
      this_type out(*this);
      out.set_dimension(std::max(dimension(), r.dimension()));
      for(int i = 0, j = std::min(dimension(), r.dimension()); i < j; i++)
        out.coords[i] -= r[i];
      if(dimension() < r.dimension())
      {
        for(int i = dimension(), j = r.dimension(); i < j; i++)
          out.coords.push_back(-r[i]);
      }
      return out;
    }

    //! Returns the "min" of two coordinates, which is the dimensionwise minimum
    //! The dimension of the output vector is the maximal dimension of both vector, the misssing dimensions
    //! are considered as 0.
    friend this_type min_coordinate(this_type l, const this_type& r)
    {
      for(int i = 0, j = std::min(l.dimension(), r.dimension()); i < j; i++)
        l[i] = std::min(l[i], r[i]);
      if(l.dimension() < r.dimension())
      {
        for(int i = l.dimension(), j = r.dimension(); i < j; i++)
          l.coords.push_back(0);
      }
      else
      {
        for(int i = r.dimension(), j = l.dimension(); i < j; i++)
          l.coords[i] = 0;
      }
      return l;
    }



    //! Index operator (const)
    const scalar_coordinate_type& operator[](unsigned int i) const 
    {
      return coords[i];
    }

    //! Index operator (non const)
    scalar_coordinate_type& operator[](unsigned int i)
    {
      return coords[i];
    }

    //! Returns the number of dimensions (dynamic)
    const unsigned int dimension() const throw() {return static_cast<unsigned int>(coords.size());}

    //! Returns the number of dimensions (dynamic)
    void set_dimension(int d) throw() {coords.resize(d);}

    //! Resets the coordinate
    void clear() throw() {coords.clear();}

  };




  template <int dim, class scalar_coordinate_t>
  s_coordinate<dim, scalar_coordinate_t>::s_coordinate(const s_coordinate<0, scalar_coordinate_t>& r)
  {
    unsigned int i = 0;
    for(unsigned int j = std::min(r.dimension(), static_cast<unsigned int>(dim)); i < j; i++) coords[i] = r[i];
    if(i < dim)
    {
      for(; i < dim; i++)
      {
        coords[i] = 0;
      }
    }
    else
    {
      for(unsigned int j = r.dimension(); i < j; i++)
      {
        DEBUG_ASSERT(
          r[i] == 0, 
          "Trying to copy a generic coordinate of dimension " + int_to_string(r.dimension())
          + std::string(" into a coordinate of dimension ") + int_to_string(dim));
      }
    }
  }

  inline s_coordinate<4> c4D(
    const s_coordinate<4>::scalar_coordinate_type a, 
    const s_coordinate<4>::scalar_coordinate_type b, 
    const s_coordinate<4>::scalar_coordinate_type c,
    const s_coordinate<4>::scalar_coordinate_type d) {
    
    const s_coordinate<4>::scalar_coordinate_type t[4] = {a,b,c,d};
    return s_coordinate<4>::from_table(t);
  } 

  inline s_coordinate<3> c3D(
    const s_coordinate<3>::scalar_coordinate_type x, 
    const s_coordinate<3>::scalar_coordinate_type y, 
    const s_coordinate<3>::scalar_coordinate_type z) {
    
    const s_coordinate<3>::scalar_coordinate_type t[3] = {x,y,z};
    return s_coordinate<3>::from_table(t);
  } 

  inline s_coordinate<2> c2D(
    const s_coordinate<2>::scalar_coordinate_type x, 
    const s_coordinate<2>::scalar_coordinate_type y) {
    
    const s_coordinate<2>::scalar_coordinate_type t[2] = {x,y};
    return s_coordinate<2>::from_table(t);
  }
  
  

}


namespace std
{
  template <int dim, class T> inline std::ostream & operator<<(std::ostream &o, const yayi::s_coordinate<dim, T> &c)
  {
    int i = 0, j = c.dimension() - 1;
    o << "(";
    for(; i < j; i++)
    {
      o << c[i] << ", ";
    }
    if(j >= 0) o << c[j];
    o << ")";
    return o;
  }

  template <int dim, class T> inline std::wostream& operator<<(std::wostream &o, const yayi::s_coordinate<dim, T> &c)
  {
    int i = 0, j = c.dimension() - 1;
    o << L"(";
    for(; i < j; i++)
    {
      o << c[i] << L", ";
    }
    if(j >= 0) o << c[j];
    o << L")";
    return o;
  }

}

#endif


