// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "ndarray.hpp"
#include "Vec6d.pypp.hpp"

namespace bp = boost::python;

void register_Vec6d_class(){

    { //::cv::Vec< double, 6 >
        typedef bp::class_< cv::Vec< double, 6 > > Vec6d_exposer_t;
        Vec6d_exposer_t Vec6d_exposer = Vec6d_exposer_t( "Vec6d", bp::init< >() );
        bp::scope Vec6d_scope( Vec6d_exposer );
        Vec6d_exposer.add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::Vec< double, 6 > >() );
        bp::scope().attr("depth") = (int)cv::Vec<double, 6>::depth;
        bp::scope().attr("channels") = (int)cv::Vec<double, 6>::channels;
        bp::scope().attr("type") = (int)cv::Vec<double, 6>::type;
        Vec6d_exposer.def( bp::init< double >(( bp::arg("v0") )) );
        bp::implicitly_convertible< double, cv::Vec< double, 6 > >();
        Vec6d_exposer.def( bp::init< double, double >(( bp::arg("v0"), bp::arg("v1") )) );
        Vec6d_exposer.def( bp::init< double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7"), bp::arg("v8") )) );
        Vec6d_exposer.def( bp::init< double, double, double, double, double, double, double, double, double, double >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7"), bp::arg("v8"), bp::arg("v9") )) );
        Vec6d_exposer.def( bp::init< cv::Vec< double, 6 > const & >(( bp::arg("v") )) );
        { //::cv::Vec< double, 6 >::all
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef ::cv::Vec< double, 6 > ( *all_function_type )( double );
            
            Vec6d_exposer.def( 
                "all"
                , all_function_type( &::cv::Vec< double, 6 >::all )
                , ( bp::arg("alpha") ) );
        
        }
        { //::cv::Vec< double, 6 >::cross
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef ::cv::Vec< double, 6 > ( exported_class_t::*cross_function_type )( ::cv::Vec< double, 6 > const & ) const;
            
            Vec6d_exposer.def( 
                "cross"
                , cross_function_type( &::cv::Vec< double, 6 >::cross )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< double, 6 >::ddot
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef double ( exported_class_t::*ddot_function_type )( ::cv::Vec< double, 6 > const & ) const;
            
            Vec6d_exposer.def( 
                "ddot"
                , ddot_function_type( &::cv::Vec< double, 6 >::ddot )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< double, 6 >::dot
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef double ( exported_class_t::*dot_function_type )( ::cv::Vec< double, 6 > const & ) const;
            
            Vec6d_exposer.def( 
                "dot"
                , dot_function_type( &::cv::Vec< double, 6 >::dot )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< double, 6 >::operator[]
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef double ( exported_class_t::*__getitem___function_type )( int ) const;
            
            Vec6d_exposer.def( 
                "__getitem__"
                , __getitem___function_type( &::cv::Vec< double, 6 >::operator[] )
                , ( bp::arg("i") ) );
        
        }
        { //::cv::Vec< double, 6 >::operator[]
        
            typedef cv::Vec< double, 6 > exported_class_t;
            typedef double & ( exported_class_t::*__getitem___function_type )( int ) ;
            
            Vec6d_exposer.def( 
                "__getitem__"
                , __getitem___function_type( &::cv::Vec< double, 6 >::operator[] )
                , ( bp::arg("i") )
                , bp::return_value_policy< bp::copy_non_const_reference >() );
        
        }
        Vec6d_exposer.staticmethod( "all" );
        Vec6d_exposer.def("from_ndarray", &bp::from_ndarray< cv::Vec6d >, (bp::arg("arr")) );
        Vec6d_exposer.staticmethod("from_ndarray");
        Vec6d_exposer.add_property("ndarray", &bp::as_ndarray< cv::Vec6d >);
    }

}
