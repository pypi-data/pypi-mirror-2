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
#include <boost/test/parameterized_test.hpp>
#include <boost/test/test_case_template.hpp>

#include <Yayi/core/yayiDistances/include/exact_distances_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <Yayi/core/yayiCommon/include/common_time.hpp>

#include <boost/random/uniform_real.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/variate_generator.hpp>

#include <boost/numeric/conversion/bounds.hpp>
#include <boost/mpl/list.hpp>
#include <boost/mpl/pair.hpp>

#include <Yayi/core/yayiCommon/include/common_coordinates_mpl_utils_t.hpp>
#include <fstream>
#include <Yayi/core/yayiCommon/common_constants.hpp>

#include <boost/numeric/ublas/io.hpp>


#ifdef YAYI_REAL_RANDOM_EXISTS__
typedef boost::random_device random_generator_type;
#else
typedef boost::mt19937 random_generator_type;
#endif


using namespace yayi;


void test_distance_functions()
{
  using namespace yayi;
  using namespace yayi::distances;
  
  typedef s_coordinate<2> coordinate_type;
  typedef s_coordinate<2, double> source_coordinate_type;
  s_euclidian_distance_op<source_coordinate_type, coordinate_type> op_dist;
  
  double tabled[] = {46.6997, 40.8816};
  int tablei[] = {49, 41};
  
  coordinate_type coord1(coordinate_type::from_table(tablei));
  source_coordinate_type coord2(source_coordinate_type::from_table(tabled));
  
  BOOST_CHECK_CLOSE(op_dist(coord2, coord1), ::sqrt((tablei[0] - tabled[0])*(tablei[0] - tabled[0]) + (tablei[1] - tabled[1])*(tablei[1] - tabled[1])), 1E-10 );

  BOOST_CHECK(!(distance_has_storage_tag<distances::s_lp_distance_op<source_coordinate_type, coordinate_type, 9, 5> >::value));
  BOOST_MPL_ASSERT_NOT((distance_has_storage_tag<distances::s_lp_distance_op<source_coordinate_type, coordinate_type, 9, 5> >));

  BOOST_CHECK((distance_has_storage_tag< s_euclidian_distance_op<source_coordinate_type, coordinate_type> >::value));
  BOOST_MPL_ASSERT((distance_has_storage_tag< s_euclidian_distance_op<source_coordinate_type, coordinate_type> >));
  //BOOST_MPL_ASSERT_NOT((distance_has_storage_tag< s_euclidian_distance_op<source_coordinate_type, coordinate_type> >));
  
  
  s_l5_distance_op<source_coordinate_type, coordinate_type> op_dist5;
  BOOST_CHECK_CLOSE(op_dist5(coord2, coord1), std::pow(std::pow(std::abs(tablei[0] - tabled[0]), 5.) + std::pow(std::abs(tablei[1] - tabled[1]), 5.), .2), 1E-10 );


}


