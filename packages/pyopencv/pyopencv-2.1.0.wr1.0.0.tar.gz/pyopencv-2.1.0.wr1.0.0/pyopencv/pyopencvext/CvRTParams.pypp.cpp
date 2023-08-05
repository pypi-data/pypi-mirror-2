// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "CvRTParams.pypp.hpp"

namespace bp = boost::python;

void register_CvRTParams_class(){

    bp::class_< CvRTParams, bp::bases< CvDTreeParams > >( "CvRTParams", bp::init< >() )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvRTParams >() )    
        .def( bp::init< int, int, float, bool, int, float const *, bool, int, int, float, int >(( bp::arg("_max_depth"), bp::arg("_min_sample_count"), bp::arg("_regression_accuracy"), bp::arg("_use_surrogates"), bp::arg("_max_categories"), bp::arg("_priors"), bp::arg("_calc_var_importance"), bp::arg("_nactive_vars"), bp::arg("max_num_of_trees_in_the_forest"), bp::arg("forest_accuracy"), bp::arg("termcrit_type") )) )    
        .def_readwrite( "calc_var_importance", &CvRTParams::calc_var_importance )    
        .def_readwrite( "nactive_vars", &CvRTParams::nactive_vars )    
        .def_readwrite( "term_crit", &CvRTParams::term_crit );

}
