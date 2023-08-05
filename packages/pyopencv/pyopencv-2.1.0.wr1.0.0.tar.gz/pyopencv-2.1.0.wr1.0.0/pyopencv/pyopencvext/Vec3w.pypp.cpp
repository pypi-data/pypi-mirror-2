// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "ndarray.hpp"
#include "Vec3w.pypp.hpp"

namespace bp = boost::python;

void register_Vec3w_class(){

    { //::cv::Vec< unsigned short, 3 >
        typedef bp::class_< cv::Vec< unsigned short, 3 > > Vec3w_exposer_t;
        Vec3w_exposer_t Vec3w_exposer = Vec3w_exposer_t( "Vec3w", bp::init< >() );
        bp::scope Vec3w_scope( Vec3w_exposer );
        Vec3w_exposer.add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::Vec< unsigned short, 3 > >() );
        bp::scope().attr("depth") = (int)cv::Vec<unsigned short, 3>::depth;
        bp::scope().attr("channels") = (int)cv::Vec<unsigned short, 3>::channels;
        bp::scope().attr("type") = (int)cv::Vec<unsigned short, 3>::type;
        Vec3w_exposer.def( bp::init< short unsigned int >(( bp::arg("v0") )) );
        bp::implicitly_convertible< short unsigned int, cv::Vec< unsigned short, 3 > >();
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7"), bp::arg("v8") )) );
        Vec3w_exposer.def( bp::init< short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int, short unsigned int >(( bp::arg("v0"), bp::arg("v1"), bp::arg("v2"), bp::arg("v3"), bp::arg("v4"), bp::arg("v5"), bp::arg("v6"), bp::arg("v7"), bp::arg("v8"), bp::arg("v9") )) );
        Vec3w_exposer.def( bp::init< cv::Vec< unsigned short, 3 > const & >(( bp::arg("v") )) );
        { //::cv::Vec< unsigned short, 3 >::all
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef ::cv::Vec< unsigned short, 3 > ( *all_function_type )( short unsigned int );
            
            Vec3w_exposer.def( 
                "all"
                , all_function_type( &::cv::Vec< unsigned short, 3 >::all )
                , ( bp::arg("alpha") ) );
        
        }
        { //::cv::Vec< unsigned short, 3 >::cross
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef ::cv::Vec< unsigned short, 3 > ( exported_class_t::*cross_function_type )( ::cv::Vec< unsigned short, 3 > const & ) const;
            
            Vec3w_exposer.def( 
                "cross"
                , cross_function_type( &::cv::Vec< unsigned short, 3 >::cross )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< unsigned short, 3 >::ddot
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef double ( exported_class_t::*ddot_function_type )( ::cv::Vec< unsigned short, 3 > const & ) const;
            
            Vec3w_exposer.def( 
                "ddot"
                , ddot_function_type( &::cv::Vec< unsigned short, 3 >::ddot )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< unsigned short, 3 >::dot
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef short unsigned int ( exported_class_t::*dot_function_type )( ::cv::Vec< unsigned short, 3 > const & ) const;
            
            Vec3w_exposer.def( 
                "dot"
                , dot_function_type( &::cv::Vec< unsigned short, 3 >::dot )
                , ( bp::arg("v") ) );
        
        }
        { //::cv::Vec< unsigned short, 3 >::operator[]
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef short unsigned int ( exported_class_t::*__getitem___function_type )( int ) const;
            
            Vec3w_exposer.def( 
                "__getitem__"
                , __getitem___function_type( &::cv::Vec< unsigned short, 3 >::operator[] )
                , ( bp::arg("i") ) );
        
        }
        { //::cv::Vec< unsigned short, 3 >::operator[]
        
            typedef cv::Vec< unsigned short, 3 > exported_class_t;
            typedef short unsigned int & ( exported_class_t::*__getitem___function_type )( int ) ;
            
            Vec3w_exposer.def( 
                "__getitem__"
                , __getitem___function_type( &::cv::Vec< unsigned short, 3 >::operator[] )
                , ( bp::arg("i") )
                , bp::return_value_policy< bp::copy_non_const_reference >() );
        
        }
        Vec3w_exposer.staticmethod( "all" );
        Vec3w_exposer.def("from_ndarray", &bp::from_ndarray< cv::Vec3w >, (bp::arg("arr")) );
        Vec3w_exposer.staticmethod("from_ndarray");
        Vec3w_exposer.add_property("ndarray", &bp::as_ndarray< cv::Vec3w >);
    }

}