template <int dim1, int dim2>
void test_distance_exact(const int N /*= 100*/) {
  BOOST_CHECKPOINT("test_distance_exact with N = " << N);
  
  yayi::time::s_time_elapsed time_init;
  
  typedef Image<yaF_double> image_type;
  
  image_type im_out_dist;
  image_type* p_im[] = {&im_out_dist};
  image_type::coordinate_type coord;
  coord[0] = dim1; coord[1] = dim2;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  //typedef boost::uniform_real<image_type::coordinate_type::scalar_coordinate_type> distribution_type;
  
  
  //typedef boost::uniform_int<image_type::coordinate_type::scalar_coordinate_type> distribution_type;
  typedef boost::uniform_real<yaF_simple> distribution_type;
  typedef random_generator_type generator_type;
  typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

  generator_type rng;
  distribution_generator_t generator(rng, distribution_type(0, 1.));
  #if 0
  std::vector<distribution_generator_t> v_generator;
  for(int i = 0; i < image_type::coordinate_type::static_dimensions; i++)
  {
    v_generator.push_back(distribution_generator_t(rng, distribution_type(0, coord[i])));
  }
  #endif
  
  // fire n random points
  typedef s_coordinate<image_type::coordinate_type::static_dimensions, yaF_double> source_coordinate_t;
  std::vector< source_coordinate_t > v_sources;
  std::cout << "Source points" << std::endl;
  for(int i = 0; i < N; i++)
  {
    source_coordinate_t current;
    for(int j = 0; j < image_type::coordinate_type::static_dimensions; j++)
    {
      current[j] = generator() * coord[j];//v_generator[j]();
    }
    v_sources.push_back(current);
    //std::cout << current << "\t";
  }
  std::cout << std::endl;
  std::cout << "Init total microseconds = " << time_init.total_microseconds() << std::endl;

  
  yayi::time::s_time_elapsed time_distance;
  
  distances::s_euclidian_distance_op<source_coordinate_t, image_type::coordinate_type> dist_op;
  yaRC res = distances::exact_distance_t(v_sources, dist_op, im_out_dist);
  std::cout << "N = " << N << "\t--- size = " << im_out_dist.Size() << "\t--- distance total milliseconds = " << time_distance.total_milliseconds() << std::endl;

  
  // check des sorties
  std::cout << "Checking" << std::endl;
  yayi::time::s_time_elapsed time_check;
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    yaF_double current_distance = im_out_dist.pixel(i), min_dist = boost::numeric::bounds<yaF_double>::highest();
    image_type::coordinate_type const pos_current = from_offset_to_coordinate(coord, i);
    source_coordinate_t pos_min_source;
    for(int j = 0; j < N; j++)
    {
      yaF_double current_dist = dist_op(v_sources[j], pos_current);
      if(min_dist > current_dist)
      {
        min_dist = current_dist;
        pos_min_source = v_sources[j];
      }
    }
    if(std::abs(current_distance - min_dist) / std::max(current_distance, min_dist) > 1E-4)
    {
      std::cout << "problem with the point " << pos_current << "\n";
      std::cout << "The source is " << pos_min_source << " with distance " << min_dist << "\n";
      std::cout << "Found distance is " << current_distance << "\n";
    }
    BOOST_CHECK_CLOSE(current_distance, min_dist, 1E-4);//"Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
  }
  
  std::cout << "Check total milliseconds = " << time_check.total_milliseconds() << std::endl;
}






