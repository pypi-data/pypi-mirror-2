// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "boost/python/object.hpp"
#include "CvVectors.pypp.hpp"

namespace bp = boost::python;

static ::CvVectors * get_next( ::CvVectors const & inst ) { return inst.next; }

void register_CvVectors_class(){

    bp::class_< CvVectors >( "CvVectors" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvVectors >() )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvVectors >() )    
        .def_readwrite( "count", &CvVectors::count )    
        .def_readwrite( "dims", &CvVectors::dims )    
        .def_readwrite( "type", &CvVectors::type )    
        .add_property( "next", bp::make_function(&::get_next, bp::return_internal_reference<>()) );

}
