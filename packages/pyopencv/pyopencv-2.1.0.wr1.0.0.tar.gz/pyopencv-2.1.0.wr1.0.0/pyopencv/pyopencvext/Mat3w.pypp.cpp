// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "opencv_converters.hpp"
#include "Mat3w.pypp.hpp"

namespace bp = boost::python;

void register_Mat3w_class(){

    { //::cv::Mat_< cv::Vec< unsigned short, 3 > >
        typedef bp::class_< cv::Mat_< cv::Vec< unsigned short, 3 > >, bp::bases< cv::Mat > > Mat3w_exposer_t;
        Mat3w_exposer_t Mat3w_exposer = Mat3w_exposer_t( "Mat3w", bp::init< >() );
        bp::scope Mat3w_scope( Mat3w_exposer );
        Mat3w_exposer.add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::Mat_< cv::Vec< unsigned short, 3 > > >() );
        Mat3w_exposer.def( bp::init< int, int >(( bp::arg("_rows"), bp::arg("_cols") )) );
        Mat3w_exposer.def( bp::init< int, int, cv::Vec< unsigned short, 3 > const & >(( bp::arg("_rows"), bp::arg("_cols"), bp::arg("value") )) );
        Mat3w_exposer.def( bp::init< cv::Size_< int > >(( bp::arg("_size") )) );
        bp::implicitly_convertible< cv::Size_< int >, cv::Mat_< cv::Vec< unsigned short, 3 > > >();
        Mat3w_exposer.def( bp::init< cv::Size_< int >, cv::Vec< unsigned short, 3 > const & >(( bp::arg("_size"), bp::arg("value") )) );
        Mat3w_exposer.def( bp::init< cv::Mat const & >(( bp::arg("m") )) );
        bp::implicitly_convertible< cv::Mat const &, cv::Mat_< cv::Vec< unsigned short, 3 > > >();
        Mat3w_exposer.def( bp::init< cv::Mat_< cv::Vec< unsigned short, 3 > > const & >(( bp::arg("m") )) );
        Mat3w_exposer.def( bp::init< cv::Mat_< cv::Vec< unsigned short, 3 > > const &, cv::Range const &, cv::Range const & >(( bp::arg("m"), bp::arg("rowRange"), bp::arg("colRange") )) );
        Mat3w_exposer.def( bp::init< cv::Mat_< cv::Vec< unsigned short, 3 > > const &, cv::Rect_< int > const & >(( bp::arg("m"), bp::arg("roi") )) );
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::adjustROI
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > & ( exported_class_t::*adjustROI_function_type )( int,int,int,int ) ;
            
            Mat3w_exposer.def( 
                "adjustROI"
                , adjustROI_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::adjustROI )
                , ( bp::arg("dtop"), bp::arg("dbottom"), bp::arg("dleft"), bp::arg("dright") )
                , bp::return_self< >() );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::channels
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef int ( exported_class_t::*channels_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "channels"
                , channels_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::channels ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::clone
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*clone_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "clone"
                , clone_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::clone ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::col
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*col_function_type )( int ) const;
            
            Mat3w_exposer.def( 
                "col"
                , col_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::col )
                , ( bp::arg("x") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::create
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef void ( exported_class_t::*create_function_type )( int,int ) ;
            
            Mat3w_exposer.def( 
                "create"
                , create_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::create )
                , ( bp::arg("_rows"), bp::arg("_cols") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::create
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef void ( exported_class_t::*create_function_type )( ::cv::Size_< int > ) ;
            
            Mat3w_exposer.def( 
                "create"
                , create_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::create )
                , ( bp::arg("_size") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::cross
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*cross_function_type )( ::cv::Mat_< cv::Vec< unsigned short, 3 > > const & ) const;
            
            Mat3w_exposer.def( 
                "cross"
                , cross_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::cross )
                , ( bp::arg("m") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::depth
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef int ( exported_class_t::*depth_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "depth"
                , depth_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::depth ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::diag
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*diag_function_type )( int ) const;
            
            Mat3w_exposer.def( 
                "diag"
                , diag_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::diag )
                , ( bp::arg("d")=(int)(0) ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::elemSize
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::size_t ( exported_class_t::*elemSize_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "elemSize"
                , elemSize_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::elemSize ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::elemSize1
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::size_t ( exported_class_t::*elemSize1_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "elemSize1"
                , elemSize1_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::elemSize1 ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::reshape
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*reshape_function_type )( int ) const;
            
            Mat3w_exposer.def( 
                "reshape"
                , reshape_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::reshape )
                , ( bp::arg("_rows") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::row
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::cv::Mat_< cv::Vec< unsigned short, 3 > > ( exported_class_t::*row_function_type )( int ) const;
            
            Mat3w_exposer.def( 
                "row"
                , row_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::row )
                , ( bp::arg("y") ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::step1
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::size_t ( exported_class_t::*step1_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "step1"
                , step1_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::step1 ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::stepT
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef ::size_t ( exported_class_t::*stepT_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "stepT"
                , stepT_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::stepT ) );
        
        }
        { //::cv::Mat_< cv::Vec< unsigned short, 3 > >::type
        
            typedef cv::Mat_< cv::Vec< unsigned short, 3 > > exported_class_t;
            typedef int ( exported_class_t::*type_function_type )(  ) const;
            
            Mat3w_exposer.def( 
                "type"
                , type_function_type( &::cv::Mat_< cv::Vec< unsigned short, 3 > >::type ) );
        
        }
    }

}