BOOST_TEST_CASE_TEMPLATE_FUNCTION( test_generic_distances_3D, DIST_AND_SIZE )
{
  BOOST_CHECKPOINT("test_generic_distances_3D generic");
  
  std::cout << std::endl<< std::endl<< "-------------------" << std::endl;
  

  
  
  const int N = mpl::at_c<typename DIST_AND_SIZE::first, 0>::type::value;
  
  
  typedef Image<yaF_double, s_coordinate<3> > image_type;
  
  image_type im_out_dist;
  image_type* p_im[] = {&im_out_dist};
  image_type::coordinate_type coord;
  coord[0] = mpl::at_c<typename DIST_AND_SIZE::first, 1>::type::value;
  coord[1] = mpl::at_c<typename DIST_AND_SIZE::first, 2>::type::value;
  coord[2] = mpl::at_c<typename DIST_AND_SIZE::first, 3>::type::value;
  
  BOOST_CHECKPOINT("test_generic_distances_3D generic: N = " + any_to_string(N) + " / size = " + any_to_string(coord));
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }
  
  //typedef boost::uniform_int<image_type::coordinate_type::scalar_coordinate_type> distribution_type;
  typedef boost::uniform_real<yaF_simple> distribution_type;
  typedef random_generator_type generator_type;
  typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

  generator_type rng;
  distribution_generator_t generator(rng, distribution_type(0, 1.));
  
  // fire n random points
  typedef s_coordinate<image_type::coordinate_type::static_dimensions, yaF_double> source_coordinate_t;
  std::vector< source_coordinate_t > v_sources;
  std::cout << "Source points" << std::endl;
  for(int i = 0; i < N; i++)
  {
    source_coordinate_t current;
    for(int j = 0; j < image_type::coordinate_type::static_dimensions; j++)
    {
      current[j] = generator() * coord[j];//v_generator[j]();
    }
    v_sources.push_back(current);
    //std::cout << current << "\t";
  }
  std::cout << std::endl;
  
  yayi::time::s_time_elapsed time_distance;
  typename DIST_AND_SIZE::second dist_op;
  std::cout << "Distance = " << yayi::errors::demangle(typeid(dist_op).name()) << " -- computation started " << yayi::time::current_date_and_time_as_string() << std::endl;
  yaRC res = distances::exact_distance_t(v_sources, dist_op, im_out_dist);
  std::cout << "N = " << N << "\t--- size = " << im_out_dist.Size() << "\t--- distance total milliseconds = " << time_distance.total_milliseconds() << std::endl;
  std::cout << "N = " << N << "\t--- size = " << im_out_dist.Size() << "\t--- distance total seconds = " << int(time_distance.total_milliseconds() / 1000 + 0.5) << std::endl;

  
  // check des sorties
  std::cout << "Checking" << " -- computation started " << yayi::time::current_date_and_time_as_string() << std::endl;
  yayi::time::s_time_elapsed time_check;
  for(offset i = 0, k = total_number_of_points(coord); i < k; i++) {
    yaF_double current_distance = im_out_dist.pixel(i), min_dist = boost::numeric::bounds<yaF_double>::highest();
    image_type::coordinate_type const pos_current = from_offset_to_coordinate(coord, i);
    source_coordinate_t pos_min_source;
    for(int j = 0; j < N; j++)
    {
      yaF_double current_dist = dist_op(v_sources[j], pos_current);
      if(min_dist > current_dist)
      {
        min_dist = current_dist;
        pos_min_source = v_sources[j];
      }
    }
    if(std::abs(current_distance - min_dist) / std::max(current_distance, min_dist) > 1E-4)
    {
      std::cout << "problem with the point " << pos_current << "\n";
      std::cout << "The source is " << pos_min_source << " with distance " << min_dist << "\n";
      std::cout << "Found distance is " << current_distance << "\n";
    }
    //"Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
    BOOST_CHECK_CLOSE(current_distance, min_dist, 1E-4);
    if((i % (k / 100)) == 0)
      std::cout << ".";
      std::cout.flush();
  }
  std::cout << std::endl;
  std::cout << "Check total milliseconds = " << time_check.total_milliseconds() << std::endl;
  std::cout << "Check total seconds = " << int(time_check.total_milliseconds() / 1000 + 0.5) << std::endl;
  
}


static int counter = 0;

template <int NB_SOURCES, class im_size_t, class distance>
void test_generic_distances_ND(const distance& dist_op = distance())
{
  BOOST_CHECKPOINT("test_generic_distances_ND");
  
  std::cout << std::endl<< std::endl<< "-------------------" << std::endl;
  
  typedef typename yayi::from_mpl_to_coordinate<im_size_t>::result_type coordinate_t;

  const int N = NB_SOURCES;
  
  typedef Image<yaF_double, coordinate_t > image_type;  
  image_type im_out_dist;
  image_type* p_im[] = {&im_out_dist};
  typename image_type::coordinate_type coord = yayi::from_mpl_to_coordinate<im_size_t>::get();

  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE(p_im[i]->SetSize(coord) == yaRC_ok);
    BOOST_REQUIRE_MESSAGE(p_im[i]->AllocateImage() == yaRC_ok, "AllocateImage() error for image index " << i);
  }


  BOOST_CHECKPOINT("test_generic_distances_ND: N = " + any_to_string(N) + " / size = " + any_to_string(coord));
  std::ofstream source_points_log( ("sources__" + any_to_string(counter++, 5) + ".log").c_str() );
  source_points_log << "Distance : " << yayi::errors::demangle(typeid(dist_op).name()) << std::endl;
  source_points_log << "Nb sources : " << N << std::endl;
  source_points_log << "Size image : " << coord << std::endl;
  


  
  //typedef boost::uniform_int<image_type::coordinate_type::scalar_coordinate_type> distribution_type;
  typedef boost::uniform_real<yaF_simple> distribution_type;
  typedef random_generator_type generator_type;
  typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

  generator_type rng;
  distribution_generator_t generator(rng, distribution_type(0, 1.));
  
  // fire n random points
  typedef s_coordinate<image_type::coordinate_type::static_dimensions, yaF_double> source_coordinate_t;
  std::vector< source_coordinate_t > v_sources;
  BOOST_CHECKPOINT("Source points");
  for(int i = 0; i < N; i++)
  {
    source_coordinate_t current;
    for(int j = 0; j < image_type::coordinate_type::static_dimensions; j++)
    {
      current[j] = generator() * coord[j];//v_generator[j]();
    }
    v_sources.push_back(current);
    source_points_log << current ;
  }

  BOOST_CHECKPOINT("Computation");  
  yayi::time::s_time_elapsed time_distance;
  source_points_log << "\nComputation --- started " << yayi::time::current_date_and_time_as_string() << std::endl;
  yaRC res = distances::exact_distance_t(v_sources, dist_op, im_out_dist);
  source_points_log << "Computation --- ended " << yayi::time::current_date_and_time_as_string() << std::endl;
  source_points_log << "Total milliseconds = " << time_distance.total_milliseconds() << std::endl;
  source_points_log << "Total seconds = " << int(time_distance.total_milliseconds() / 1000 + 0.5) << std::endl;

  
  // check des sorties
  BOOST_CHECKPOINT("Check");    
  source_points_log << "Checking -- started " << yayi::time::current_date_and_time_as_string() << std::endl;
  yayi::time::s_time_elapsed time_check;
  for(offset i = 0, k = total_number_of_points(coord); i < k; i++) {
    yaF_double current_distance = im_out_dist.pixel(i), min_dist = boost::numeric::bounds<yaF_double>::highest();
    typename image_type::coordinate_type const pos_current = from_offset_to_coordinate(coord, i);
    source_coordinate_t pos_min_source;
    for(int j = 0; j < N; j++)
    {
      yaF_double current_dist = dist_op(v_sources[j], pos_current);
      if(min_dist > current_dist)
      {
        min_dist = current_dist;
        pos_min_source = v_sources[j];
      }
    }
    if(std::abs(current_distance - min_dist) / std::max(current_distance, min_dist) > 1E-4)
    {
      source_points_log << "problem with the point " << pos_current << "\n";
      source_points_log << "The source is " << pos_min_source << " with distance " << min_dist << "\n";
      source_points_log << "Found distance is " << current_distance << "\n";
    }
    //"Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
    BOOST_CHECK_CLOSE(current_distance, min_dist, 1E-4);
    if((i % (k / 100)) == 0)
      source_points_log << ".";
      source_points_log.flush();
  }
  source_points_log << std::endl;
  source_points_log << "Checking -- ended " << yayi::time::current_date_and_time_as_string() << std::endl;
  source_points_log << "Total milliseconds = " << time_check.total_milliseconds() << std::endl;
  source_points_log << "Total seconds = " << int(time_check.total_milliseconds() / 1000 + 0.5) << std::endl;

  source_points_log.close();
  
}






template <class dist_op_t>
struct s_distance_registration_helper
{
  typedef boost::mpl::list<
    mpl::pair < mpl::vector_c<int,100,  100,  100,  100>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,100,  500,  500,  500>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,100, 1000, 1000, 1000>,      dist_op_t>,
    mpl::pair < mpl::vector_c<int,200,  100,  100,  100>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,200,  500,  500,  500>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,200, 1000, 1000 ,1000>,      dist_op_t>,
    mpl::pair < mpl::vector_c<int,500,  100,  100,  100>,      dist_op_t>/*,
    //mpl::pair < mpl::vector_c<int,500,  500,  500,  500>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,500, 1000, 1000, 1000>,      dist_op_t>,
    //mpl::pair < mpl::vector_c<int,1000,  100,  100,  100>,     dist_op_t>
    //mpl::pair < mpl::vector_c<int,1000,  500,  500,  500>,     dist_op_t>//,
    //mpl::pair < mpl::vector_c<int,1000, 1000, 1000, 1000>,     dist_op_t>*/
  > type;
};

#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
using namespace boost::numeric::ublas;

template <int dim>
matrix<double> get_rotation_matrix(const int dim1, const int dim2, const double angle)
{
  matrix<double> m (dim, dim);
  for (unsigned i = 0; i < m.size1 (); ++ i)
  {
    for (unsigned j = 0; j < m.size2 (); ++ j)
    {
      if(i == j)
      {
        m(i, j) = 1;
      }
      else
      {
        m (i, j) = 0;
      }
    }
  }
  
  m(dim1, dim1) = m(dim2, dim2) = std::cos(angle);
  m(dim1, dim2) = std::sin(angle);
  m(dim2, dim1) = -std::sin(angle);

  return m;
}


template <int dim>
matrix<double> get_diagonal_matrix(const double* diagonal_value)
{
  matrix<double> m (dim, dim);
  for (unsigned i = 0; i < m.size1 (); ++ i)
  {
    for (unsigned j = 0; j < m.size2 (); ++ j)
    {
      if(i == j)
      {
        m(i, j) = *(diagonal_value++);
      }
      else
      {
        m (i, j) = 0;
      }
    }
  }
  return m;
}

std::vector<double> matrix_to_vector(const matrix<double>&m)
{
  std::vector<double> out;
  for (unsigned i = 0; i < m.size1 (); ++ i)
  {
    for (unsigned j = 0; j < m.size2 (); ++ j)
    {
      out.push_back(m(i,j));
    }
  }

  return out;
}


template <int dim, class T>
yayi::distances::s_generic_euclidian_norm_op<s_coordinate<dim, T>, s_coordinate<dim> > get_random_distance()
{
  typedef yayi::distances::s_generic_euclidian_norm_op<s_coordinate<dim, T>, s_coordinate<dim> > out_type;
  
  typedef boost::uniform_real<yaF_double> distribution_type;
  typedef random_generator_type generator_type;
  typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

  static generator_type rng;
  static distribution_generator_t generator(rng, distribution_type(0, 1.));
  
  std::vector< double > v_diag;
  BOOST_CHECKPOINT("Source points");
  for(int i = 0; i < dim; i++)
  {
    v_diag.push_back(generator() + 1.);
    std::cout << v_diag.back() << "\t";
  }  
  
  matrix<double> md = get_diagonal_matrix<dim>(&(*v_diag.begin()));
  matrix<double> mu = get_rotation_matrix<dim>(0, 1, generator() * 2*yaPI);
  for(unsigned int i = 1; i < dim-1; i++)
  {
    matrix<double> r = get_rotation_matrix<dim>(i, i+1, generator() * 2*yaPI);
    std::cout << "matrix dim " << i << " is " << r << std::endl;
    mu = prod(matrix<double>(mu), r);
  }
  
  matrix<double> m = prod(matrix<double>(trans(mu)), md) ; 
  m = prod(matrix<double>(m), mu);
  
  std::cout << "matrix is:" << std::endl;
  std::cout << m << std::endl;
  
  return out_type(matrix_to_vector(m));
}





void register_exact_tests(test_suite*& test) 
{
#if 0
  test->add( BOOST_TEST_CASE(&test_distance_functions) );

  int params_nb_sources[] = { 10, 100, 300, 400, 500 };
  test->add( BOOST_PARAM_TEST_CASE( (&test_distance_exact<50, 60>), params_nb_sources, (params_nb_sources + sizeof(params_nb_sources)/sizeof(params_nb_sources[0])) ) );
  test->add( BOOST_PARAM_TEST_CASE( (&test_distance_exact<100, 100>), params_nb_sources, (params_nb_sources + sizeof(params_nb_sources)/sizeof(params_nb_sources[0])) ) );
  test->add( BOOST_PARAM_TEST_CASE( (&test_distance_exact<200, 200>), params_nb_sources, (params_nb_sources + sizeof(params_nb_sources)/sizeof(params_nb_sources[0])) ) );
  test->add( BOOST_PARAM_TEST_CASE( (&test_distance_exact<500, 500>), params_nb_sources, (params_nb_sources + sizeof(params_nb_sources)/sizeof(params_nb_sources[0])) ) );
  test->add( BOOST_PARAM_TEST_CASE( (&test_distance_exact<1000, 1000>), params_nb_sources, (params_nb_sources + sizeof(params_nb_sources)/sizeof(params_nb_sources[0])) ) );

  typedef s_coordinate<3> coordinate_type;
  typedef s_coordinate<3, yaF_double> source_coordinate_t;
  
  typedef s_distance_registration_helper<distances::s_euclidian_distance_op<source_coordinate_t, coordinate_type> >::type T1;
  typedef s_distance_registration_helper<distances::s_l5_distance_op<source_coordinate_t, coordinate_type> >::type T2;
  typedef s_distance_registration_helper<distances::s_lp_distance_op<source_coordinate_t, coordinate_type, 7, 5> >::type T3;
  typedef s_distance_registration_helper<distances::s_lp_distance_op<source_coordinate_t, coordinate_type, 9, 5> >::type T4;
  test->add( BOOST_TEST_CASE_TEMPLATE( test_generic_distances_3D, T1) );
  test->add( BOOST_TEST_CASE_TEMPLATE( test_generic_distances_3D, T2) );
  test->add( BOOST_TEST_CASE_TEMPLATE( test_generic_distances_3D, T3) );
  test->add( BOOST_TEST_CASE_TEMPLATE( test_generic_distances_3D, T4) );
#endif
  
  typedef mpl::vector_c<int,100,  100,  100> s_100_3;
  typedef mpl::vector_c<int, 50,  50,  50, 50> s_50_4;
  typedef mpl::vector_c<int,500,  500,  500> s_500_3;
  typedef yayi::distances::s_generic_euclidian_norm_op<s_coordinate<3, yaF_double>, s_coordinate<3> > distance3_type;
  typedef yayi::distances::s_generic_euclidian_norm_op<s_coordinate<4, yaF_double>, s_coordinate<4> > distance4_type;
  
  static const distance3_type distances_3 [] = {get_random_distance<3, yaF_double>(), get_random_distance<3, yaF_double>(), get_random_distance<3, yaF_double>()};
  
  // 100^3 // 500 sources
  test->add( 
    BOOST_PARAM_TEST_CASE( 
      (&test_generic_distances_ND<500, s_100_3, distance3_type>), 
      distances_3, 
      (distances_3 + sizeof(distances_3)/sizeof(distances_3[0])) ) );
   
  #if 0
  // 500^3 / 50 sources
  test->add( 
    BOOST_PARAM_TEST_CASE( 
      (&test_generic_distances_ND<50, s_500_3, distance3_type>), 
      distances_3, 
      (distances_3 + sizeof(distances_3)/sizeof(distances_3[0])) ) );

  static const distance4_type distances_4 [] = {get_random_distance<4, yaF_double>(), get_random_distance<4, yaF_double>()};
  
  // 50^4 / 50 sources
  test->add( 
    BOOST_PARAM_TEST_CASE( 
      (&test_generic_distances_ND<50, s_50_4, distance4_type>), 
      distances_4, 
      (distances_4 + sizeof(distances_4)/sizeof(distances_4[0])) ) );

  #endif
  
}
